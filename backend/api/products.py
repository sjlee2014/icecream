from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from backend.core.database import get_db
from backend.models.product import Product
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/products", tags=["products"])


# Pydantic schemas
class ProductResponse(BaseModel):
    id: int
    product_id: str
    name: str
    category: Optional[str]
    price: Optional[float]
    original_price: Optional[float]
    discount_rate: Optional[float]
    description: Optional[str]
    image_url: Optional[str]
    is_available: bool
    is_new: bool
    is_best: bool
    is_sale: bool
    view_count: int
    sales_count: int
    review_count: int
    rating: float
    url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_scraped_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProductStats(BaseModel):
    total_products: int
    available_products: int
    new_products: int
    best_products: int
    sale_products: int
    categories: List[dict]
    avg_price: float
    avg_discount_rate: float


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    category: Optional[str] = None,
    is_new: Optional[bool] = None,
    is_best: Optional[bool] = None,
    is_sale: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|price|rating|sales_count|name)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """
    Get products with filtering, searching, and sorting.
    """
    query = db.query(Product)

    # Filters
    if category:
        query = query.filter(Product.category == category)
    if is_new is not None:
        query = query.filter(Product.is_new == is_new)
    if is_best is not None:
        query = query.filter(Product.is_best == is_best)
    if is_sale is not None:
        query = query.filter(Product.is_sale == is_sale)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Sorting
    sort_column = getattr(Product, sort_by)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/stats", response_model=ProductStats)
def get_product_stats(db: Session = Depends(get_db)):
    """
    Get overall product statistics.
    """
    total = db.query(Product).count()
    available = db.query(Product).filter(Product.is_available == True).count()
    new = db.query(Product).filter(Product.is_new == True).count()
    best = db.query(Product).filter(Product.is_best == True).count()
    sale = db.query(Product).filter(Product.is_sale == True).count()

    # Category breakdown
    categories = (
        db.query(Product.category, func.count(Product.id).label("count"))
        .filter(Product.category.isnot(None))
        .group_by(Product.category)
        .all()
    )
    category_list = [{"name": cat, "count": count} for cat, count in categories]

    # Average price
    avg_price_result = db.query(func.avg(Product.price)).filter(Product.price.isnot(None)).scalar()
    avg_price = float(avg_price_result) if avg_price_result else 0.0

    # Average discount
    avg_discount_result = (
        db.query(func.avg(Product.discount_rate)).filter(Product.discount_rate.isnot(None)).scalar()
    )
    avg_discount = float(avg_discount_result) if avg_discount_result else 0.0

    return ProductStats(
        total_products=total,
        available_products=available,
        new_products=new,
        best_products=best,
        sale_products=sale,
        categories=category_list,
        avg_price=avg_price,
        avg_discount_rate=avg_discount,
    )


@router.get("/trending", response_model=List[ProductResponse])
def get_trending_products(
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db),
):
    """
    Get trending products based on sales, views, and ratings.
    """
    # Calculate trending score: (sales_count * 2) + view_count + (rating * 10)
    products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .order_by(
            desc(
                (Product.sales_count * 2)
                + Product.view_count
                + (Product.rating * 10)
            )
        )
        .limit(limit)
        .all()
    )
    return products


@router.get("/best-sellers", response_model=List[ProductResponse])
def get_best_sellers(
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db),
):
    """
    Get best selling products.
    """
    products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .order_by(desc(Product.sales_count))
        .limit(limit)
        .all()
    )
    return products


@router.get("/new-arrivals", response_model=List[ProductResponse])
def get_new_arrivals(
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db),
):
    """
    Get newly added products.
    """
    products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .filter(Product.is_new == True)
        .order_by(desc(Product.created_at))
        .limit(limit)
        .all()
    )
    return products


@router.get("/on-sale", response_model=List[ProductResponse])
def get_on_sale(
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db),
):
    """
    Get products on sale.
    """
    products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .filter(Product.is_sale == True)
        .order_by(desc(Product.discount_rate))
        .limit(limit)
        .all()
    )
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """
    Get a specific product by ID.
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
