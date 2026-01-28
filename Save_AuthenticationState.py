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

    email_input = page.get_by_label("Email or phone")

    email_input.click()
    email_input.fill("")  
    page.wait_for_timeout(500) 

    email_input.type("rabeya@gmail.com", delay=150)
    page.get_by_role("button",name="Next").click()

    #Enter Pass
    password_input=page.get_by_label("Enter your password")
    password_input.fill("Pass123")

    page.get_by_role("button",name="Next").click()

    page.pause()

    #Save Authentication State
    context.storage_state(
        path="playwright/.auth/storage_state.json"
    )

    context.close()