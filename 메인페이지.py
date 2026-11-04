import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정 및 스타일링
# ==========================================
st.set_page_config(
    page_title="플리마켓 실시간 재고 안내",
    page_icon="🎈",
    layout="wide"
)

# 플리마켓 분위기의 커스텀 CSS 적용
st.markdown("""
    <style>
    .market-banner {
        background-color: #FFF9E6;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #FF8C00;
        margin-bottom: 25px;
    }
    .status-card {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 초기화 (Session State & 안전한 타입 지정)
# ==========================================
if "fleamarket_inventory" not in st.session_state:
    initial_items = [
        {"상품코드": "ITEM-01", "상품명": "수제 딸기잼 (250g)", "카테고리": "수제 푸드", "가격(원)": 8500, "재고수량": 12, "안내위치": "부스 1호"},
        {"상품코드": "ITEM-02", "상품명": "핸드메이드 자수 코스터", "카테고리": "패브릭/소품", "가격(원)": 4500, "재고수량": 2, "안내위치": "부스 2호"},
        {"상품코드": "ITEM-03", "상품명": "천연 아로마 캔들", "카테고리": "리빙/향수", "가격(원)": 15000, "재고수량": 0, "안내위치": "부스 3호"},
        {"상품코드": "ITEM-04", "상품명": "빈티지 비즈 반지", "카테고리": "악세서리", "가격(원)": 6000, "재고수량": 5, "안전위치": "부스 2호"},
        {"상품코드": "ITEM-05", "상품명": "드립백 커피 파우치 (5개입)", "카테고리": "수제 푸드", "가격(원)": 7000, "재고수량": 1, "안내위치": "부스 1호"},
    ]
    df_init = pd.DataFrame(initial_items)
    df_init["재고수량"] = df_init["재고수량"].astype(int)
    df_init["가격(원)"] = df_init["가격(원)"].astype(int)
    st.session_state.fleamarket_inventory = df_init

df = st.session_state.fleamarket_inventory

# 상태 표시 판별 함수 (3개 이하 수량 시 '소량남음' 경고)
def get_status(qty):
    qty = int(qty)
    if qty <= 0:
        return "🔴 품절"
    elif qty <= 3:
        return "🟡 임박 (소량남음)"
    else:
        return "🟢 구매가능"

if not df.empty:
    df["상태"] = df["재고수량"].apply(get_status)

# ==========================================
# 3. 사이드바 - 관리자/방문객 모드 전환 & 신규 품목
# ==========================================
st.sidebar.title("🎈 플리마켓 메뉴")
mode = st.sidebar.radio("모드 선택", ["👀 실시간 재고 보기 (방문객)", "⚙️ 수량 정산/관리 (셀러용)"])

st.sidebar.divider()
st.sidebar.subheader("➕ 신규 상품 등록 (셀러 전용)")
with st.sidebar.form("add_item_form", clear_on_submit=True):
    new_code = st.text_input("상품코드", value=f"ITEM-0{len(df)+1}")
    new_name = st.text_input("상품명", placeholder="예: 손느낌 도자기 컵")
    new_cat = st.selectbox("카테고리", ["수제 푸드", "패브릭/소품", "악세서리", "리빙/향수", "기타"])
    new_price = st.number_input("가격(원)", min_value=0, value=5000, step=500)
    new_qty = st.number_input("초기 수량(개)", min_value=0, value=10, step=1)
    new_loc = st.text_input("부스 번호/위치", value="부스 1호")
    
    submit_btn = st.form_submit_button("상품 등록", type="primary")
    if submit_btn:
        if not new_name.strip():
            st.sidebar.error("상품명을 입력해주세요.")
        elif new_code in st.session_state.fleamarket_inventory["상품코드"].values:
            st.sidebar.error("이미 존재하는 상품코드입니다.")
        else:
            new_row = {
                "상품코드": str(new_code),
                "상품명": str(new_name),
                "카테고리": str(new_cat),
                "가격(원)": int(new_price),
                "재고수량": int(new_qty),
                "안내위치": str(new_loc)
            }
            st.session_state.fleamarket_inventory = pd.concat(
                [st.session_state.fleamarket_inventory, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.sidebar.success(f"'{new_name}' 등록 완료!")
            st.rerun()

# ==========================================
# 4. 메인 화면 - 플리마켓 소개 글 (요구사항 반영)
# ==========================================
st.title("🎈 햇살가득 주말 플리마켓")
st.caption("실시간으로 각 부스별 수량 및 잔여 개수를 안내해 드립니다.")

# 플리마켓 소개 박스
st.markdown("""
<div class="market-banner">
    <h3>📢 플리마켓 행사 안내 & 소개</h3>
    <p><b>운영 시간:</b> 매주 토/일요일 11:00 ~ 17:00 | <b>장소:</b> 중앙 공원 잔디광장</p>
    <p>정성껏 만든 핸드메이드 소품과 정갈한 수제 디저트를 만날 수 있는 팝업 마켓입니다.<br>
    인기 수제 품목은 조기 품절될 수 있으니 아래 <b>실시간 재고 수량</b>을 꼭 확인해 주세요!</p>
    <small>💡 🎁 <b>이벤트:</b> 2개 이상 구매 시 현장 할인 혜택이 적용됩니다.</small>
</div>
""", unsafe_allow_html=True)

# 주요 지표 (Metrics)
total_items_cnt = len(df)
total_rem_qty = int(df["재고수량"].sum()) if not df.empty else 0
out_cnt = len(df[df["재고수량"] <= 0]) if not df.empty else 0
low_cnt = len(df[(df["재고수량"] > 0) & (df["재고수량"] <= 3)]) if not df.empty else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("총 등록 상품", f"{total_items_cnt}개")
m2.metric("남은 전체 개수", f"{total_rem_qty:,}개")
m3.metric("품절 임박 (3개 이하)", f"{low_cnt}개", delta_color="inverse")
m4.metric("완판/품절", f"{out_cnt}개", delta_color="inverse")

st.divider()

# ==========================================
# 5. 모드별 화면 구성을 위한 렌더링
# ==========================================

# ------------------------------------------
# 모드 1: 실시간 재고 보기 (방문객용)
# ------------------------------------------
if mode == "👀 실시간 재고 보기 (방문객)":
    st.subheader("🛍️ 실시간 개수 & 재고 현황판")
    
    if df.empty:
        st.info("현재 안내할 상품이 없습니다.")
    else:
        # 검색 및 필터
        c1, c2 = st.columns([1, 2])
        cats = ["전체 카테고리"] + sorted(list(df["카테고리"].unique()))
        selected_cat = c1.selectbox("카테고리 선택", cats)
        search_txt = c2.text_input("🔍 상품명으로 찾기", placeholder="찾으시는 상품명을 입력하세요...")
        
        filtered_df = df.copy()
        if selected_cat != "전체 카테고리":
            filtered_df = filtered_df[filtered_df["카테고리"] == selected_cat]
        if search_txt.strip():
            filtered_df = filtered_df[filtered_df["상품명"].str.contains(search_txt, case=False, na=False)]
        
        # 보기 좋은 표 형태로 출력
        show_cols = ["상품코드", "상품명", "카테고리", "가격(원)", "재고수량", "상태", "안내위치"]
        st.dataframe(
            filtered_df[show_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "가격(원)": st.column_config.NumberColumn(format="%d 원"),
                "재고수량": st.column_config.NumberColumn(format="%d 개")
            }
        )

# ------------------------------------------
# 모드 2: 수량 정산/관리 (셀러 전용 현장 조작)
# ------------------------------------------
else:
    st.subheader("⚙️ 셀러 전용 수량 실시간 조작")
    st.caption("판매가 일어날 때마다 아래 버튼을 눌러 현장 재고 개수를 바로 수정하세요.")
    
    if df.empty:
        st.info("등록된 상품이 없습니다. 사이드바에서 상품을 먼저 등록하세요.")
    else:
        for idx, row in df.iterrows():
            with st.container():
                col_info, col_btn1, col_btn2, col_btn3, col_del = st.columns([4, 1.5, 1.5, 2, 1])
                
                # 상품 정보 표시
                curr_qty = int(row["재고수량"])
                col_info.markdown(f"**[{row['상품코드']}] {row['상품명']}** | {row['가격(원)']:,}원 | 위치: {row['안내위치']}")
                col_info.caption(f"현재 수량: **{curr_qty}개** ({row['상태']})")
                
                # -1 개수 감소 버튼
                if col_btn1.button("➖ 1개 판매", key=f"dec_{row['상품코드']}"):
                    if curr_qty > 0:
                        st.session_state.fleamarket_inventory.loc[idx, "재고수량"] = curr_qty - 1
                        st.rerun()
                
                # +1 개수 증가 버튼
                if col_btn2.button("➕ 1개 채움", key=f"inc_{row['상품코드']}"):
                    st.session_state.fleamarket_inventory.loc[idx, "재고수량"] = curr_qty + 1
                    st.rerun()
                
                # 즉시 품
