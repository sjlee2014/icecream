"""
샘플 FAQ 데이터 초기화
"""
from backend.core.database import SessionLocal, init_db
from backend.models.chatbot import FAQ

# 데이터베이스 초기화
init_db()

db = SessionLocal()

# 샘플 FAQ 데이터
sample_faqs = [
    {
        "category": "상품",
        "question": "어떤 상품들을 판매하나요?",
        "answer": "저희는 다양한 아이스크림, 빙수, 셔벗 등을 판매하고 있습니다.\n\n인기 상품:\n• 바닐라 아이스크림\n• 초코 아이스크림\n• 딸기 셔벗\n• 망고 빙수 세트\n\n자세한 상품 목록은 웹사이트에서 확인하실 수 있습니다!",
        "keywords": "상품,제품,아이스크림,종류,판매",
    },
    {
        "category": "상품",
        "question": "상품 가격은 얼마인가요?",
        "answer": "상품별로 가격이 다릅니다.\n\n가격대:\n• 아이스크림: 5,500원 ~ 9,800원\n• 빙수 세트: 12,900원 ~ 15,900원\n• 셔벗: 5,900원 ~ 6,800원\n\n할인 행사 중인 상품도 있으니 웹사이트를 확인해주세요!",
        "keywords": "가격,얼마,비용",
    },
    {
        "category": "주문",
        "question": "주문은 어떻게 하나요?",
        "answer": "주문 방법은 간단합니다!\n\n1️⃣ 웹사이트(www.i-screammall.co.kr) 접속\n2️⃣ 원하시는 상품을 장바구니에 담기\n3️⃣ 주문/결제 진행\n4️⃣ 주문 완료!\n\n회원가입 후 이용하시면 다양한 혜택을 받으실 수 있습니다.",
        "keywords": "주문,구매,결제,방법",
    },
    {
        "category": "주문",
        "question": "최소 주문 금액이 있나요?",
        "answer": "최소 주문 금액은 없습니다! 원하시는 만큼 주문하실 수 있습니다.\n\n💡 Tip: 30,000원 이상 주문 시 배송비가 무료입니다!",
        "keywords": "최소주문,금액,얼마",
    },
    {
        "category": "배송",
        "question": "배송 기간은 얼마나 걸리나요?",
        "answer": "배송 기간 안내:\n\n• 일반 배송: 주문 후 2-3일\n• 제주/도서산간: 3-5일\n• 콜드체인 배송으로 신선하게 배송됩니다\n\n주문 폭주 시 배송이 지연될 수 있습니다.",
        "keywords": "배송,기간,언제,도착,걸리",
    },
    {
        "category": "배송",
        "question": "배송비는 얼마인가요?",
        "answer": "배송비 안내:\n\n• 30,000원 이상: 무료\n• 30,000원 미만: 3,000원\n• 제주/도서산간: 추가 3,000원\n\n신선도 유지를 위한 콜드체인 배송입니다!",
        "keywords": "배송비,비용,무료배송",
    },
    {
        "category": "배송",
        "question": "배송 조회는 어떻게 하나요?",
        "answer": "배송 조회 방법:\n\n1️⃣ 마이페이지 > 주문내역\n2️⃣ 주문번호 클릭\n3️⃣ 송장번호로 배송 추적\n\n또는 고객센터(1588-0000)로 주문번호를 말씀해주시면 조회해드립니다!",
        "keywords": "배송조회,추적,확인",
    },
    {
        "category": "반품/교환",
        "question": "반품이나 교환은 어떻게 하나요?",
        "answer": "반품/교환 절차:\n\n1️⃣ 고객센터(1588-0000) 문의\n2️⃣ 반품/교환 사유 확인\n3️⃣ 택배 회수 또는 방문 수거\n4️⃣ 검수 후 환불/교환 처리\n\n• 수령 후 7일 이내\n• 상품 미개봉/훼손 없을 것\n• 냉동 상품 특성상 신선도 확인 필요",
        "keywords": "반품,교환,환불,취소",
    },
    {
        "category": "반품/교환",
        "question": "반품 배송비는 누가 부담하나요?",
        "answer": "반품 배송비 안내:\n\n• 상품 불량/오배송: 무료 (당사 부담)\n• 단순 변심: 왕복 배송비 고객 부담\n  - 일반 지역: 6,000원\n  - 제주/도서산간: 12,000원\n\n상품 불량 시 사진과 함께 문의해주세요!",
        "keywords": "반품비용,배송비,누가",
    },
    {
        "category": "회원",
        "question": "회원가입 혜택이 있나요?",
        "answer": "회원가입 혜택:\n\n✨ 즉시 혜택\n• 신규 가입 3,000원 쿠폰\n• 첫 구매 시 추가 5% 할인\n\n🎁 회원 전용\n• 적립금 적립 (구매액의 1%)\n• 생일 쿠폰\n• 등급별 추가 할인\n• 회원 전용 특가 상품\n\n지금 가입하세요!",
        "keywords": "회원,가입,혜택,쿠폰",
    },
    {
        "category": "기타",
        "question": "영업시간은 언제인가요?",
        "answer": f"영업시간 안내:\n\n⏰ {init_db.__globals__['settings'].BUSINESS_HOURS}\n\n📞 고객센터: {init_db.__globals__['settings'].SUPPORT_PHONE}\n📧 이메일: {init_db.__globals__['settings'].SUPPORT_EMAIL}\n\n온라인 주문은 24시간 가능합니다!\n상담원 연결은 영업시간 내에만 가능합니다.",
        "keywords": "영업시간,운영시간,몇시,시간",
    },
    {
        "category": "기타",
        "question": "대량 구매 문의하고 싶어요",
        "answer": "대량 구매 문의 환영합니다!\n\n📞 대량구매 전용: 1588-0000 (내선 2번)\n📧 이메일: wholesale@i-screammall.co.kr\n\n• 기업/단체 구매 할인\n• 맞춤 견적서 발행\n• 법인 세금계산서 발행\n\n수량과 원하시는 상품을 알려주시면 최선을 다해 상담해드리겠습니다!",
        "keywords": "대량구매,도매,대량,단체,기업",
    },
]

try:
    # 기존 FAQ 삭제 (선택사항)
    db.query(FAQ).delete()

    # 샘플 FAQ 추가
    for faq_data in sample_faqs:
        faq = FAQ(**faq_data)
        db.add(faq)

    db.commit()
    print(f"✅ {len(sample_faqs)}개의 샘플 FAQ가 추가되었습니다!")

except Exception as e:
    print(f"❌ 오류: {e}")
    db.rollback()

finally:
    db.close()
