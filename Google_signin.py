from pathlib import Path
from playwright.sync_api import sync_playwright

AUTH_DIR = Path(__file__).parent / "playwright" / ".auth"
AUTH_DIR.mkdir(parents=True, exist_ok=True)
STATE = AUTH_DIR / "storage_state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://accounts.google.com/")

    email_input = page.get_by_label("Email or phone")

    email_input.click()
    email_input.fill("")  # ensure empty
    page.wait_for_timeout(500)  # small pause before typing (optional)

    email_input.type("rabeya@gmail.com", delay=150)  # 150ms per character (slower typing)
    page.wait_for_timeout(800)  # pause to see the result (optional)

    email_input.clear()
