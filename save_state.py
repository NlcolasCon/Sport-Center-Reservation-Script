# save_state.py
import argparse
from playwright.sync_api import sync_playwright

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="state.json", help="Path to save storage state (per user)")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://applications2.ucy.ac.cy/sportscenter/main_online_new?p_lang=en")

        print(">>> Log in manually in the window that opened")
        print(">>> When you’re at the reservations page, press ENTER here")
        input()

        context.storage_state(path=args.state)
        browser.close()
        print(f"[OK] Saved session to {args.state}")

if __name__ == "__main__":
    main()
