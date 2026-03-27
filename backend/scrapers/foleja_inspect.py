from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.foleja.com/search?search=iphone", timeout=15000)
    page.wait_for_timeout(4000)
    
    with open('foleja_html.txt', 'w', encoding='utf-8') as f:
        f.write(page.content())
    
    print("Done! Check foleja_html.txt")
    print("Page title:", page.title())
    browser.close()