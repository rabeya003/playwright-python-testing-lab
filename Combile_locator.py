from pathlib import Path
from playwright.sync_api import sync_playwright
import time

AUTH_DIR = Path(__file__).parent / "playwright" / ".auth"
AUTH_DIR.mkdir(parents=True, exist_ok=True)
STATE = AUTH_DIR / "storage_state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to Google accounts
    print("Navigating to Google accounts...")
    page.goto("https://accounts.google.com/")
    
    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")
    time.sleep(3)  # Wait 3 seconds for page to render
    
    print("Waiting for email page to load...")
    
    # IMPORTANT: You're going to accounts.google.com which is the LOGIN page
    # You need to actually LOGIN first before you can access emails
    # Let's check if we're on login page
    if page.locator("input[type='email']").count() > 0:
        print("You need to login first! The script is trying to access Gmail directly.")
        print("Please login manually, then we'll continue...")
        
        # Wait for user to login manually
        input("Press Enter after you've logged in and see your Gmail inbox...")
    
    # After login, wait for Gmail interface to load
    print("Waiting for Gmail interface...")
    page.wait_for_load_state("networkidle")
    time.sleep(5)  # Wait 5 seconds for Gmail to fully load
    
    # Wait for the email table to appear
    print("Looking for email table...")
    try:
        page.wait_for_selector("div.UI table", timeout=15000)
        print("Email table found!")
    except:
        print("Email table not found. Taking screenshot for debugging...")
        page.screenshot(path="debug_no_email_table.png")
        print("Current URL:", page.url)
        print("Page title:", page.title())
        context.close()
        browser.close()
        exit()
    
    # Wait a bit more for emails to load
    time.sleep(2)
    
    # Now try to get emails
    new_emails = []
    emails = page.locator("div.UI table tr")
    
    # Wait for at least some email rows to be visible
    print(f"Found {emails.count()} email rows")
    
    if emails.count() == 0:
        print("No emails found. Taking screenshot...")
        page.screenshot(path="debug_no_emails.png")
    else:
        print("Processing emails...")
        # Process each email with a small delay
        for i, email in enumerate(emails.all()):
            print(f"Processing email {i+1} of {emails.count()}...")
            
            # Add small delay between processing each email
            time.sleep(0.5)
            
            is_new_email = email.locator(
                "td li[data-tooltip='Mark as read']"
            ).count() == 1
            
            if is_new_email:
                try:
                    sender = email.locator("td span[email]:visible").inner_text(timeout=2000)
                    title = email.locator("td span[data-thread-id]:visible").inner_text(timeout=2000)
                    new_emails.append([sender, title])
                    print(f"  Found new email: {sender} - {title}")
                except:
                    print(f"  Could not extract details from email {i+1}")
    
    # Show results
    print("\n" + "="*50)
    if len(new_emails) == 0:
        print("No new emails!")
    else:
        print(f"{len(new_emails)} new emails!")
        print("="*50)
        for i, new_email in enumerate(new_emails, 1):
            print(f"\nEmail #{i}:")
            print(f"From: {new_email[0]}")
            print(f"Subject: {new_email[1]}")
            print("-" * 30)
    
    # Take final screenshot for reference
    page.screenshot(path="final_result.png")
    print(f"\nScreenshot saved as 'final_result.png'")
    
    # Keep browser open for a moment to see results
    print("\nScript completed. Browser will close in 5 seconds...")
    time.sleep(5)
    
    context.close()
    browser.close()