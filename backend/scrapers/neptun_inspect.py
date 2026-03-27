from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.neptun-ks.com/search-product-result.nspx?q=iphone", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    
    with open('neptun_html.txt', 'w', encoding='utf-8') as f:
        f.write(page.content())
    
    print("Done! Title:", page.title())
    browser.close()