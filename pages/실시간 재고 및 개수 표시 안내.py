import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="실시간 재고 & 개수 안내 대시보드",
    page_icon="📦",
    layout="wide"
)

# Custom CSS로 가시성 향상
st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 초기화 (Session State)
# ==========================================
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"상품코드": "P001", "상품명": "무선 마우스", "카테고리": "전자기기", "보관위치": "A-1", "단가(원)": 25000, "재고수량": 15, "안전재고": 5},
        {"상품코드": "P002", "상품명": "기계식 키보드", "카테고리": "전자기기", "보관위치": "A-2", "단가(원)": 89000, "재고수량": 3, "안전재고": 5},
        {"상품코드": "P003", "상품명": "27인치 모니터", "카테고리": "전자기기", "보관위치": "B-1", "단가(원)": 240000, "재고수량": 0, "안전재고": 2},
        {"상품코드": "P004", "상품명": "A4 복용지(1BOX)", "카테고리": "사무용품", "보관위치": "C-1", "단가(원)": 32000, "재고수량": 45, "안전재고": 10},
        {"상품코드": "P005", "상품명": "유성펜 세트", "카테고리": "사무용품", "보관위치": "C-2", "단가(원)": 4500, "재고수량": 2, "안전재고": 5},
    ])

df = st.session_state.inventory

# 재고 상태 판별 함수
def get_status(row):
    if row["재고수량"] == 0:
        return "🔴 품절"
    elif row["재고수량"] <= row["안전재고"]:
        return "🟡 부족"
    else:
        return "🟢 정상"

if not df.empty:
    df["재고상태"] = df.apply(get_status, axis=1)

# ==========================================
# 3. 사이드바 - 메뉴 구성
# ==========================================
st.sidebar.title("📌 메뉴")
menu = st.sidebar.radio("작업 선택", ["📊 실시간 재고 현황", "✏️ 재고 수량 변경", "➕ 신규 품목 등록"])

# ==========================================
# 4. 헤더 및 요약 지표 (Metrics)
# ==========================================
st.title("📦 실시간 재고 & 개수 안내 대시보드")
st.caption("현재 품목의 재고 개수와 상태를 실시간으로 모니터링하고 관리할 수 있습니다.")

total_items = len(df)
total_qty = int(df["재고수량"].sum()) if not df.empty else 0
out_of_stock = len(df[df["재고수량"] == 0]) if not df.empty else 0
low_stock = len(df[(df["재고수량"] > 0) & (df["재고수량"] <= df["안전재고"])]) if not df.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("총 등록 품목", f"{total_items:,} 개")
col2.metric("총 재고 개수", f"{total_qty:,} 개")
col3.metric("재고 부족 (임박)", f"{low_stock:,} 건")
col4.metric("품절 상태", f"{out_of_stock:,} 건")

st.divider()

# ==========================================
# 5. 메뉴별 기능 구현
# ==========================================

# ------------------------------------------
# 메뉴 1: 실시간 재고 현황
# ------------------------------------------
if menu == "📊 실시간 재고 현황":
    st.subheader("🔍 재고 조회 및 검색")
    
    if df.empty:
        st.info("등록된 재고 상품이 없습니다.")
    else:
        # 필터 레이아웃
        f_col1, f_col2, f_col3 = st.columns([2, 2, 3])
        
        cats = ["전체"] + sorted(list(df["카테고리"].unique()))
        selected_cat = f_col1.selectbox("카테고리 필터", cats)
        
        statuses = ["전체", "🔴 품절", "🟡 부족", "🟢 정상"]
        selected_status = f_col2.selectbox("재고 상태 필터", statuses)
        
        search_kw = f_col3.text_input("상품명 검색", placeholder="검색할 상품명을 입력하세요")
        
        # 필터링 처리
        filtered = df.copy()
        if selected_cat != "전체":
            filtered = filtered[filtered["카테고리"] == selected_cat]
        if selected_status != "전체":
            filtered = filtered[filtered["재고상태"] == selected_status]
        if search_kw:
            filtered = filtered[filtered["상품명"].str.contains(search_kw, case=False, na=False)]
            
        st.write(f"검색 결과: 총 **{len(filtered)}**건")
        
        # 표 출력
        cols = ["상품코드", "상품명", "카테고리", "보관위치", "단가(원)", "재고수량", "안전재고", "재고상태"]
        st.dataframe(
            filtered[cols],
            use_container_width=True,
            hide_index=True
        )

