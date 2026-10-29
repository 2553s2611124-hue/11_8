
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="포근포근 플리마켓 🩵",
    page_icon="🩵",
    layout="wide",
)

# 하늘색 테마와 귀여운 디자인
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

.stApp {
    background: linear-gradient(180deg, #e1f5ff, #f5fbff, #eaf8ff);
    color: #254b61;
}
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #287da5;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(135deg, #bce8ff, #e6f7ff, #ffe9f3);
    border: 2px solid white;
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 22px;
}
.card {
    background: rgba(255,255,255,.9);
    border: 1px solid #c6eaff;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}
div.stButton > button,
div.stFormSubmitButton > button {
    background: #d8f2ff;
    color: #245e7b;
    border: 1px solid #a9def5;
    border-radius: 13px;
    font-family: 'Jua', sans-serif;
    min-height: 2.6rem;
}
div.stButton > button:hover {
    background: #bce8ff;
    border-color: #7ac9ed;
}
[data-testid="stSidebar"] {
    background: #d9f2ff;
}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #c6eaff;
    border-radius: 15px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# 기본 상품
DEFAULT_ITEMS = [
    {"상품": "구름 키링 ☁️", "가격": 3500, "초기 수량": 20, "재고": 20},
    {"상품": "하늘색 파우치 🩵", "가격": 7000, "초기 수량": 12, "재고": 12},
    {"상품": "말랑 스티커 🌷", "가격": 2000, "초기 수량": 30, "재고": 30},
    {"상품": "손뜨개 꽃 🌼", "가격": 5000, "초기 수량": 10, "재고": 10},
]

if "items" not in st.session_state:
    st.session_state.items = [item.copy() for item in DEFAULT_ITEMS]

if "records" not in st.session_state:
    st.session_state.records = []

if "event_done" not in st.session_state:
    st.session_state.event_done = {}

# 상단 배너
st.markdown("""
<div class="hero">
    <h1>🩵 포근포근 플리마켓</h1>
    <p>어서 와요! 오늘은 어떤 귀여운 보물을 발견할까요? ☁️</p>
    <p>천천히 구경하고, 즐거운 추억을 만들어 봐요! 🌷</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 메뉴
with st.sidebar:
    st.title("🐳 메뉴판")
    page = st.radio(
        "원하는 메뉴를 골라 주세요!",
        [
            "🏠 홈",
            "📍 행사장 경로 & 위치",
            "📢 행사장 주의사항",
            "🎁 이벤트",
            "🛍️ 실시간 재고",
            "🧺 재고 관리",
        ],
    )
    st.markdown("---")
    st.caption("작은 보물과 큰 행복을 찾아요! 💙")

# 홈
if page == "🏠 홈":
    st.header("☁️ 플리마켓에 오신 걸 환영해요!")

    col1, col2, col3 = st.columns(3)
    col1.metric("🛍️ 상품 종류", f"{len(st.session_state.items)}종")
    col2.metric(
        "📦 남은 상품",
        f"{sum(x['재고'] for x in st.session_state.items)}개"
    )
    col3.metric("🎁 준비된 이벤트", "3개")

    st.markdown("""
    <div class="card">
        <h3>🐾 오늘의 추천 코스</h3>
        <p>① 입구에서 안내 지도 확인하기</p>
        <p>② 귀여운 소품 부스 구경하기</p>
        <p>③ 맛있는 간식 먹기</p>
        <p>④ 휴식 공간에서 잠깐 쉬어 가기</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎒 출발 전 체크리스트")
    for item in [
        "에코백이나 장바구니 챙기기",
        "결제 수단 확인하기",
        "행사장 위치 확인하기",
        "분실물 안내 확인하기",
    ]:
        st.checkbox(item, key=f"home_{item}")

    st.info("아래 메뉴를 눌러 원하는 정보를 확인해 보세요. 🩵")

# 행사장 경로와 위치
elif page == "📍 행사장 경로 & 위치":
    st.header("📍 어디로 가 볼까요?")

    address = st.text_input(
        "행사장 주소 또는 장소명",
        value="서울 플리마켓 (예시)",
        help="실제 행사장 주소로 바꾸어 입력해 주세요."
    )

    map_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote(address.strip())
    )

    st.link_button(
        "🗺️ 지도에서 행사장 위치 보기",
        map_url,
        use_container_width=True,
    )

    places = {
        "🚪 입구 & 안내소": (
            "행사장에 도착하면 가장 먼저 들러요!",
            "안내도와 운영 시간, 분실물 안내를 확인해요."
        ),
        "🎀 소품 부스": (
            "키링과 스티커 등 귀여운 소품이 있는 곳이에요.",
            "통로를 막지 않도록 천천히 구경해요."
        ),
        "🍪 먹거리 존": (
            "간식과 음료를 즐길 수 있는 곳이에요.",
            "알레르기 유발 재료를 확인하고 쓰레기를 정리해요."
        ),
        "🚻 화장실": (
            "필요할 때 이용할 수 있는 편의시설이에요.",
            "현장 안내 표지판을 따라 이동해 주세요."
        ),
        "🪑 휴식 공간": (
            "잠깐 앉아서 쉬어 갈 수 있어요.",
            "다른 방문객도 이용할 수 있도록 배려해요."
        ),
    }

    selected = st.selectbox("장소 선택하기", list(places.keys()))
    title, description = places[selected]

    st.markdown(
        f'<div class="card"><h3>{title}</h3>'
        f'<p>{description}</p></div>',
        unsafe_allow_html=True,
    )

    st.subheader("🐾 추천 이동 순서")
    st.write("입구 → 소품 부스 → 먹거리 존 → 휴식 공간 → 출구")
    st.caption("실제 행사장 내부 위치는 주최 측 안내도를 확인해 주세요.")

# 행사장 주의사항
elif page == "📢 행사장 주의사항":
    st.header("📢 다 함께 안전하게 즐겨요!")

    notices = {
        "🚶 천천히 이동하기": (
            "사람이 많은 곳에서는 뛰지 말고 통로를 비워 둬요."
        ),
        "👜 소지품 잘 챙기기": (
            "지갑과 휴대전화를 잘 보관하고 물건을 두고 오지 않았는지 확인해요."
        ),
        "💳 구매 전에 확인하기": (
            "가격과 상품 상태, 교환 및 환불 가능 여부를 확인해요."
        ),
        "🧃 쓰레기 정리하기": (
            "쓰레기는 지정된 곳에 버리고 행사장을 깨끗하게 이용해요."
        ),
        "🧸 일행과 함께하기": (
            "일행과 만날 장소를 정해 두고 길을 잃으면 안내소에 도움을 요청해요."
        ),
        "🚨 위험 상황 알리기": (
            "위험하거나 불편한 상황을 발견하면 운영 스태프에게 알려요."
        ),
    }

    for title, description in notices.items():
        with st.expander(title):
            st.write(description)

    st.warning("안전 문제가 생기면 현장 운영요원의 안내를 따라 주세요.")

# 이벤트
elif page == "🎁 이벤트":
    st.header("🎁 신나는 플리마켓 이벤트!")

    st.caption(
        "아래 이벤트는 앱 시연용 예시예요. "
        "실제 행사에서 운영되는지는 주최 측에 확인해 주세요."
    )

    events = {
        "🌟 스탬프 투어": "참여 부스 3곳을 방문해 스탬프를 모아 봐요!",
        "🎀 나만의 보물 찾기": "마음에 드는 상품을 찾아 이유를 적어 봐요!",
        "📸 추억 기록하기": "촬영이 허용된 장소에서 추억을 남겨 봐요!",
    }

    for name, description in events.items():
        with st.container(border=True):
            st.subheader(name)
            st.write(description)

            done = st.checkbox(
                "참여 완료했어요! ✨",
                key=f"event_{name}"
            )

            if done:
                st.success("참여 완료! 즐거운 추억 하나 추가했어요 💙")

    st.subheader("💌 오늘의 한 줄 기록")
    memory = st.text_area(
        "기억하고 싶은 순간을 적어 주세요.",
        placeholder="예: 귀여운 꽃 키링을 발견했어요! 🌼"
    )

    if st.button("기록 확인하기"):
        if memory.strip():
            st.success(f"오늘의 기록: {memory.strip()}")
        else:
            st.info("한 줄만 적어 주면 기록을 확인할 수 있어요!")

# 실시간 재고 조회
elif page == "🛍️ 실시간 재고":
    st.header("🛍️ 상품 재고를 확인해요!")

    items = st.session_state.items

    if not items:
        st.info("아직 등록된 상품이 없어요.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("상품 종류", f"{len(items)}종")
        col2.metric("전체 남은 수량", f"{sum(x['재고'] for x in items)}개")
        col3.metric("품절 상품", f"{sum(x['재고'] == 0 for x in items)}종")

        for item in items:
            with st.container(border=True):
                left, right = st.columns([3, 1])

                left.subheader(item["상품"])
                left.write(f"가격: {item['가격']:,}원")
                left.write(f"남은 수량: {item['재고']}개")

                total = max(1, item["초기 수량"])
                ratio = min(1.0, item["재고"] / total)
                left.progress(ratio, text="초기 수량 대비 남은 재고")

                if item["재고"] == 0:
                    right.error("품절 🥹")
                elif item["재고"] <= 3:
                    right.warning("소량 남음 💨")
                else:
                    right.success("판매 중 🩵")

    st.caption(
        "현재 재고는 앱 세션에 저장돼요. "
        "앱 재시작이나 세션 변경 후에도 유지되는 영구 재고는 아니에요."
    )

# 재고 관리
elif page == "🧺 재고 관리":
    st.header("🧺 상품 재고 관리")
    st.warning(
        "시연용 관리 메뉴예요. 공개 운영 시에는 관리자 인증을 추가해 주세요."
    )

    st.subheader("➕ 새 상품 등록")

    with st.form("add_product", clear_on_submit=True):
        name = st.text_input("상품 이름")
        price = st.number_input(
            "가격 (원)", min_value=0, value=3000, step=500
        )
        quantity = st.number_input(
            "초기 수량", min_value=0, value=10, step=1
        )
        add = st.form_submit_button("상품 등록하기")

    if add:
        if not name.strip():
            st.error("상품 이름을 입력해 주세요.")
        elif any(x["상품"] == name.strip() for x in st.session_state.items):
            st.error("이미 등록된 상품이에요.")
        else:
            st.session_state.items.append({
                "상품": name.strip(),
                "가격": int(price),
                "초기 수량": int(quantity),
                "재고": int(quantity),
            })
            st.success("상품 등록 완료! 🩵")
            st.rerun()

    st.divider()
    st.subheader("📦 판매 및 입고 처리")

    items = st.session_state.items

    if not items:
        st.info("먼저 상품을 등록해 주세요.")
    else:
        names = [x["상품"] for x in items]
        selected = st.selectbox("상품 선택", names)
        item = next(x for x in items if x["상품"] == selected)

        st.write(f"현재 재고: **{item['재고']}개**")

        action = st.radio(
            "작업 선택",
            ["판매 처리", "추가 입고", "수량 직접 수정"],
            horizontal=True,
        )

        amount = st.number_input(
            "수량", min_value=0, value=1, step=1
        )

        if st.button("재고 반영하기", use_container_width=True):
            amount = int(amount)

            if action == "판매 처리":
                if amount > item["재고"]:
                    st.error("재고가 부족해요. 수량을 다시 확인해 주세요.")
                else:
                    item["재고"] -= amount
                    st.session_state.records.append(
                        f"{selected}: {amount}개 판매"
                    )
                    st.success(f"판매 처리 완료! {item['재고']}개 남았어요.")
                    st.rerun()

            elif action == "추가 입고":
                item["재고"] += amount
                item["초기 수량"] += amount
                st.session_state.records.append(
                    f"{selected}: {amount}개 입고"
                )
                st.success(f"입고 완료! {item['재고']}개 남았어요.")
                st.rerun()

            else:
                item["재고"] = amount
                st.session_state.records.append(
                    f"{selected}: 재고를 {amount}개로 수정"
                )
                st.success(f"재고를 {amount}개로 변경했어요.")
                st.rerun()

    with st.expander("📋 최근 재고 변경 기록"):
        if st.session_state.records:
            for record in reversed(st.session_state.records[-10:]):
                st.write(f"• {record}")
        else:
            st.caption("아직 변경 기록이 없어요.")

    if st.button("기본 샘플 재고로 초기화"):
        st.session_state.items = [
            item.copy() for item in DEFAULT_ITEMS
        ]
        st.session_state.records = []
        st.success("기본 재고로 초기화했어요!")
        st.rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#62899d;'>"
    "made with 🩵 · 포근포근 플리마켓 · 즐거운 하루 보내요!</div>",
    unsafe_allow_html=True,
)
