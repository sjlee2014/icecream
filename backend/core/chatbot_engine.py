"""
Chatbot logic for intent detection and response generation
"""
import re
from typing import Tuple, Optional
from backend.models.chatbot import FAQ
from sqlalchemy.orm import Session


class ChatbotEngine:
    """챗봇 엔진 - 의도 파악 및 자동 응답"""

    # 의도 키워드 매핑
    INTENT_KEYWORDS = {
        "greeting": ["안녕", "안녕하세요", "hi", "hello", "헬로", "반가"],
        "product": ["상품", "제품", "아이스크림", "종류", "맛", "가격", "얼마"],
        "order": ["주문", "구매", "결제", "구입", "살", "사고싶"],
        "shipping": ["배송", "배달", "언제", "도착", "배송비", "택배", "받"],
        "return": ["반품", "교환", "환불", "취소", "불량", "파손"],
        "business_hours": ["영업시간", "운영시간", "몇시", "시간", "언제"],
        "contact": ["연락", "전화", "이메일", "문의", "상담원", "직원"],
    }

    # 기본 응답 템플릿
    RESPONSES = {
        "greeting": "안녕하세요! {}입니다. 무엇을 도와드릴까요? 😊\n\n상품 문의, 주문, 배송, 반품/교환 등 궁금하신 점을 말씀해주세요!",
        "product": "상품에 대해 궁금하신 점이 있으시군요!\n\n구체적으로 어떤 상품이나 정보가 필요하신가요?\n예: 바닐라 아이스크림 가격, 베스트 상품 추천 등",
        "order": "주문을 원하시나요?\n\n웹사이트(www.i-screammall.co.kr)에서 직접 주문하실 수 있습니다.\n주문 과정에서 도움이 필요하시면 말씀해주세요!",
        "shipping": "배송 관련 문의시군요!\n\n• 배송 기간: 주문 후 2-3일\n• 배송비: 30,000원 이상 무료\n• 배송 지역: 전국 (일부 도서산간 제외)\n\n주문번호가 있으시면 배송 조회가 가능합니다.",
        "return": "반품/교환 문의시군요.\n\n• 수령 후 7일 이내 가능\n• 상품 미개봉/훼손 없을 것\n• 단순 변심: 왕복 배송비 고객 부담\n• 상품 불량: 무료 교환/환불\n\n구체적인 상황을 말씀해주시면 더 도와드리겠습니다!",
        "business_hours": "{}의 운영시간은 다음과 같습니다:\n\n⏰ {}\n📧 {}\n📞 {}\n\n상담원 연결은 운영시간 내에 가능합니다.",
        "contact": "연락처 안내:\n\n📞 고객센터: {}\n📧 이메일: {}\n⏰ 운영시간: {}\n\n무엇을 도와드릴까요?",
        "default": "죄송합니다. 질문을 정확히 이해하지 못했습니다. 😅\n\n다음 중 하나를 선택하시거나 구체적으로 말씀해주세요:\n\n1️⃣ 상품 문의\n2️⃣ 주문 방법\n3️⃣ 배송 문의\n4️⃣ 반품/교환\n5️⃣ 영업시간/연락처",
    }

    def __init__(self, business_name: str, business_hours: str, support_email: str, support_phone: str):
        self.business_name = business_name
        self.business_hours = business_hours
        self.support_email = support_email
        self.support_phone = support_phone

    def detect_intent(self, message: str) -> str:
        """메시지에서 의도를 파악"""
        message_lower = message.lower()

        # 각 의도별로 키워드 매칭
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent

        return "default"

    def generate_response(self, message: str, db: Session) -> Tuple[str, str]:
        """
        자동 응답 생성
        Returns: (response_text, detected_intent)
        """
        intent = self.detect_intent(message)

        # FAQ 검색 시도
        faq_response = self.search_faq(message, db)
        if faq_response:
            return faq_response, intent

        # 의도별 기본 응답
        response_template = self.RESPONSES.get(intent, self.RESPONSES["default"])

        # 템플릿에 비즈니스 정보 삽입
        if intent == "greeting":
            response = response_template.format(self.business_name)
        elif intent == "business_hours":
            response = response_template.format(
                self.business_name,
                self.business_hours,
                self.support_email,
                self.support_phone
            )
        elif intent == "contact":
            response = response_template.format(
                self.support_phone,
                self.support_email,
                self.business_hours
            )
        else:
            response = response_template

        return response, intent

    def search_faq(self, message: str, db: Session) -> Optional[str]:
        """FAQ에서 관련 답변 검색"""
        message_lower = message.lower()

        # 활성화된 FAQ만 검색
        faqs = db.query(FAQ).filter(FAQ.is_active == True).all()

        # 키워드 매칭
        for faq in faqs:
            keywords = faq.keywords.split(",") if faq.keywords else []
            question_words = faq.question.lower().split()

            # 키워드 또는 질문 내용과 매칭
            for keyword in keywords + question_words:
                if keyword.strip() and keyword.strip() in message_lower:
                    # 조회수 증가
                    faq.view_count += 1
                    db.commit()

                    return f"💡 FAQ에서 찾았습니다!\n\n❓ {faq.question}\n\n✅ {faq.answer}"

        return None

    def get_quick_replies(self) -> list:
        """빠른 응답 버튼 목록"""
        return [
            {"label": "📦 상품 문의", "value": "상품 문의"},
            {"label": "🛒 주문 방법", "value": "주문 방법"},
            {"label": "🚚 배송 조회", "value": "배송 조회"},
            {"label": "↩️ 반품/교환", "value": "반품 교환"},
            {"label": "⏰ 영업시간", "value": "영업시간"},
        ]
