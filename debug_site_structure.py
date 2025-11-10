"""
Debug script to analyze the actual rendered HTML structure of i-screammall.co.kr
"""
import asyncio
from playwright.async_api import async_playwright

async def analyze_site():
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set viewport
        await page.set_viewport_size({"width": 1920, "height": 1080})

        print("📡 Loading homepage...")
        try:
            await page.goto("https://i-screammall.co.kr/", wait_until="networkidle", timeout=60000)
            print("✅ Page loaded!")

            # Wait a bit more for dynamic content
            await asyncio.sleep(5)

            # Get page content
            content = await page.content()

            # Save full HTML
            print("💾 Saving full HTML...")
            with open("data/site_full.html", "w", encoding="utf-8") as f:
                f.write(content)

            # Try to find product elements with various selectors
            print("\n🔍 Searching for product elements...")

            selectors_to_try = [
                "div[class*='product']",
                "div[class*='item']",
                "div[class*='goods']",
                "article",
                "li[class*='product']",
                "a[href*='product']",
                "a[href*='goods']",
                ".product-item",
                ".goods-item",
                "[data-product]",
            ]

            found_elements = []
            for selector in selectors_to_try:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        print(f"  ✓ Found {len(elements)} elements with selector: {selector}")
                        found_elements.append((selector, len(elements)))

                        # Get HTML of first element
                        if len(elements) > 0:
                            first_html = await elements[0].inner_html()
                            print(f"    First element preview: {first_html[:200]}...")
                except Exception as e:
                    pass

            # Try to find links
            print("\n🔗 Checking for navigation links...")
            links = await page.query_selector_all("a")
            print(f"  Found {len(links)} total links")

            product_links = []
            for link in links[:50]:  # Check first 50 links
                href = await link.get_attribute("href")
                text = await link.inner_text()
                if href and any(keyword in href.lower() for keyword in ['product', 'goods', 'item', 'detail']):
                    product_links.append((text.strip(), href))

            if product_links:
                print(f"\n  📦 Found {len(product_links)} potential product links:")
                for text, href in product_links[:10]:
                    print(f"    - {text[:30]}: {href}")

            # Check for images
            print("\n🖼️ Checking for product images...")
            images = await page.query_selector_all("img")
            print(f"  Found {len(images)} total images")

            # Take screenshot
            print("\n📸 Taking screenshot...")
            await page.screenshot(path="data/site_screenshot.png", full_page=False)

            # Get main content area
            print("\n📝 Extracting main content area...")
            main_selectors = ["main", "#main", ".main", "#content", ".content", "body"]
            for selector in main_selectors:
                try:
                    main_element = await page.query_selector(selector)
                    if main_element:
                        main_html = await main_element.inner_html()
                        print(f"  ✓ Found main content with selector: {selector}")
                        with open("data/main_content.html", "w", encoding="utf-8") as f:
                            f.write(main_html)
                        break
                except:
                    pass

            # Try to find any text that looks like product names or prices
            print("\n💰 Looking for price patterns...")
            text_content = await page.inner_text("body")

            # Look for Korean won prices
            import re
            prices = re.findall(r'(\d{1,3}(?:,\d{3})*)\s*원', text_content)
            if prices:
                print(f"  Found {len(prices)} price mentions")
                print(f"  Sample prices: {prices[:5]}")

            print("\n✅ Analysis complete!")
            print("📁 Files saved:")
            print("  - data/site_full.html (full page HTML)")
            print("  - data/main_content.html (main content area)")
            print("  - data/site_screenshot.png (screenshot)")

            if found_elements:
                print("\n💡 Recommended selectors to try:")
                for selector, count in sorted(found_elements, key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {selector} ({count} elements)")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(analyze_site())
