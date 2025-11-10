from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Conversation(Base):
    """대화방 모델"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)

    # Customer info
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    customer_phone = Column(String, nullable=True)

    # Status
    status = Column(String, default="active")  # active, closed, waiting
    is_resolved = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone,
            "status": self.status,
            "is_resolved": self.is_resolved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }


class Message(Base):
    """메시지 모델"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    # Message content
    content = Column(Text, nullable=False)
    sender_type = Column(String, nullable=False)  # customer, bot, admin

    # Metadata
    is_read = Column(Boolean, default=False)
    intent = Column(String, nullable=True)  # product, order, shipping, return, etc.

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "sender_type": self.sender_type,
            "is_read": self.is_read,
            "intent": self.intent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class FAQ(Base):
    """FAQ 모델"""
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)

    # Content
    category = Column(String, nullable=False, index=True)  # 상품, 주문, 배송, 반품/교환, 기타
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    keywords = Column(Text, nullable=True)  # 검색을 위한 키워드 (쉼표로 구분)

    # Stats
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "question": self.question,
            "answer": self.answer,
            "keywords": self.keywords.split(",") if self.keywords else [],
            "view_count": self.view_count,
            "helpful_count": self.helpful_count,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
