import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.models.scrape_log import ScrapeLog
from backend.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IcecreamScraper:
    """
    Web scraper for i-screammall.co.kr using Playwright.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.base_url = settings.TARGET_URL
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def init_browser(self):
        """Initialize Playwright browser."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({"width": 1920, "height": 1080})

    async def close_browser(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()

    async def scrape_product_list(self, url: str = None) -> List[Dict]:
        """
        Scrape product list from a page.
        """
        if url is None:
            url = self.base_url

        logger.info(f"Scraping product list from: {url}")

        try:
            await self.page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for product elements to load
            # Note: These selectors will need to be adjusted based on actual site structure
            await asyncio.sleep(3)  # Give extra time for dynamic content

            products = []

            # Try to find product cards - common selectors for e-commerce sites
            # These selectors will need to be updated after inspecting the actual site
            product_selectors = [
                ".product-item",
                ".product-card",
                "[class*='product']",
                ".goods-list li",
                ".item-wrap",
            ]

            product_elements = None
            for selector in product_selectors:
                try:
                    product_elements = await self.page.query_selector_all(selector)
                    if product_elements and len(product_elements) > 0:
                        logger.info(f"Found {len(product_elements)} products with selector: {selector}")
                        break
                except Exception as e:
                    continue

            if not product_elements:
                logger.warning("No product elements found. Page structure may have changed.")
                # Save page content for debugging
                content = await self.page.content()
                with open("/home/user/icecream/data/debug_page.html", "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info("Saved page content to data/debug_page.html for debugging")
                return []

            for element in product_elements:
                try:
                    product_data = await self.extract_product_data(element)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    logger.error(f"Error extracting product data: {e}")
                    continue

            logger.info(f"Successfully scraped {len(products)} products")
            return products

        except Exception as e:
            logger.error(f"Error scraping product list: {e}")
            raise

    async def extract_product_data(self, element) -> Optional[Dict]:
        """
        Extract product data from a product element.
        """
        try:
            # Try to extract common e-commerce data
            # These will need to be adjusted based on actual site structure

            # Product name
            name = None
            name_selectors = [".product-name", ".goods-name", "[class*='name']", "h3", "h4"]
            for selector in name_selectors:
                try:
                    name_elem = await element.query_selector(selector)
                    if name_elem:
                        name = await name_elem.inner_text()
                        name = name.strip()
                        break
                except:
                    continue

            # Product link and ID
            product_url = None
            product_id = None
            link_elem = await element.query_selector("a")
            if link_elem:
                product_url = await link_elem.get_attribute("href")
                if product_url and not product_url.startswith("http"):
                    product_url = self.base_url.rstrip("/") + "/" + product_url.lstrip("/")
                # Extract ID from URL
                if product_url:
                    product_id = product_url.split("/")[-1] or product_url.split("/")[-2]

            # Price
            price = None
            price_selectors = [".price", ".product-price", "[class*='price']"]
            for selector in price_selectors:
                try:
                    price_elem = await element.query_selector(selector)
                    if price_elem:
                        price_text = await price_elem.inner_text()
                        # Extract numbers from price text
                        price_text = price_text.replace(",", "").replace("원", "").strip()
                        import re
                        price_match = re.search(r"(\d+)", price_text)
                        if price_match:
                            price = float(price_match.group(1))
                            break
                except:
                    continue

            # Image
            image_url = None
            img_elem = await element.query_selector("img")
            if img_elem:
                image_url = await img_elem.get_attribute("src")
                if image_url and not image_url.startswith("http"):
                    image_url = self.base_url.rstrip("/") + "/" + image_url.lstrip("/")

            # Only return if we have at least a name
            if name:
                return {
                    "product_id": product_id or f"unknown_{hash(name)}",
                    "name": name,
                    "price": price,
                    "image_url": image_url,
                    "url": product_url,
                }

            return None

        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
            return None

    async def scrape_product_detail(self, product_url: str) -> Dict:
        """
        Scrape detailed information from a product page.
        """
        logger.info(f"Scraping product detail: {product_url}")

        try:
            await self.page.goto(product_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # Extract detailed information
            # These selectors need to be adjusted based on actual site

            detail_data = {
                "description": None,
                "category": None,
                "specifications": {},
                "images": [],
            }

            # Description
            try:
                desc_elem = await self.page.query_selector(".product-description, .detail-info")
                if desc_elem:
                    detail_data["description"] = await desc_elem.inner_text()
            except:
                pass

            # Additional images
            try:
                img_elements = await self.page.query_selector_all(".product-images img, .detail-images img")
                for img in img_elements:
                    img_src = await img.get_attribute("src")
                    if img_src:
                        detail_data["images"].append(img_src)
            except:
                pass

            return detail_data

        except Exception as e:
            logger.error(f"Error scraping product detail: {e}")
            return {}

    async def scrape_all_products(self, db: Session, scrape_detail: bool = False) -> ScrapeLog:
        """
        Main scraping function that scrapes all products and saves to database.
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

            # Scrape main page products
            products_data = await self.scrape_product_list()

            # Try to find and scrape category pages
            # This is a placeholder - actual implementation will depend on site structure
            try:
                category_links = await self.page.query_selector_all("a[href*='category'], .category-link")
                logger.info(f"Found {len(category_links)} category links")

                for link in category_links[:5]:  # Limit to first 5 categories for now
                    try:
                        url = await link.get_attribute("href")
                        if url and not url.startswith("http"):
                            url = self.base_url.rstrip("/") + "/" + url.lstrip("/")
                        if url:
                            category_products = await self.scrape_product_list(url)
                            products_data.extend(category_products)
                    except Exception as e:
                        logger.error(f"Error scraping category: {e}")
                        continue
            except Exception as e:
                logger.warning(f"Could not scrape category pages: {e}")

            # Remove duplicates based on product_id
            unique_products = {p["product_id"]: p for p in products_data}
            products_data = list(unique_products.values())

            logger.info(f"Total unique products found: {len(products_data)}")

            # Save to database
            new_count = 0
            updated_count = 0

            for product_data in products_data:
                try:
                    existing_product = db.query(Product).filter(
                        Product.product_id == product_data["product_id"]
                    ).first()

                    if existing_product:
                        # Update existing product
                        for key, value in product_data.items():
                            setattr(existing_product, key, value)
                        existing_product.last_scraped_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new product
                        new_product = Product(**product_data)
                        db.add(new_product)
                        new_count += 1

                    db.commit()

                except Exception as e:
                    logger.error(f"Error saving product {product_data.get('product_id')}: {e}")
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

            logger.info(
                f"Scraping completed: {new_count} new, {updated_count} updated, "
                f"{len(products_data)} total products"
            )

            return scrape_log

        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            scrape_log.status = "failed"
            scrape_log.error_message = str(e)
            scrape_log.completed_at = datetime.utcnow()
            db.add(scrape_log)
            db.commit()
            raise

        finally:
            await self.close_browser()


async def run_scraper(db: Session):
    """
    Convenience function to run the scraper.
    """
    scraper = IcecreamScraper(headless=settings.SCRAPER_HEADLESS)
    return await scraper.scrape_all_products(db)
