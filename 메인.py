
import streamlit as st
from urllib.parse import quote_plus
from datetime import datetime

st.set_page_config(
    page_title="편안하게 플리마켓 즐기는 법!",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 기본 설정
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #FFF9F2;
}
h1, h2, h3 {
    color: #654735;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 45px;
    border: 1px solid #E7D5C3;
}
div.stButton > button:hover {
    border-color: #B88662;
    color: #654735;
}
.market-card {
    background: #FFFFFF;
    border: 1px solid #F0E1D1;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 10px;
}
.small-note {
    color: #76685D;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

PAGES = [
    "🏠 홈",
    "📦 실시간 재고 및 개수 표시",
    "📢 주의사항 및 이벤트",
    "🚨 긴급상황 대처법",
    "🗺️ 행사장 경로 및 위치",
]

if "page" not in st.session_state:
    st.session_state.page = "🏠 홈"

if "stock" not in st.session_state:
    st.session_state.stock = {
        "핸드메이드 키링": {"price": 5000, "qty": 15},
        "비즈 팔찌": {"price": 4000, "qty": 20},
        "에코백": {"price": 10000, "qty": 8},
        "수제 비누": {"price": 6000, "qty": 12},
        "엽서 세트": {"price": 3000, "qty": 25},
    }

if "sales_count" not in st.session_state:
    st.session_state.sales_count = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "market_address" not in st.session_state:
    st.session_state.market_address = "서울특별시 서울광장"

def go_to(page):
    st.session_state.page = page

def won(value):
    return f"{value:,}원"

# -----------------------------
# 사이드바 메뉴
# -----------------------------
with st.sidebar:
    st.markdown("# 🛍️ 플리마켓")
    st.caption("여유롭고 즐거운 하루를 위한 안내서")
    st.divider()

    for page in PAGES:
        if st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
        ):
            go_to(page)

    st.divider()
    st.markdown("### 오늘의 이용 팁")
    st.info("장바구니 대신 에코백을 챙기고, 현금과 간편결제 수단을 함께 준비해 보세요.")
    st.caption("※ 예시 데이터로 구성된 안내 앱입니다.")

# -----------------------------
# 홈
# -----------------------------
if st.session_state.page == "🏠 홈":
    st.markdown("# 🧺 편안하게 플리마켓 즐기는 법!")
    st.markdown(
        "구경은 여유롭게, 쇼핑은 알뜰하게! "
        "필요한 정보만 빠르게 확인해 보세요."
    )

    st.markdown(
        '<div class="market-card">'
        '<h3>🌷 오늘의 플리마켓</h3>'
        '<p>다양한 수공예품과 소품을 구경하고, '
        '판매자와 이야기도 나눠 보세요.</p>'
        '<p>추천 준비물: 에코백 · 물 · 결제 수단 · 편한 신발</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    total_items = sum(
        item["qty"] for item in st.session_state.stock.values()
    )
    total_products = len(st.session_state.stock)

    c1, c2, c3 = st.columns(3)
    c1.metric("상품 종류", f"{total_products}종")
    c2.metric("등록된 재고", f"{total_items}개")
    c3.metric("판매 처리", f"{st.session_state.sales_count}개")

    st.markdown("## ✨ 무엇이 궁금하세요?")
    st.caption("아래 버튼을 누르면 해당 기능으로 이동합니다.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📦 실시간 재고 및 개수 표시", use_container_width=True):
            go_to("📦 실시간 재고 및 개수 표시")
        if st.button("🚨 행사장 긴급상황 대처법", use_container_width=True):
            go_to("🚨 긴급상황 대처법")

    with c2:
        if st.button("📢 행사장 주의사항 및 관련 이벤트", use_container_width=True):
            go_to("📢 주의사항 및 이벤트")
        if st.button("🗺️ 행사장 경로 및 위치", use_container_width=True):
            go_to("🗺️ 행사장 경로 및 위치")

    st.markdown("## 💡 편안한 관람을 위한 3가지")
    a, b, c = st.columns(3)
    a.markdown("### 👟\n편한 복장\n\n오래 걸어도 편한 신발을 신어요.")
    b.markdown("### 👜\n가벼운 짐\n\n에코백과 물을 챙겨요.")
    c.markdown("### 💳\n결제 확인\n\n가격과 결제 방법을 미리 확인해요.")

