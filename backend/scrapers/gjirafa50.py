from playwright.sync_api import sync_playwright
import re

def scrape_gjirafa50(query: str) -> list:
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            url = f"https://gjirafa50.com/search?q={query.replace(' ', '+')}"
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_selector('.product-item', timeout=10000)
            
            items = page.query_selector_all('.product-item')
            
            for item in items[:10]:
                try:
                    name = item.query_selector('.product-title a')
                    price = item.query_selector('.price.main')
                    link = item.query_selector('.picture a')
                    image = item.query_selector('.picture img')

                    if name and price and link:
                        price_text = price.inner_text().strip()
                        price_clean = re.sub(r'[^\d.,]', '', price_text)
                        price_clean = price_clean.replace(',', '.')

                        results.append({
                            'platform': 'gjirafa50',
                            'name': name.inner_text().strip(),
                            'price': float(price_clean) if price_clean else None,
                            'currency': 'EUR',
                            'url': 'https://gjirafa50.com' + link.get_attribute('href'),
                            'image_url': image.get_attribute('src') if image else None,
                            'in_stock': True,
                        })
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Gjirafa50 scraper error: {e}")
        finally:
            browser.close()
    
    return results


if __name__ == '__main__':
    results = scrape_gjirafa50('iphone')
    for r in results:
        print(r)