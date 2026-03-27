from playwright.sync_api import sync_playwright

def scrape_foleja(query: str) -> list:
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            url = f"https://www.foleja.com/search?search={query.replace(' ', '+')}"
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_selector('.product-box', timeout=15000)

            items = page.query_selector_all('.product-box')

            for item in items[:10]:
                try:
                    name = item.query_selector('a.product-name')
                    link = item.query_selector('a.product-image-link')
                    image = item.query_selector('img.product-image')
                    price_wrapper = item.query_selector('.whole-original-price')

                    if name and price_wrapper and link:
                        # Get whole number — it's a raw text node, not in a span
                        # We extract it by removing currency and decimal spans
                        decimal_el = price_wrapper.query_selector('.decimal-rounded-price')
                        currency_el = price_wrapper.query_selector('.currency-symbol')

                        decimal = decimal_el.inner_text().strip() if decimal_el else '00'
                        
                        # Get full text, remove currency and decimal to get whole number
                        full_text = price_wrapper.inner_text()
                        full_text = full_text.replace('€', '').strip()
                        if decimal_el:
                            full_text = full_text.replace(decimal, '').strip()
                        
                        # Clean whitespace and newlines
                        whole = ''.join(full_text.split())
                        
                        price_str = f"{whole}.{decimal}"
                        price = float(price_str)

                        results.append({
                            'platform': 'foleja',
                            'name': name.inner_text().strip(),
                            'price': price,
                            'currency': 'EUR',
                            'url': link.get_attribute('href'),
                            'image_url': image.get_attribute('src') if image else None,
                            'in_stock': True,
                        })
                except Exception:
                    continue

        except Exception as e:
            print(f"Foleja scraper error: {e}")
        finally:
            browser.close()

    return results


if __name__ == '__main__':
    results = scrape_foleja('iphone')
    for r in results:
        print(r)