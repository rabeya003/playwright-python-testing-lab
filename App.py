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

    # Only load storage_state if it exists and has content
    if STATE.exists() and STATE.stat().st_size > 0:
        context = browser.new_context(storage_state=str(STATE))
    else:
        context = browser.new_context()

    page = context.new_page()
    page.goto("https://accounts.google.com/")
    page.pause()

    context.close()
    browser.close()
