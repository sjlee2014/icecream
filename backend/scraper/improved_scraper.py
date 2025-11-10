import asyncio
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.models.scrape_log import ScrapeLog
from backend.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovedIcecreamScraper:
    """
    Improved web scraper for i-screammall.co.kr with better selector handling
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.base_url = settings.TARGET_URL
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def init_browser(self):
        """Initialize Playwright browser with proper settings"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-dev-shm-usage', '--no-sandbox']
        )

        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=settings.SCRAPER_USER_AGENT,
        )

        self.page = await context.new_page()

        # Set default timeout
        self.page.set_default_timeout(30000)

    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

    def extract_price(self, text: str) -> Optional[float]:
        """Extract price from Korean text"""
        if not text:
            return None

        # Remove commas and extract numbers
        text = text.replace(',', '').replace('원', '').strip()

        # Try to find number pattern
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def extract_discount_rate(self, text: str) -> Optional[float]:
        """Extract discount rate from text"""
        if not text:
            return None

        # Look for percentage pattern
        match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    async def wait_for_content(self):
        """Wait for dynamic content to load"""
        try:
            # Wait for common shopping mall elements
            await self.page.wait_for_selector('img', timeout=10000)
            await asyncio.sleep(3)  # Additional wait for lazy loading
        except Exception as e:
            logger.warning(f"Timeout waiting for content: {e}")

    async def scrape_product_list(self, url: str = None) -> List[Dict]:
        """
        Scrape product list from a page using multiple selector strategies
        """
        if url is None:
            url = self.base_url

        logger.info(f"Scraping product list from: {url}")

        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await self.wait_for_content()

            # Save page for debugging
            content = await self.page.content()
            with open("/home/user/icecream/data/debug_page.html", "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Saved page content to data/debug_page.html")

            # Take screenshot for debugging
            await self.page.screenshot(path="/home/user/icecream/data/debug_screenshot.png")
            logger.info("Saved screenshot to data/debug_screenshot.png")

            products = []

            # Strategy 1: Try common Korean shopping mall selectors
            selectors_to_try = [
                # Common shopping mall patterns
                "li.product-item, li.goods-item, li[class*='product'], li[class*='goods']",
                "div.product-card, div.goods-card, div[class*='product-'], div[class*='goods-']",
                "article[class*='product'], article[class*='goods']",

                # More generic patterns
                "a[href*='/product/'], a[href*='/goods/'], a[href*='detail']",

                # Grid/list patterns
                ".product-list > *, .goods-list > *, .item-list > *",
                "[data-product-id], [data-goods-id]",

                # Fallback to any link with images
                "a:has(img)",
            ]

            product_elements = []
            used_selector = None

            for selector in selectors_to_try:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) > 5:  # Reasonable number of products
                        logger.info(f"✓ Found {len(elements)} products with: {selector}")
                        product_elements = elements
                        used_selector = selector
                        break
                except Exception as e:
                    continue

            if not product_elements:
                logger.warning("Could not find product elements with any selector")

                # Last resort: look for any links with images and prices
                logger.info("Trying fallback strategy...")
                all_links = await self.page.query_selector_all("a")

                for link in all_links[:100]:  # Check first 100 links
                    try:
                        # Check if link has image and price-like text
                        has_img = await link.query_selector("img")
                        text = await link.inner_text()

                        if has_img and ('원' in text or ',' in text):
                            product_elements.append(link)
                    except:
                        continue

                if product_elements:
                    logger.info(f"✓ Found {len(product_elements)} products with fallback strategy")

            # Extract product data
            for idx, element in enumerate(product_elements[:50]):  # Limit to 50 products
                try:
                    product_data = await self.extract_product_data_improved(element, idx)
                    if product_data and product_data.get('name'):
                        products.append(product_data)
                except Exception as e:
                    logger.error(f"Error extracting product {idx}: {e}")
                    continue

            logger.info(f"Successfully scraped {len(products)} products")
            return products

        except Exception as e:
            logger.error(f"Error scraping product list: {e}")
            import traceback
            traceback.print_exc()
            raise

    async def extract_product_data_improved(self, element, idx: int) -> Optional[Dict]:
        """
        Extract product data with improved strategies
        """
        try:
            data = {
                'product_id': None,
                'name': None,
                'price': None,
                'original_price': None,
                'discount_rate': None,
                'image_url': None,
                'url': None,
                'category': None,
            }

            # Extract product URL and ID
            try:
                # Try to get href
                href = await element.get_attribute('href')
                if not href:
                    link = await element.query_selector('a')
                    if link:
                        href = await link.get_attribute('href')

                if href:
                    if not href.startswith('http'):
                        href = self.base_url.rstrip('/') + '/' + href.lstrip('/')
                    data['url'] = href

                    # Extract ID from URL
                    id_match = re.search(r'[\?&](?:product_no|goods_no|no|id)=(\d+)', href)
                    if id_match:
                        data['product_id'] = f"prod_{id_match.group(1)}"
                    else:
                        # Use last segment of URL
                        parts = href.rstrip('/').split('/')
                        if parts:
                            data['product_id'] = f"prod_{parts[-1]}_{idx}"
                else:
                    data['product_id'] = f"prod_unknown_{idx}"
            except Exception as e:
                data['product_id'] = f"prod_unknown_{idx}"

            # Extract product name
            name_selectors = [
                '.product-name, .goods-name, .prd-name, .item-name',
                '[class*="name"]',
                'h3, h4, h5',
                'strong',
                'p',
            ]

            for selector in name_selectors:
                try:
                    name_elem = await element.query_selector(selector)
                    if name_elem:
                        name = await name_elem.inner_text()
                        name = name.strip()
                        if len(name) > 3 and len(name) < 200:  # Reasonable name length
                            data['name'] = name
                            break
                except:
                    continue

            # If no name found, try getting all text
            if not data['name']:
                try:
                    text = await element.inner_text()
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    # First substantial line is probably the name
                    for line in lines:
                        if len(line) > 3 and len(line) < 200 and not re.match(r'^[\d,\s원%]+$', line):
                            data['name'] = line
                            break
                except:
                    pass

            # Extract price
            price_selectors = [
                '.price, .goods-price, .product-price, .prd-price',
                '[class*="price"]',
                'span strong, strong span',
            ]

            price_found = False
            for selector in price_selectors:
                try:
                    price_elem = await element.query_selector(selector)
                    if price_elem:
                        price_text = await price_elem.inner_text()
                        price = self.extract_price(price_text)
                        if price:
                            data['price'] = price
                            price_found = True
                            break
                except:
                    continue

            # If no price found, scan all text
            if not price_found:
                try:
                    text = await element.inner_text()
                    prices = re.findall(r'(\d{1,3}(?:,\d{3})+)\s*원', text)
                    if prices:
                        # First price is usually current price
                        price = self.extract_price(prices[0])
                        if price:
                            data['price'] = price

                        # Second price might be original price
                        if len(prices) > 1:
                            orig_price = self.extract_price(prices[1])
                            if orig_price and orig_price > price:
                                data['original_price'] = orig_price
                                data['discount_rate'] = round((1 - price / orig_price) * 100, 1)
                except:
                    pass

            # Extract image
            img_selectors = ['img', 'img[src]']
            for selector in img_selectors:
                try:
                    img_elem = await element.query_selector(selector)
                    if img_elem:
                        img_url = await img_elem.get_attribute('src')
                        if not img_url:
                            img_url = await img_elem.get_attribute('data-src')

                        if img_url:
                            if not img_url.startswith('http'):
                                img_url = self.base_url.rstrip('/') + '/' + img_url.lstrip('/')
                            data['image_url'] = img_url
                            break
                except:
                    continue

            # Only return if we have at least a name
            if data['name']:
                return data

            return None

        except Exception as e:
            logger.error(f"Error in extract_product_data_improved: {e}")
            return None

    async def scrape_all_products(self, db: Session) -> ScrapeLog:
        """
        Main scraping function
        """
        started_at = datetime.utcnow()
        scrape_log = ScrapeLog(
            status="running",
            started_at=started_at,
            products_scraped=0,
            products_new=0,
            products_updated=0,
        )

        try:
            await self.init_browser()
            logger.info("Browser initialized")

            # Scrape main page
            products_data = await self.scrape_product_list()

            logger.info(f"Total products scraped: {len(products_data)}")

            # Save to database
            new_count = 0
            updated_count = 0

            for product_data in products_data:
                try:
                    existing_product = db.query(Product).filter(
                        Product.product_id == product_data['product_id']
                    ).first()

                    if existing_product:
                        # Update
                        for key, value in product_data.items():
                            if value is not None:
                                setattr(existing_product, key, value)
                        existing_product.last_scraped_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new
                        new_product = Product(**product_data)
                        db.add(new_product)
                        new_count += 1

                    db.commit()

                except Exception as e:
                    logger.error(f"Error saving product: {e}")
                    db.rollback()
                    continue

            # Update scrape log
            completed_at = datetime.utcnow()
            scrape_log.status = "success"
            scrape_log.completed_at = completed_at
            scrape_log.duration_seconds = (completed_at - started_at).total_seconds()
            scrape_log.products_scraped = len(products_data)
            scrape_log.products_new = new_count
            scrape_log.products_updated = updated_count

            db.add(scrape_log)
            db.commit()

            logger.info(f"✅ Scraping completed: {new_count} new, {updated_count} updated")
            return scrape_log

        except Exception as e:
            logger.error(f"❌ Scraping failed: {e}")
            scrape_log.status = "failed"
            scrape_log.error_message = str(e)
            scrape_log.completed_at = datetime.utcnow()
            db.add(scrape_log)
            db.commit()
            raise

        finally:
            await self.close_browser()


async def run_improved_scraper(db: Session):
    """
    Run the improved scraper
    """
    scraper = ImprovedIcecreamScraper(headless=settings.SCRAPER_HEADLESS)
    return await scraper.scrape_all_products(db)
