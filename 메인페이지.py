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

# 플리마켓 스타일에 맞춘 커스텀 CSS
st.markdown("""
    <style>
    .banner-box {
        background-color: #FEF3C7;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #F59E0B;
        margin-bottom: 20px;
    }
    .info-card {
        background-color: #F9FAFB;
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

# 2-1. 재고/부스 데이터 초기화
if "flea_inventory" not in st.session_state:
    init_items = [
        {"부스명": "부스 A (달콤푸드)", "상품명": "수제 딸기잼 세트", "카테고리": "수제 푸드", "가격(원)": 8500, "재고수량": 12, "위치": "잔디광장 A-1"},
        {"부스명": "부스 B (자수공방)", "상품명": "핸드메이드 자수 코스터", "카테고리": "패브릭/소품", "가격(원)": 4500, "재고수량": 2, "위치": "잔디광장 B-3"},
        {"부스명": "부스 C (향기창고)", "상품명": "천연 아로마 캔들", "카테고리": "리빙/향수", "가격(원)": 15000, "재고수량": 0, "위치": "잔디광장 C-2"},
        {"부스명": "부스 B (자수공방)", "상품명": "빈티지 비즈 반지", "카테고리": "악세서리", "가격(원)": 6000, "재고수량": 5, "위치": "잔디광장 B-3"},
        {"부스명": "부스 A (달콤푸드)", "상품명": "콜드브루 파우치", "카테고리": "수제 푸드", "가격(원)": 4000, "재고수량": 18, "위치": "잔디광장 A-1"}
    ]
    df_init = pd.DataFrame(init_items)
    df_init["가격(원)"] = df_init["가격(원)"].astype(int)
    df_init["재고수량"] = df_init["재고수량"].astype(int)
    st.session_state.flea_inventory = df_init

# 2-2. 셀러 신청 데이터 초기화
if "seller_applications" not in st.session_state:
    st.session_state.seller_applications = []

# 2-3. 방명록 데이터 초기화
if "guestbook" not in st.session_state:
    st.session_state.guestbook = [
        {"작성자": "민지", "메시지": "자수 코스터 너무 예뻐요! 주말 마실 나오기 딱 좋아요 💛", "별점": "⭐⭐⭐⭐⭐", "작성일": "2026-11-01"},
        {"작성자": "수현", "메시지": "수제잼 조기 품절돼서 아쉬웠어요! 다음엔 일찍 올게요~", "별점": "⭐⭐⭐⭐", "작성일": "2026-11-02"}
    ]

# ==========================================
# 3. 사이드바 - 페이지 셀렉터
# ==========================================
st.sidebar.title("🎪 마켓 가이드 메뉴")
page = st.sidebar.radio(
    "페이지를 선택하면 이동합니다:",
    [
        "📖 1. 플리마켓 소개",
        "📦 2. 실시간 부스 & 재고 안내",
        "📝 3. 셀러 참가 신청하기",
        "💬 4. 방문객 방명록 & 후기"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("📍 **행사 위치:** 중앙공원 잔디광장")
st.sidebar.markdown("⏰ **운영 시간:** 매주 토/일 11:00 ~ 17:00")

# ==========================================
# 4. 선택 페이지별 기능 구동
# ==========================================

# ------------------------------------------
# [페이지 1] 플리마켓 소개
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
        st.subheader("💡 마켓 브랜드 스토리")
        st.write("""
        '햇살가득 플리마켓'은 지역 창작자, 수공예 셀러, 디저트 장인들이 모여 
        따뜻한 취향을 나누는 팝업 플랫폼입니다. 
        
        기성품에서는 느낄 수 없는 손맛과 디테일이 살아있는 제품들을 만나보세요.
        연인, 가족, 반려동물과 함께 편안한 주말 산책을 즐기실 수 있습니다.
        """)
        
    with col_b:
        st.subheader("📍 방문 안내 및 위치")
        st.markdown("""
        * **운영 시간:** 매주 토요일, 일요일 11:00 - 17:00
        * **행사 장소:** 중앙공원 잔디광장 일대 (지하철역 2번 출구 도보 5분)
        * **주차 안내:** 공원 주차장 이용 가능 (가급적 대중교통 이용 권장)
        * **문의:** Instagram `@weekend_fleamarket`
        """)

# ------------------------------------------
# [페이지 2] 실시간 부스 & 재고 안내
# ------------------------------------------
elif page == "📦 2. 실시간 부스 & 재고 안내":
    st.title("📦 실시간 부스 & 재고 현황판")
    st.caption("현장의 인기 품목과 잔여 개수를 실시간으로 확인하고 빠르게 방문해보세요!")
    
    df_inv = st.session_state.flea_inventory
    
    if df_inv.empty:
        st.info("현재 등록된 안내 상품이 없습니다.")
    else:
        # 상태 태그 생성 함수
        def get_status_tag(qty):
            q = int(qty)
            if q <= 0:
                return "🔴 품절"
            elif q <= 3:
                return "🟡 소량남음"
            else:
                return "🟢 구매가능"

        df_inv_display = df_inv.copy()
        df_inv_display["상태"] = df_inv_display["재고수량"].apply(get_status_tag)
        
        # 현황 메트릭 카드
        total_items = len(df_inv_display)
        total_qty = int(df_inv_display["재고수량"].sum())
        sold_out = len(df_inv_display[df_inv_display["재고수량"] == 0])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("등록 품목 수", f"{total_items}개")
        m2.metric("남은 총 재고 개수", f"{total_qty}개")
        m3.metric("품절 상품", f"{sold_out}개")
        
        st.divider()
        
        # 검색 및 필터 레이아웃
        f_c1, f_c2 = st.columns([1, 2])
        cats = ["전체"] + list(df_inv_display["카테고리"].unique())
        selected_cat = f_c1.selectbox("카테고리 필터", cats)
        search_kw = f_c2.text_input("🔍 상품명 또는 부스명 검색", placeholder="검색어를 입력하세요...")
        
        filtered = df_inv_display.copy()
        if selected_cat != "전체":
            filtered = filtered[filtered["카테고리"] == selected_cat]
        if search_kw.strip():
            filtered = filtered[
                filtered["상품명"].str.contains(search_kw, case=False, na=False) |
                filtered["부스명"].str.contains(search_kw, case=False, na=False)
            ]
            
        show_cols = ["부스명", "상품명", "카테고리", "가격(원)", "재고수량", "상태", "위치"]
        st.dataframe(
            filtered[show_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "가격(원)": st.column_config.NumberColumn(format="%d 원"),
                "재고수량": st.column_config.NumberColumn(format="%d 개")
            }
        )

# ------------------------------------------
# [페이지 3] 셀러 참가 신청하기
# ------------------------------------------
elif page == "📝 3. 셀러 참가 신청하기":
    st.title("📝 신규 셀러 참가 신청")
    st.caption("햇살가득 플리마켓과 함께할 셀러분들의 신청을 기다립니다.")
    
    with st.form("seller_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            brand_name = st.text_input("브랜드/셀러명 *", placeholder="예: 달콤공방")
            seller_name = st.text_input("대표자 성함 *", placeholder="홍길동")
            contact = st.text_input("연락처 *", placeholder="010-0000-0000")
        with col2:
            category = st.selectbox("판매 품목 카테고리", ["수제 푸드", "패브릭/소품", "악세서리", "리빙/향수", "기타"])
            sns_account = st.text_input("SNS / 인스타그램 계정", placeholder="@your_brand")
            table_needed = st.radio("테이블 대여 여부", ["필요함 (1개)", "개인 테이블 지참"])
            
        description = st.text_area("판매 상품 설명 및 브랜드 소개", placeholder="판매하실 상품의 종류와 특징을 입력해주세요.")
        
        submitted = st.form_submit_button("신청서 제출하기", type="primary")
        if submitted:
            if not brand_name.strip() or not seller_name.strip() or not contact.strip():
                st.error("필수 항목(*)을 모두 입력해 주세요.")
            else:
                new_app = {
                    "브랜드명": brand_name,
                    "대표자": seller_name,
                    "연락처": contact,
                    "카테고리": category,
                    "소개": description,
                    "신청일시": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.seller_applications.append(new_app)
                st.success(f"🎉 [{brand_name}] 브랜드의 셀러 참가 신청이 접수되었습니다!")
                st.balloons()

# ------------------------------------------
# [페이지 4] 방문객 방명록 & 후기
# ------------------------------------------
elif page == "💬 4. 방문객 방명록 & 후기":
    st.title("💬 마켓 방문 후기 & 방명록")
    st.caption("플리마켓 소감이나 셀러분들을 향한 응원 메시지를 자유롭게 남겨주세요!")
    
    with st.expander("✍️ 방명록 작성하기", expanded=True):
        with st.form("guestbook_form", clear_on_submit=True):
            g_c1, g_c2 = st.columns([1, 2])
            writer = g_c1.text_input("작성자 닉네임", value="익명")
            rating = g_c2.select_slider("만족도 별점", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], value="⭐⭐⭐⭐⭐")
            message = st.text_area("응원 메시지 / 후기 내용", placeholder="따뜻한 한 줄을 남겨주세요.")
            
            gb_submit = st.form_submit_button("등록하기", type="primary")
            if gb_submit:
                if not message.strip():
                    st.warning("메시지 내용을 입력해 주세요.")
                else:
                    new_entry = {
                        "작성자": writer,
                        "메시지": message,
                        "별점": rating,
                        "작성일": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.guestbook.insert(0, new_entry)
                    st.success("방명록이 정상적으로 남겨졌습니다!")
                    st.rerun()

    st.divider()
    
    st.subheader("📜 최근 방명록 피드")
    for entry in st.session_state.guestbook:
        with st.container():
            st.markdown(f"**{entry['작성자']}** `{entry['작성일']}` | {entry['별점']}")
            st.write(entry["메시지"])
            st.markdown("---")
