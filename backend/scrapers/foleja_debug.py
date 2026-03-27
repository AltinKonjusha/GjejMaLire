from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.foleja.com/search?search=iphone", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_selector('.product-box', timeout=15000)

    items = page.query_selector_all('.product-box')
    
    for item in items[:3]:
        name = item.query_selector('a.product-name')
        price_wrapper = item.query_selector('.whole-original-price')
        
        if name and price_wrapper:
            print("--- PRODUCT ---")
            print("Name:", name.inner_text().strip())
            print("Price inner_text repr:", repr(price_wrapper.inner_text()))
            print("Price innerHTML:", price_wrapper.inner_html())
            print()
    
    browser.close()