# -----------------------------
# 재고 및 판매 관리
# -----------------------------
elif st.session_state.page == "📦 실시간 재고 및 개수 표시":
    st.title("📦 실시간 재고 및 개수 표시")
    st.write("상품별 수량을 확인하고 입고 또는 판매 처리를 할 수 있어요.")

    stock = st.session_state.stock
    total_qty = sum(item["qty"] for item in stock.values())
    low_qty = sum(1 for item in stock.values() if item["qty"] <= 5)

    c1, c2, c3 = st.columns(3)
    c1.metric("상품 종류", f"{len(stock)}종")
    c2.metric("남은 총수량", f"{total_qty}개")
    c3.metric("재고 확인 필요", f"{low_qty}종")

    keyword = st.text_input("🔎 상품 검색", placeholder="예: 키링, 팔찌")
    filtered = [
        name for name in stock
        if keyword.strip().lower() in name.lower()
    ]

    if not filtered:
        st.warning("검색 결과가 없어요. 다른 상품명을 입력해 보세요.")

    for index, name in enumerate(filtered):
        item = stock[name]
        with st.container(border=True):
            left, right = st.columns([2, 1])
            with left:
                st.subheader(name)
                st.write(f"가격: **{won(item['price'])}**")
                st.write(f"남은 수량: **{item['qty']}개**")
                if item["qty"] == 0:
                    st.error("품절")
                elif item["qty"] <= 5:
                    st.warning("재고가 얼마 남지 않았어요.")
                else:
                    st.success("구매 가능")

            with right:
                amount = st.number_input(
                    "변경 수량",
                    min_value=1,
                    max_value=1000,
                    value=1,
                    step=1,
                    key=f"amount_{name}",
                )

                x, y = st.columns(2)
                with x:
                    if st.button(
                        "➕ 입고",
                        key=f"add_{name}",
                        use_container_width=True,
                    ):
                        try:
                            item["qty"] += int(amount)
                            st.session_state.history.insert(
                                0, f"{datetime.now():%H:%M:%S} - "
                                f"{name} {amount}개 입고"
                            )
                            st.rerun()
                        except (ValueError, TypeError, KeyError):
                            st.error("입고 처리 중 오류가 발생했어요.")

                with y:
                    if st.button(
                        "➖ 판매",
                        key=f"sell_{name}",
                        use_container_width=True,
                    ):
                        try:
                            if item["qty"] < amount:
                                st.warning("남은 재고보다 많이 판매할 수 없어요.")
                            else:
                                item["qty"] -= int(amount)
                                st.session_state.sales_count += int(amount)
                                st.session_state.history.insert(
                                    0, f"{datetime.now():%H:%M:%S} - "
                                    f"{name} {amount}개 판매"
                                )
                                st.rerun()
                        except (ValueError, TypeError, KeyError):
                            st.error("판매 처리 중 오류가 발생했어요.")

    st.divider()
    st.subheader("🧾 최근 재고 변경 내역")
    if st.session_state.history:
        for record in st.session_state.history[:10]:
            st.write(f"• {record}")
    else:
        st.caption("아직 변경 내역이 없어요.")

    st.caption(
        "주의: 이 버전은 현재 세션의 예시 재고를 관리합니다. "
        "페이지를 새로 시작하거나 서버가 재시작되면 데이터가 초기화될 수 있으며, "
        "실제 판매자 간 재고가 자동으로 공유되지는 않습니다."
    )

# -----------------------------
# 주의사항 및 이벤트
# -----------------------------
elif st.session_state.page == "📢 주의사항 및 이벤트":
    st.title("📢 행사장 주의사항 및 관련 이벤트")
    st.write("모두가 기분 좋게 즐길 수 있도록 확인해 주세요.")

    with st.expander("✅ 방문 전 알아두면 좋은 주의사항", expanded=True):
        st.markdown("""
        - 사람이 많은 곳에서는 가방과 소지품을 잘 챙겨요.
        - 구매 전 가격, 크기, 교환 가능 여부를 확인해요.
        - 사진 촬영 전 판매자에게 허락을 구해요.
        - 통로와 비상구를 막지 않아요.
        - 쓰레기는 지정된 장소에 버려요.
        - 음식이나 음료는 행사장 안내 규정을 따라요.
        """)

    with st.expander("💰 현명한 쇼핑 방법"):
        st.markdown("""
        - 구매할 물건과 예산을 미리 정해요.
        - 여러 판매자의 상품과 가격을 비교해요.
        - 수공예품은 제작 방식과 관리 방법을 물어봐요.
        - 결제 후 영수증이나 결제 내역을 확인해요.
        """)

    st.subheader("🎉 행사 이벤트 안내")
    events = [
        ("🎁 랜덤 뽑기", "운영 부스에서 참여 방법과 경품을 확인해 보세요."),
        ("📸 포토존 인증", "포토존에서 사진을 찍고 공식 이벤트 안내를 확인해 보세요."),
        ("🧵 수공예 체험", "체험 부스의 운영 시간과 참가비를 먼저 확인해요."),
        ("♻️ 에코백 캠페인", "개인 가방을 가져와 일회용 포장재 사용을 줄여요."),
    ]

    for title, description in events:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.write(description)

    st.info(
        "위 이벤트는 앱에서 제공하는 예시 아이디어입니다. "
        "실제 행사에서 진행되는지 운영자에게 확인해 주세요."
    )

