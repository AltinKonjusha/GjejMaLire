from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Opens real browser so you can see it
    page = browser.new_page()
    page.goto("https://gjirafa50.com/search?q=iphone", timeout=15000)
    page.wait_for_timeout(4000)  # Wait 4 seconds for page to load
    
    # Print the full HTML so we can see the structure
    html = page.content()
    
    # Save to file so we can read it easily
    with open('gjirafa50_html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML saved to gjirafa50_html.txt")
    print("Page title:", page.title())
    browser.close()