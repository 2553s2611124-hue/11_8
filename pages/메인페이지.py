
import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="포근포근 플리마켓 🩵",
    page_icon="🩵",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(180deg, #eaf9ff, #f7fcff, #edf9ff);
    color: #23465a;
}
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #246b91;
}
.block-container {
    max-width: 1150px;
    padding-top: 1.7rem;
}
.hero {
    background: linear-gradient(135deg, #bfeaff, #e7f8ff, #ffeaf4);
    border: 2px solid white;
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 20px;
}
.card {
    background: white;
    border: 1px solid #cceeff;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}
div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 14px;
    background: #dff5ff;
    border: 1px solid #a8def5;
    color: #225c7a;
    font-family: 'Jua', sans-serif;
}
[data-testid="stSidebar"] {
    background: #dff5ff;
}
</style>
""", unsafe_allow_html=True)

DEFAULT_ITEMS = [
    {"상품": "구름 키링 ☁️", "가격(원)": 3500,
     "초기 수량": 20, "남은 수량": 20},
    {"상품": "하늘색 파우치 🩵", "가격(원)": 7000,
     "초기 수량": 12, "남은 수량": 12},
    {"상품": "말랑 스티커 세트 🌷", "가격(원)": 2000,
     "초기 수량": 30, "남은 수량": 30},
    {"상품": "손뜨개 꽃 🌼", "가격(원)": 5000,
     "초기 수량": 10, "남은 수량": 10},
]

if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame(DEFAULT_ITEMS)
if "sales_log" not in st.session_state:
    st.session_state.sales_log = []

st.markdown("""
<div class="hero">
<h1>🩵 포근포근 플리마켓</h1>
<p>천천히 구경하고, 마음에 드는 보물도 찾아봐요! ☁️</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🐳 메뉴")
    page = st.radio("메뉴 선택", [
        "🏠 홈", "📍 경로 & 위치", "📢 주의사항",
        "🎁 이벤트", "🛍️ 실시간 재고", "🧺 재고 관리"
    ])
    st.caption("즐거운 하루 보내요! 🩵")

if page == "🏠 홈":
    st.header("오늘은 어떤 보물을 찾을까요? 🐾")
    a, b, c = st.columns(3)
    a.metric("등록 상품", f"{len(st.session_state.inventory)}종")
    b.metric("남은 상품", f"{int(st.session_state.inventory['남은 수량'].sum())}개")
    c.metric("추천 코스", "3곳")

    st.markdown("""
    <div class="card">
    <h3>☁️ 포근한 추천 코스</h3>
    입구에서 안내 지도 확인하기 → 소품 부스 둘러보기 →
    먹거리 존에서 쉬어가기 → 마음에 드는 물건 구매하기!
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎒 출발 전 체크리스트")
    for item in [
        "장바구니 챙기기", "결제 수단 확인하기",
        "행사장 위치 확인하기", "분실물 안내 확인하기"
    ]:
        st.checkbox(item, key=f"check_{item}")

elif page == "📍 경로 & 위치":
    st.header("📍 행사장 길 안내")
    venue = st.text_input("행사장 주소 또는 장소명",
                          "서울 플리마켓 (예시)")
    st.link_button(
        "🗺️ 지도에서 행사장 찾기",
        "https://www.google.com/maps/search/?api=1&query="
        + quote(venue.strip()),
        use_container_width=True
    )

    places = {
        "🚪 입구 & 안내소": "안내도와 운영 시간을 먼저 확인해요.",
        "🎀 소품 부스": "키링, 스티커, 파우치를 구경해요.",
        "🍪 먹거리 존": "간식과 음료를 즐겨요.",
        "🚻 화장실": "현장 표지판을 따라 이동해요.",
        "🪑 휴식 공간": "잠시 앉아서 쉬어 가요."
    }
    chosen = st.selectbox("장소 선택", list(places.keys()))
    st.markdown(
        f'<div class="card"><h3>{chosen}</h3>'
        f'<p>{places[chosen]}</p></div>',
        unsafe_allow_html=True
    )
    st.info("추천 동선: 입구 → 소품 부스 → 먹거리 존 → 휴식 공간")

elif page == "📢 주의사항":
    st.header("📢 우리 모두 편안하게 즐겨요!")
    tips = {
        "🚶 천천히 이동하기": "혼잡한 곳에서는 뛰지 말고 통로를 비워 둬요.",
        "👜 소지품 챙기기": "지갑과 휴대전화를 잘 보관해요.",
        "💳 구매 전 확인하기": "가격과 교환·환불 가능 여부를 물어봐요.",
        "🧃 쓰레기 정리하기": "쓰레기는 지정된 곳에 버려요.",
        "🧸 일행과 함께하기": "만날 장소를 미리 정해 둬요.",
        "🚨 위험 상황 알리기": "운영 스태프에게 도움을 요청해요."
    }
    for title, body in tips.items():
        with st.expander(title):
            st.write(body)

elif page == "🎁 이벤트":
    st.header("🎁 플리마켓 이벤트")
    st.caption("아래는 시연용 예시 이벤트예요. 실제 운영 여부를 확인해 주세요.")

    events = {
        "🌟 스탬프 투어": "참여 부스 3곳을 방문해요!",
        "🎀 보물 찾기": "마음에 드는 상품을 발견해요!",
        "📸 추억 기록": "촬영이 허용된 곳에서 추억을 남겨요!"
    }
    for name, description in events.items():
        with st.container(border=True):
            st.subheader(name)
            st.write(description)
            if st.checkbox("참여 완료 ✨", key=f"event_{name}"):
                st.success("참여 완료! 즐거운 추억 하나 추가했어요 💙")

    memory = st.text_area("오늘의 한 줄 기록", placeholder="오늘 발견한 보물은?")
    if st.button("기록 확인하기"):
        if memory.strip():
            st.success(f"오늘의 기록: {memory.strip()}")
        else:
            st.info("기억하고 싶은 순간을 적어 주세요!")

elif page == "🛍️ 실시간 재고":
    st.header("🛍️ 상품 재고 한눈에 보기")
    inventory = st.session_state.inventory.copy()

    if inventory.empty:
        st.info("등록된 상품이 없어요.")
    else:
        inventory["재고 상태"] = inventory["남은 수량"].apply(
            lambda n: "품절 🥹" if n <= 0
            else "얼마 안 남았어요 💨" if n <= 3
            else "판매 중 🩵"
        )
        st.dataframe(inventory, use_container_width=True, hide_index=True)
        st.metric("전체 남은 수량", f"{int(inventory['남은 수량'].sum())}개")

        for _, item in inventory.iterrows():
            with st.container(border=True):
                st.subheader(item["상품"])
                st.write(f"가격: {item['가격(원)']:,}원")
                st.write(f"남은 수량: {int(item['남은 수량'])}개")

elif page == "🧺 재고 관리":
    st.header("🧺 재고 관리")
    st.warning("시연용 관리 화면이에요. 공개 운영 시 인증 기능을 추가해 주세요.")

    with st.form("add_item"):
        name = st.text_input("새 상품 이름")
        price = st.number_input("가격 (원)", min_value=0, value=3000, step=500)
        qty = st.number_input("초기 수량", min_value=0, value=10)
        submitted = st.form_submit_button("상품 등록")

    if submitted:
        if not name.strip():
            st.error("상품 이름을 입력해 주세요.")
        elif name.strip() in st.session_state.inventory["상품"].tolist():
            st.error("이미 등록된 상품이에요.")
        else:
            new_item = pd.DataFrame([{
                "상품": name.strip(),
                "가격(원)": int(price),
                "초기 수량": int(qty),
                "남은 수량": int(qty)
            }])
            st.session_state.inventory = pd.concat(
                [st.session_state.inventory, new_item],
                ignore_index=True
            )
            st.success("상품을 등록했어요!")
            st.rerun()

    inventory = st.session_state.inventory
    if not inventory.empty:
        selected = st.selectbox("상품 선택", inventory["상품"].tolist())
        idx = inventory.index[inventory["상품"] == selected][0]
        current = int(inventory.loc[idx, "남은 수량"])

        action = st.radio(
            "작업 선택", ["판매 처리", "추가 입고", "수량 직접 수정"]
        )
        amount = st.number_input("수량", min_value=0, value=1, step=1)

        if st.button("재고 반영하기"):
            if action == "판매 처리":
                if amount > current:
                    st.error(f"재고가 부족해요. 현재 {current}개예요.")
                else:
                    inventory.loc[idx, "남은 수량"] = current - int(amount)
                    st.success("판매 수량을 반영했어요!")
                    st.rerun()
            elif action == "추가 입고":
                inventory.loc[idx, "남은 수량"] = current + int(amount)
                inventory.loc[idx, "초기 수량"] += int(amount)
                st.success("추가 입고를 반영했어요!")
                st.rerun()
            else:
                inventory.loc[idx, "남은 수량"] = int(amount)
                st.success("수량을 변경했어요!")
                st.rerun()

st.markdown("---")
st.caption("made with 🩵 · 포근포근 플리마켓 안내소")
