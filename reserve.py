# reserve.py
import time
import random
import datetime as dt
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import re
from datetime import date, timedelta

BASE_URL = "https://applications2.ucy.ac.cy/sportscenter/main_online_new?p_lang=en"
TARGET_TIME = "20:15"   # exact label in the time-period dropdown
STATE_FILE = "state.json"  # your saved login
SHOT_DIR = Path("runs"); SHOT_DIR.mkdir(exist_ok=True)

def jitter(min_s=0.4, max_s=1.4):
    time.sleep(random.uniform(min_s, max_s))

def target_date():
    # 5 days after today (local). Adjust display format if needed.
    d = dt.date.today() + dt.timedelta(days=5)
    # Try common site formats in order:
    return {
        "human": d.strftime("%d/%m/%Y"),
        "d": d.day,
        "m": d.strftime("%B"),  # e.g., "September" if calendar shows words
        "iso": d.isoformat()
    }

def main(headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()
        page.set_default_timeout(15000)

        try:
            # 0) Open site
            page.goto(BASE_URL)
            jitter()

            # 1) Go to "Reservations" tab (adjust if the text differs)
            try:
                page.get_by_role("link", name="Reservations").first.click()
            except PWTimeout:
                page.get_by_text("Reservations", exact=False).click()
            jitter()

            # 2) Choose sport = "Gymnastic"
            try:
                page.get_by_label("Specify the sport", exact=True).select_option(label="Gymnastic")
            except PWTimeout:
                page.locator("select").filter(has_text="Gymnastic").select_option(label="Gymnastic")
            jitter()

            # 3) Agree to regulations
            try:
                page.get_by_label("I have read the regulations and I agree", exact=False).check()
            except PWTimeout:
                page.locator("input[type=checkbox]").check()
            jitter()

            # 4) Submit to proceed to slot selection
            page.get_by_role("button", name="Submit").first.click()
            jitter()

            # 5) Pick date = today + 5
            target_day = (date.today() + timedelta(days=5)).day
            target_day_str = str(target_day)

            # click the blue button for that day
            day_button = page.locator(f"td >> button:has-text('{target_day_str}')")
            day_button.first.click()

            jitter()

            # 6) Choose time-period = 20:15 from the dropdown
            time_select = page.locator("select:has(option:has-text('20:15'))").first
            time_select.select_option(label=TARGET_TIME)

            jitter()

            # 7) Purpose = 'g'  (target the actual textarea, not the readonly date input)
            purpose_box = page.locator("textarea#textarea, textarea[name='p_skopos']")
            purpose_box.wait_for(state="visible")
            purpose_box.fill("g")

            # 8) Submit then confirm
            submit_btn = page.get_by_role("button", name=re.compile(r"^\s*Submit\s*$", re.I)).first
            submit_btn.click()
            jitter(0.6, 1.8)
            try:
                page.get_by_role("button", name=re.compile(r"^\s*Submit\s*$", re.I)).first.click()
            except Exception:
                pass

            # Save proof
            stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=str(SHOT_DIR / f"success_{stamp}.png"))
            print("[OK] Reservation flow completed.")

        except Exception as e:
            stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=str(SHOT_DIR / f"error_{stamp}.png"))
            Path("last_error.txt").write_text(f"{stamp}\n{type(e).__name__}: {e}\n")
            raise
        finally:
            context.storage_state(path=STATE_FILE)
            browser.close()

if __name__ == "__main__":
    main(headless=True)
