from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from pydantic import BaseModel
import uuid

from backend.core.database import get_db
from backend.models.chatbot import Conversation, Message
from backend.core.chatbot_engine import ChatbotEngine
from backend.core.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize chatbot engine
chatbot = ChatbotEngine(
    business_name=settings.BUSINESS_NAME,
    business_hours=settings.BUSINESS_HOURS,
    support_email=settings.SUPPORT_EMAIL,
    support_phone=settings.SUPPORT_PHONE,
)


# Pydantic schemas
class MessageCreate(BaseModel):
    content: str
    session_id: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    content: str
    sender_type: str
    created_at: str

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    session_id: str
    customer_name: str | None
    status: str
    created_at: str
    message_count: int

    class Config:
        from_attributes = True


@router.post("/start")
def start_conversation(db: Session = Depends(get_db)):
    """
    새로운 대화 시작
    """
    session_id = str(uuid.uuid4())

    conversation = Conversation(session_id=session_id, status="active")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # 환영 메시지 자동 전송
    welcome_message = Message(
        conversation_id=conversation.id,
        content=f"안녕하세요! {settings.BUSINESS_NAME}입니다. 무엇을 도와드릴까요? 😊",
        sender_type="bot",
    )
    db.add(welcome_message)
    db.commit()

    return {
        "session_id": session_id,
        "conversation_id": conversation.id,
        "message": "대화가 시작되었습니다",
        "quick_replies": chatbot.get_quick_replies(),
    }


@router.post("/message")
def send_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    """
    메시지 전송 및 자동 응답
    """
    # 대화방 찾기
    conversation = db.query(Conversation).filter(
        Conversation.session_id == message_data.session_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")

    # 사용자 메시지 저장
    user_message = Message(
        conversation_id=conversation.id,
        content=message_data.content,
        sender_type="customer",
    )
    db.add(user_message)
    db.commit()

    # 챗봇 응답 생성
    bot_response, detected_intent = chatbot.generate_response(message_data.content, db)

    # 봇 응답 저장
    bot_message = Message(
        conversation_id=conversation.id,
        content=bot_response,
        sender_type="bot",
        intent=detected_intent,
    )
    db.add(bot_message)

    # 대화 업데이트 시간 갱신
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(bot_message)

    return {
        "user_message": user_message.to_dict(),
        "bot_message": bot_message.to_dict(),
        "quick_replies": chatbot.get_quick_replies(),
    }


@router.get("/history/{session_id}")
def get_conversation_history(session_id: str, db: Session = Depends(get_db)):
    """
    대화 내역 조회
    """
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    return {
        "conversation": conversation.to_dict(),
        "messages": [msg.to_dict() for msg in messages],
    }


@router.get("/conversations")
def get_all_conversations(
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    """
    모든 대화 목록 조회 (관리자용)
    """
    query = db.query(Conversation)

    if status:
        query = query.filter(Conversation.status == status)

    conversations = query.order_by(desc(Conversation.updated_at)).limit(limit).all()

    result = []
    for conv in conversations:
        message_count = db.query(Message).filter(Message.conversation_id == conv.id).count()
        conv_dict = conv.to_dict()
        conv_dict["message_count"] = message_count
        result.append(conv_dict)

    return result


@router.post("/close/{session_id}")
def close_conversation(session_id: str, db: Session = Depends(get_db)):
    """
    대화 종료
    """
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")

    conversation.status = "closed"
    conversation.closed_at = datetime.utcnow()
    db.commit()

    return {"message": "대화가 종료되었습니다"}


# WebSocket for real-time chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    실시간 채팅을 위한 WebSocket 엔드포인트
    """
    await manager.connect(websocket, session_id)

    try:
        while True:
            # 클라이언트로부터 메시지 받기
            data = await websocket.receive_json()

            # 여기서 메시지 처리 및 응답
            # (실제로는 위의 send_message 함수를 재사용)

            await websocket.send_json({
                "type": "message",
                "content": "서버에서 받았습니다",
                "timestamp": datetime.utcnow().isoformat(),
            })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
