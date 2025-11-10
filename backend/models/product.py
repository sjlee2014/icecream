from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from backend.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Product identifiers
    product_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    category = Column(String, index=True)

    # Product details
    price = Column(Float)
    original_price = Column(Float, nullable=True)
    discount_rate = Column(Float, nullable=True)
    description = Column(Text, nullable=True)

    # Images
    image_url = Column(String, nullable=True)
    images = Column(JSON, nullable=True)  # List of additional images

    # Status and metrics
    is_available = Column(Boolean, default=True)
    is_new = Column(Boolean, default=False)
    is_best = Column(Boolean, default=False)
    is_sale = Column(Boolean, default=False)

    # Popularity metrics
    view_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)
    review_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)

    # Additional data
    tags = Column(JSON, nullable=True)  # List of tags
    specifications = Column(JSON, nullable=True)  # Product specs
    url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Product {self.product_id}: {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "original_price": self.original_price,
            "discount_rate": self.discount_rate,
            "description": self.description,
            "image_url": self.image_url,
            "images": self.images,
            "is_available": self.is_available,
            "is_new": self.is_new,
            "is_best": self.is_best,
            "is_sale": self.is_sale,
            "view_count": self.view_count,
            "sales_count": self.sales_count,
            "review_count": self.review_count,
            "rating": self.rating,
            "tags": self.tags,
            "specifications": self.specifications,
            "url": self.url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_scraped_at": self.last_scraped_at.isoformat() if self.last_scraped_at else None,
        }
