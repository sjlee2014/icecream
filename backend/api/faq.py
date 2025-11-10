from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from pydantic import BaseModel

from backend.core.database import get_db
from backend.models.chatbot import FAQ

router = APIRouter(prefix="/faq", tags=["faq"])


# Pydantic schemas
class FAQCreate(BaseModel):
    category: str
    question: str
    answer: str
    keywords: str | None = None


class FAQUpdate(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    keywords: str | None = None
    is_active: bool | None = None


class FAQResponse(BaseModel):
    id: int
    category: str
    question: str
    answer: str
    keywords: List[str]
    view_count: int
    helpful_count: int
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[FAQResponse])
def get_faqs(
    category: str | None = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """
    FAQ 목록 조회
    """
    query = db.query(FAQ).filter(FAQ.is_active == is_active)

    if category:
        query = query.filter(FAQ.category == category)

    faqs = query.order_by(desc(FAQ.view_count)).all()

    return [
        {
            **faq.to_dict(),
            "keywords": faq.keywords.split(",") if faq.keywords else []
        }
        for faq in faqs
    ]


@router.get("/categories")
def get_faq_categories(db: Session = Depends(get_db)):
    """
    FAQ 카테고리 목록
    """
    categories = db.query(FAQ.category).distinct().all()
    return [cat[0] for cat in categories]


@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    """
    특정 FAQ 조회
    """
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    # 조회수 증가
    faq.view_count += 1
    db.commit()

    return {
        **faq.to_dict(),
        "keywords": faq.keywords.split(",") if faq.keywords else []
    }


@router.post("/", response_model=FAQResponse)
def create_faq(faq_data: FAQCreate, db: Session = Depends(get_db)):
    """
    새 FAQ 생성 (관리자용)
    """
    faq = FAQ(**faq_data.model_dump())
    db.add(faq)
    db.commit()
    db.refresh(faq)

    return {
        **faq.to_dict(),
        "keywords": faq.keywords.split(",") if faq.keywords else []
    }


@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(faq_id: int, faq_data: FAQUpdate, db: Session = Depends(get_db)):
    """
    FAQ 수정 (관리자용)
    """
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    update_data = faq_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(faq, key, value)

    db.commit()
    db.refresh(faq)

    return {
        **faq.to_dict(),
        "keywords": faq.keywords.split(",") if faq.keywords else []
    }


@router.delete("/{faq_id}")
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    """
    FAQ 삭제 (관리자용)
    """
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    db.delete(faq)
    db.commit()

    return {"message": "FAQ가 삭제되었습니다"}


@router.post("/{faq_id}/helpful")
def mark_helpful(faq_id: int, db: Session = Depends(get_db)):
    """
    FAQ 도움됨 표시
    """
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    faq.helpful_count += 1
    db.commit()

    return {"message": "도움이 되었다는 의견이 반영되었습니다"}


@router.get("/search/{keyword}")
def search_faqs(keyword: str, db: Session = Depends(get_db)):
    """
    FAQ 검색
    """
    faqs = db.query(FAQ).filter(
        FAQ.is_active == True,
        (FAQ.question.contains(keyword) | FAQ.keywords.contains(keyword))
    ).all()

    return [
        {
            **faq.to_dict(),
            "keywords": faq.keywords.split(",") if faq.keywords else []
        }
        for faq in faqs
    ]
