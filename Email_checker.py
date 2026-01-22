from pathlib import Path
from playwright.sync_api import sync_playwright


AUTH_DIR = Path(__file__).parent / "playwright" / ".auth"
AUTH_DIR.mkdir(parents=True, exist_ok=True)
STATE = AUTH_DIR / "storage_state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500,
        args=["--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://accounts.google.com/")
    input("Log in in the opened browser, then press Enter here...")

    context.storage_state(path=str(STATE))
    print("Saved:", STATE)

    email_input=page.get_by_label("Email or phone")



    browser.close()
