import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. 페이지 기본 설정 및 디자인 (CSS)
# ==========================================
st.set_page_config(
    page_title="감성 팝업 & 플리마켓 포털",
    page_icon="🎪",
    layout="wide"
)

# 플리마켓에 어울리는 감성 스타일링
st.markdown("""
    <style>
    .main-title {
        color: #D97706;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .banner-box {
        background-color: #FEF3C7;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #F59E0B;
        margin-bottom: 20px;
    }
    .booth-card {
        background-color: #FAFAFA;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 글로벌 세션 데이터 초기화 (오류 방지)
# ==========================================

# 2-1. 재고/부스 데이터
if "flea_inventory" not in st.session_state:
    init_items = [
        {"부스명": "부스 A (달콤푸드)", "상품명": "수제 수제잼 세트", "카테고리": "수제 푸드", "가격(원)": 8500, "재고수량": 12, "위치": "잔디광장 A-1"},
        {"부스명": "부스 B (자수공방)", "상품명": "핸드메이드 자수 코스터", "카테고리": "패브릭/소품", "가격(원)": 4500, "재고수량": 2, "위치": "잔디광장 B-3"},
        {"부스명": "부스 C (향기창고)", "상품명": "천연 아로마 캔들", "카테고리": "리빙/향수", "가격(원)": 15000, "재고수량": 0, "위치": "잔디광장 C-2"},
        {"부스명": "부스 B (자수공방)", "상품명": "빈티지 비즈 반지", "카테고리": "악세서리", "가격(원)": 6000, "재고수량": 5, "위치": "잔디광장 B-3"},
        {"부스명": "부스 A (달콤푸드)", "상품명": "콜드브루 파우치", "카테고리": "수제 푸드", "가격(원)": 4000, "재고수량": 18, "위치": "잔디광장 A-1"}
    ]
    df_init = pd.DataFrame(init_items)
    df_init["가격(원)"] = df_init["가격(원)"].astype(int)
    df_init["재고수량"] = df_init["재고수량"].astype(int)
    st.session_state.flea_inventory = df_init

# 2-2. 셀러 신청 데이터
if "seller_applications" not in st.session_state:
    st.session_state.seller_applications = []

# 2-3. 방명록 데이터
if "guestbook" not in st.session_state:
    st.session_state.guestbook = [
        {"작성자": "민지", "메시지": "자수 코스터 너무 예뻐요! 주말 마실 나오기 딱 좋아요 💛", "별점": "⭐⭐⭐⭐⭐", "작성일": "2026-11-01"},
        {"작성자": "수현", "메시지": "수제잼 조기 품절돼서 아쉬웠어요! 다음엔 일찍 올게요~", "별점": "⭐⭐⭐⭐", "작성일": "2026-11-02"}
    ]

# ==========================================
# 3. 사이드바 - 페이지 메뉴 셀렉터
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1513151233558-d860c5398176?w=400", use_column_width=True)
st.sidebar.title("🎪 마켓 이동하기")
page = st.sidebar.radio(
    "원하는 페이지를 선택하세요:",
    [
        "📖 1. 플리마켓 소개",
        "📦 2. 실시간 부스 & 재고 안내",
        "📝 3. 셀러 참가 신청하기",
        "💬 4. 방문객 방명록 & 후기"
    ]
)

st.sidebar.divider()
st.sidebar.caption("📍 위치: 중앙 공원 잔디광장")
st.sidebar.caption("⏰ 일시: 매주 토/일 11:00 ~ 17:00")

# ==========================================
# 4. 페이지별 독립 앱 구동
# ==========================================

# ------------------------------------------
# [페이지 1] 플리마켓 소개 (Brand Story)
# ------------------------------------------
if page == "📖 1. 플리마켓 소개":
    st.title("🎪 햇살가득 주말 감성 플리마켓")
    st.caption("일상에 소소한 온기를 더하는 핸드메이드 팝업 마켓에 여러분을 초대합니다.")
    
    st.markdown("""
    <div class="banner-box">
        <h3>📢 이번 주말 마켓 하이라이트</h3>
        <p>🌱 <b>지속 가능한 일상:</b> 친환경 제로웨이스트 소품 및 수제 정성 가득 푸드 총집합!</p>
        <p>🎁 <b>방문객 이벤트:</b> 2개 이상 부스 구매 시 현장 뽑기 이벤트 참여권 증정!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("💡 마켓 소개")
        st.write("""
        '햇살가
