from playwright.sync_api import sync_playwright
import re

def scrape_neptun(query: str) -> list:
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            url = f"https://www.neptun-ks.com/search-product-result.nspx?q={query.replace(' ', '+')}"
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_selector('.productWrapperInner', timeout=15000)

            items = page.query_selector_all('.productWrapperInner')

            for item in items[:10]:
                try:
                    name = item.query_selector('h2.product-list-item__content--title')
                    link = item.query_selector('a.theLink')
                    image = item.query_selector('.imageWrapper img')
                    price_el = item.query_selector('span.priceNum')

                    if name and price_el and link:
                        price_text = price_el.inner_text().strip()
                        price_clean = price_text.replace(',', '.')
                        price_clean = re.sub(r'[^\d.]', '', price_clean)

                        href = link.get_attribute('href')
                        full_url = f"https://www.neptun-ks.com{href}" if href.startswith('/') else href

                        img_src = image.get_attribute('src') if image else None
                        if img_src and img_src.startswith('/'):
                            img_src = f"https://www.neptun-ks.com{img_src}"

                        results.append({
                            'platform': 'neptun',
                            'name': name.inner_text().strip(),
                            'price': float(price_clean) if price_clean else None,
                            'currency': 'EUR',
                            'url': full_url,
                            'image_url': img_src,
                            'in_stock': True,
                        })
                except Exception:
                    continue

        except Exception as e:
            print(f"Neptun scraper error: {e}")
        finally:
            browser.close()

    return results


if __name__ == '__main__':
    results = scrape_neptun('iphone')
    for r in results:
        print(r)