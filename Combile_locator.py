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
    new_emails=[]
    emails=page.locator("div.UI table tr")

    for email in emails.all():
        is_new_email=email.locator(
            "td li[data-tooltip='Mark as read]"
        ).count()=1
        if is_new_email:
            sender=email.locator("td span[email]:visible").inner_text()
            title=email.locator("td span [data-thread-id]:visible").inner_text()
            new_emails.append(
                [sender,title]
            )