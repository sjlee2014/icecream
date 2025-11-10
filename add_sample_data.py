"""
Add sample product data to demonstrate the system
"""
from datetime import datetime
from backend.core.database import SessionLocal, init_db
from backend.models.product import Product
from backend.models.scrape_log import ScrapeLog

# Initialize database
init_db()

db = SessionLocal()

# Sample products data
sample_products = [
    {
        "product_id": "p001",
        "name": "바닐라 아이스크림 1L",
        "category": "아이스크림",
        "price": 8900,
        "original_price": 12000,
        "discount_rate": 25.8,
        "image_url": "https://via.placeholder.com/250x200?text=Vanilla+Ice+Cream",
        "is_new": True,
        "is_best": True,
        "sales_count": 245,
        "view_count": 1520,
        "review_count": 89,
        "rating": 4.8,
    },
    {
        "product_id": "p002",
        "name": "초코 아이스크림 500ml",
        "category": "아이스크림",
        "price": 5500,
        "original_price": 7000,
        "discount_rate": 21.4,
        "image_url": "https://via.placeholder.com/250x200?text=Chocolate+Ice+Cream",
        "is_best": True,
        "sales_count": 312,
        "view_count": 2100,
        "review_count": 124,
        "rating": 4.9,
    },
    {
        "product_id": "p003",
        "name": "딸기 셔벗 750ml",
        "category": "셔벗",
        "price": 6800,
        "is_new": True,
        "is_sale": True,
        "sales_count": 156,
        "view_count": 890,
        "review_count": 45,
        "rating": 4.6,
    },
    {
        "product_id": "p004",
        "name": "망고 빙수 세트",
        "category": "빙수",
        "price": 15900,
        "original_price": 19900,
        "discount_rate": 20.1,
        "image_url": "https://via.placeholder.com/250x200?text=Mango+Bingsu",
        "is_new": True,
        "sales_count": 89,
        "view_count": 670,
        "review_count": 34,
        "rating": 4.7,
    },
    {
        "product_id": "p005",
        "name": "민트초코 아이스크림",
        "category": "아이스크림",
        "price": 7200,
        "image_url": "https://via.placeholder.com/250x200?text=Mint+Chocolate",
        "is_best": True,
        "sales_count": 198,
        "view_count": 1340,
        "review_count": 76,
        "rating": 4.5,
    },
    {
        "product_id": "p006",
        "name": "녹차 아이스크림 파인트",
        "category": "아이스크림",
        "price": 8500,
        "original_price": 10000,
        "discount_rate": 15.0,
        "is_sale": True,
        "sales_count": 134,
        "view_count": 950,
        "review_count": 52,
        "rating": 4.4,
    },
    {
        "product_id": "p007",
        "name": "커피 아이스크림 1L",
        "category": "아이스크림",
        "price": 9800,
        "is_best": True,
        "sales_count": 267,
        "view_count": 1780,
        "review_count": 98,
        "rating": 4.7,
    },
    {
        "product_id": "p008",
        "name": "쿠키앤크림 아이스크림",
        "category": "아이스크림",
        "price": 7900,
        "original_price": 9900,
        "discount_rate": 20.2,
        "image_url": "https://via.placeholder.com/250x200?text=Cookies+and+Cream",
        "is_new": True,
        "is_sale": True,
        "sales_count": 223,
        "view_count": 1450,
        "review_count": 87,
        "rating": 4.8,
    },
    {
        "product_id": "p009",
        "name": "레몬 셔벗 500ml",
        "category": "셔벗",
        "price": 5900,
        "is_new": True,
        "sales_count": 98,
        "view_count": 560,
        "review_count": 28,
        "rating": 4.3,
    },
    {
        "product_id": "p010",
        "name": "팥빙수 세트",
        "category": "빙수",
        "price": 12900,
        "original_price": 15900,
        "discount_rate": 18.9,
        "is_sale": True,
        "sales_count": 178,
        "view_count": 1120,
        "review_count": 64,
        "rating": 4.6,
    },
    {
        "product_id": "p011",
        "name": "블루베리 요거트 아이스크림",
        "category": "아이스크림",
        "price": 8200,
        "is_best": True,
        "sales_count": 189,
        "view_count": 1290,
        "review_count": 71,
        "rating": 4.7,
    },
    {
        "product_id": "p012",
        "name": "카라멜 마키아토 아이스크림",
        "category": "아이스크림",
        "price": 8900,
        "original_price": 11900,
        "discount_rate": 25.2,
        "image_url": "https://via.placeholder.com/250x200?text=Caramel+Macchiato",
        "is_new": True,
        "is_sale": True,
        "sales_count": 156,
        "view_count": 980,
        "review_count": 58,
        "rating": 4.8,
    },
]

try:
    # Add products
    for product_data in sample_products:
        product = Product(**product_data)
        db.add(product)

    # Add scrape log
    scrape_log = ScrapeLog(
        status="success",
        products_scraped=len(sample_products),
        products_new=len(sample_products),
        products_updated=0,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
        duration_seconds=5.2,
    )
    db.add(scrape_log)

    db.commit()
    print(f"✅ Successfully added {len(sample_products)} sample products!")

except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
