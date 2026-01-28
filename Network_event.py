from pathlib import Path
from playwright.sync_api import Page,expect,Request,Response,sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500,
        args=["--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
    )

def on_request(request: Request):
    print("Sent Resuest",request)

def on_response(response: Response):
    print("Sent Response",response)

def test_docs_link(page:Page):
    page.on("request",on_request)
    page.on("response",on_response)
    
    page.go("http://playwright.dev/python")

    docs_link=page.get_by_role("link",name="Docs")
    docs_link.click()

    expect(page).to_have_url(
        "https://playwright.dev/python/docs/intro"
    )