# -----------------------------
# 긴급상황 대처법
# -----------------------------
elif st.session_state.page == "🚨 긴급상황 대처법":
    st.title("🚨 행사장 긴급상황 대처법")
    st.warning(
        "위급한 상황에서는 자신의 안전을 먼저 확보하고 "
        "현장 안전요원과 관계 기관의 안내를 따르세요."
    )

    with st.expander("🚑 응급환자가 발생했을 때", expanded=True):
        st.markdown("""
        1. 주변이 안전한지 먼저 확인해요.
        2. 현장 안전요원에게 즉시 도움을 요청해요.
        3. 긴급한 응급상황은 **119**에 신고해요.
        4. 환자를 함부로 옮기지 말고, 신고자의 안내에 따라요.
        5. 의식과 호흡을 확인할 수 있다면 신고 접수자의 지시에 따라요.
        """)

    with st.expander("🔥 화재 또는 대피 안내가 있을 때"):
        st.markdown("""
        1. 주변 사람에게 알리고 안전한 방향으로 대피해요.
        2. 엘리베이터를 이용하지 말고 안내된 대피로를 이용해요.
        3. 소지품을 챙기느라 대피를 늦추지 않아요.
        4. 안전한 장소에서 119에 신고하고 안내를 따라요.
        """)

    with st.expander("🧒 미아 또는 보호자와 떨어졌을 때"):
        st.markdown("""
        1. 안전한 곳에서 멈추고 가까운 행사 안내소나 안전요원을 찾아요.
        2. 보호자와 연락할 수 있다면 전화해요.
        3. 모르는 사람을 따라가지 말고 공식 안전요원의 도움을 받아요.
        4. 위험하거나 긴급한 상황이면 112 또는 119에 도움을 요청해요.
        """)

    with st.expander("🎒 분실물이 생겼을 때"):
        st.markdown("""
        1. 행사장 안내소 또는 공식 분실물 접수처에 문의해요.
        2. 분실 장소와 물건의 특징을 설명해요.
        3. 신분증, 카드 등 중요한 물건은 분실 신고도 확인해요.
        """)

    st.subheader("☎️ 긴급 연락처")
    c1, c2 = st.columns(2)
    c1.metric("119", "화재·구급·구조")
    c2.metric("112", "경찰 신고")

    st.caption(
        "이 안내는 일반적인 행동 요령입니다. "
        "실제 현장에서는 현장 방송과 신고 접수자의 지시를 우선하세요."
    )

# -----------------------------
# 행사장 경로 및 위치
# -----------------------------
elif st.session_state.page == "🗺️ 행사장 경로 및 위치":
    st.title("🗺️ 행사장 경로 및 위치")
    st.write("행사장 주소를 입력하고 지도에서 위치와 이동 경로를 확인해 보세요.")

    address = st.text_input(
        "📍 행사장 주소 또는 장소명",
        value=st.session_state.market_address,
        placeholder="예: 서울특별시 서울광장",
    )

    if st.button("📌 행사장 위치 확인", use_container_width=True):
        if address.strip():
            st.session_state.market_address = address.strip()
            st.session_state.map_search = quote_plus(address.strip())
        else:
            st.warning("행사장 주소나 장소명을 입력해 주세요.")

    current_address = st.session_state.market_address
    map_query = quote_plus(current_address)

    st.markdown("### 📍 행사장 정보")
    st.info(f"검색할 장소: {current_address}")

    map_url = f"https://www.google.com/maps/search/?api=1&query={map_query}"
    route_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={map_query}"
    )

    st.link_button("🌐 지도에서 위치 보기", map_url, use_container_width=True)
    st.link_button("🚶 이동 경로 확인하기", route_url, use_container_width=True)

    st.caption(
        "기본 장소는 예시입니다. 실제 행사장 주소를 입력해야 "
        "정확한 장소를 검색할 수 있어요. 이동 경로는 지도 서비스에서 확인하세요."
    )

    st.subheader("🧭 행사장에서 찾아볼 곳")
    locations = [
        ("🚪 입구", "입장 및 출구 안내"),
        ("ℹ️ 안내소", "행사 안내와 분실물 문의"),
        ("🚻 화장실", "가까운 화장실 위치 확인"),
        ("🚑 응급지원", "응급상황 시 안전요원에게 문의"),
        ("🗑️ 쓰레기통", "분리배출 및 쓰레기 처리"),
    ]

    for title, detail in locations:
        st.markdown(f"- **{title}** — {detail}")

    st.info(
        "행사장 내부의 실제 부스 배치도는 별도로 제공되지 않으므로, "
        "현장 안내판과 운영요원의 안내를 함께 확인해 주세요."
    )

# -----------------------------
# 공통 하단
# -----------------------------
st.divider()
st.caption(
    "🛍️ 편안하게 플리마켓 즐기는 법! | "
    "즐거운 쇼핑과 안전한 관람을 위한 안내 앱"
)
