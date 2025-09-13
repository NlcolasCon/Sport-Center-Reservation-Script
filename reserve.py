# reserve.py
import time
import random
import datetime as dt
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import re
from datetime import date, timedelta
import argparse

BASE_URL = "https://applications2.ucy.ac.cy/sportscenter/main_online_new?p_lang=en"

def jitter(min_s=0.4, max_s=1.4):
    time.sleep(random.uniform(min_s, max_s))

def desired_time_for_today() -> str:
    # Monday = 1 .. Sunday = 7
    if dt.datetime.now().isoweekday() == 1:
        return "12:15" 
    if dt.datetime.now().isoweekday() == 7:
        return "16:45"
    if dt.datetime.now().isoweekday() == 5:
        return "09:30"
    return "20:15"

def main(headless=True, state_file="state.json", tag="user"):
    SHOT_DIR = Path(f"runs/{tag}"); SHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()
        page.set_default_timeout(15000)

        try:
            # 0) Open site
            page.goto(BASE_URL)
            jitter()

            # 1) Reservations
            try:
                page.get_by_role("link", name="Reservations").first.click()
            except PWTimeout:
                page.get_by_text("Reservations", exact=False).click()
            jitter()

            # 2) Sport = Gymnastic
            try:
                page.get_by_label("Specify the sport", exact=True).select_option(label="Gymnastic")
            except PWTimeout:
                page.locator("select").filter(has_text="Gymnastic").select_option(label="Gymnastic")
            jitter()

            # 3) Agree
            try:
                page.get_by_label("I have read the regulations and I agree", exact=False).check()
            except PWTimeout:
                page.locator("input[type=checkbox]").check()
            jitter()

            # 4) Submit → calendar
            page.get_by_role("button", name="Submit").first.click()
            jitter()

            # 5) Pick date = today + 5
            target_day = (date.today() + timedelta(days=5)).day
            page.locator(f"td >> button:has-text('{target_day}')").first.click()
            jitter()

            # 6) time-period (Mon 12:15, else 20:15)
            TARGET_TIME = desired_time_for_today()
            time_select = page.locator(f"select:has(option:has-text('{TARGET_TIME}'))").first
            time_select.select_option(label=TARGET_TIME)
            jitter()

            # 7) Purpose = 'g'
            purpose_box = page.locator("textarea#textarea, textarea[name='p_skopos']")
            purpose_box.wait_for(state="visible")
            purpose_box.fill("g")

            # 8) Submit (+ confirm if present)
            submit_btn = page.get_by_role("button", name=re.compile(r"^\s*Submit\s*$", re.I)).first
            submit_btn.click()
            jitter(0.6, 1.8)
            try:
                page.get_by_role("button", name=re.compile(r"^\s*Submit\s*$", re.I)).first.click()
            except Exception:
                pass

            # Proof
            stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=str(SHOT_DIR / f"{tag}_success_{stamp}.png"))
            print(f"[OK] ({tag}) Reservation completed at {TARGET_TIME}.")

        except Exception as e:
            stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                page.screenshot(path=str(SHOT_DIR / f"{tag}_error_{stamp}.png"))
            except Exception:
                pass
            Path(f"{tag}_last_error.txt").write_text(f"{stamp}\n{type(e).__name__}: {e}\n")
            raise
        finally:
            context.storage_state(path=state_file)
            browser.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="state.json", help="Path to storage state (per user)")
    ap.add_argument("--tag",   default="user", help="Name used for logs/screenshots")
    ap.add_argument("--headless", action="store_true", help="Run headless (recommended for automation)")
    args = ap.parse_args()
    main(headless=args.headless or True, state_file=args.state, tag=args.tag)
