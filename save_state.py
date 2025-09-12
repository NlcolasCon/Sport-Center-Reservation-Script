from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # keep visible for login
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://applications2.ucy.ac.cy/sportscenter/main_online_new?p_lang=en")

        print(">>> Log in manually in the browser window that opened <<<")
        print(">>> When you’re at the reservations page, press ENTER here <<<")
        input()

        context.storage_state(path="state.json")
        browser.close()

if __name__ == "__main__":
    main()