# ------------------------------------------
# 메뉴 2: 재고 수량 변경
# ------------------------------------------
elif menu == "✏️ 재고 수량 변경":
    st.subheader("✏️ 품목별 재고 수량 조정")
    
    if df.empty:
        st.info("조정 가능한 품목이 없습니다.")
    else:
        # 품목 선택
        options = [f"{row['상품코드']} | {row['상품명']} (현재: {row['재고수량']}개)" for _, row in df.iterrows()]
        selected_option = st.selectbox("수량을 변경할 품목을 선택하세요", options)
        
        selected_code = selected_option.split(" | ")[0]
        selected_row = df[df["상품코드"] == selected_code].iloc[0]
        
        col_up, col_del = st.columns(2)
        
        with col_up:
            st.write(f"**선택 품목:** {selected_row['상품명']} ({selected_row['상품코드']})")
            new_qty = st.number_input("변경할 재고 개수", min_value=0, value=int(selected_row["재고수량"]), step=1)
            
            if st.button("수량 저장", type="primary"):
                st.session_state.inventory.loc[
                    st.session_state.inventory["상품코드"] == selected_code, "재고수량"
                ] = new_qty
                st.success(f"[{selected_row['상품명']}]의 재고가 {new_qty}개로 변경되었습니다.")
                st.rerun()

        with col_del:
            st.write("**품목 삭제**")
            st.caption("해당 상품을 목록에서 완전히 제거합니다.")
            if st.button("상품 삭제", type="secondary"):
                st.session_state.inventory = st.session_state.inventory[
                    st.session_state.inventory["상품코드"] != selected_code
                ]
                st.warning(f"[{selected_row['상품명']}] 품목이 삭제되었습니다.")
                st.rerun()

# ------------------------------------------
# 메뉴 3: 신규 품목 등록
# ------------------------------------------
elif menu == "➕ 신규 품목 등록":
    st.subheader("➕ 신규 재고 품목 등록")
    
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        
        with c1:
            code = st.text_input("상품 코드", value=f"P00{len(df)+1}")
            name = st.text_input("상품명", placeholder="예: 무선 헤드셋")
            category = st.text_input("카테고리", value="전자기기")
            
        with c2:
            location = st.text_input("보관 위치", value="A-3")
            price = st.number_input("단가(원)", min_value=0, value=10000, step=1000)
            qty = st.number_input("초기 재고 개수", min_value=0, value=10, step=1)
            safe_qty = st.number_input("최소 안전 재고", min_value=0, value=5, step=1)
            
        submit = st.form_submit_button("등록 완료", type="primary")
        
        if submit:
            if not code or not name:
                st.error("상품 코드와 상품명은 필수 입력 사항입니다.")
            elif code in st.session_state.inventory["상품코드"].values:
                st.error("이미 존재하는 상품 코드입니다.")
            else:
                new_item = {
                    "상품코드": code,
                    "상품명": name,
                    "카테고리": category,
                    "보관위치": location,
                    "단가(원)": price,
                    "재고수량": qty,
                    "안전재고": safe_qty
                }
                st.session_state.inventory = pd.concat(
                    [st.session_state.inventory, pd.DataFrame([new_item])],
                    ignore_index=True
                )
                st.success(f"[{name}] 품목이 성공적으로 등록되었습니다.")
                st.rerun()
