
import streamlit as st

st.set_page_config(
    page_title="행사 한눈에",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 디자인 ----------
st.markdown("""
<style>
.stApp {
    background-color: #F7F8FC;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(120deg, #5267D9, #8294F5);
    color: white;
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 24px;
}
.hero h1 {
    color: white;
    font-size: 34px;
    margin-bottom: 8px;
}
.hero p {
    color: #F0F2FF;
    font-size: 16px;
}
.info-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E8EAF3;
    margin-bottom: 12px;
}
.small-label {
    color: #6875D9;
    font-weight: 700;
    font-size: 13px;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #E8EAF3;
}
</style>
""", unsafe_allow_html=True)

# ---------- 예시 데이터 ----------
NOTICES = [
    {
        "category": "안전",
        "title": "행사장 안전 수칙",
        "description": "뛰거나 다른 참가자를 밀지 마세요. 사람이 많이 모이는 곳에서는 안내 요원의 지시에 따라 주세요.",
        "level": "필수 확인"
    },
    {
        "category": "시설",
        "title": "시설 및 부스 이용",
        "description": "각 부스에 게시된 이용 방법을 확인하고, 장비나 전시물을 임의로 만지지 마세요.",
        "level": "이용 안내"
    },
    {
        "category": "환경",
        "title": "쓰레기 배출",
        "description": "쓰레기는 지정된 분리배출 장소에 버려 주세요. 행사장을 깨끗하게 이용해 주세요.",
        "level": "참여 안내"
    },
    {
        "category": "분실물",
        "title": "분실물 확인",
        "description": "물건을 잃어버렸다면 행사 운영본부에 문의하세요. 주운 물건도 운영본부에 전달해 주세요.",
        "level": "도움 안내"
    },
    {
        "category": "긴급 상황",
        "title": "위급 상황 발생 시",
        "description": "가까운 행사 진행 요원에게 즉시 알리고 안내에 따라 주세요. 긴급한 상황에는 112 또는 119에 연락하세요.",
        "level": "중요"
    },
    {
        "category": "이용",
        "title": "행사장 이용 에티켓",
        "description": "다른 참가자를 배려하고, 줄을 설 때는 순서를 지켜 주세요. 큰 소음으로 주변에 피해를 주지 않도록 해 주세요.",
        "level": "이용 안내"
    },
]

EVENTS = [
    {
        "category": "공연",
        "title": "오프닝 공연",
        "time": "10:00~10:30",
        "place": "메인 무대",
        "description": "행사의 시작을 알리는 신나는 오프닝 공연입니다.",
        "tag": "공연"
    },
    {
        "category": "체험",
        "title": "나만의 키링 만들기",
        "time": "11:00~16:00",
        "place": "체험 부스 A",
        "description": "다양한 재료를 활용해 나만의 키링을 만들어 보세요.",
        "tag": "체험"
    },
    {
        "category": "참여",
        "title": "스탬프 미션",
        "time": "10:30~16:00",
        "place": "행사장 곳곳",
        "description": "지정된 장소에서 스탬프를 모으며 행사장을 둘러보세요.",
        "tag": "참여 이벤트"
    },
    {
        "category": "공연",
        "title": "동아리 무대",
        "time": "13:00~14:00",
        "place": "메인 무대",
        "description": "참가자들이 준비한 다양한 공연을 감상할 수 있습니다.",
        "tag": "공연"
    },
    {
        "category": "체험",
        "title": "포토존 인증 이벤트",
        "time": "10:00~16:00",
        "place": "포토존",
        "description": "포토존에서 기념사진을 촬영해 행사 추억을 남겨 보세요.",
        "tag": "체험"
    },
    {
        "category": "참여",
        "title": "행운의 뽑기",
        "time": "14:00~15:30",
        "place": "이벤트 부스",
        "description": "운영 요원의 안내에 따라 참여할 수 있는 이벤트입니다.",
        "tag": "참여 이벤트"
    },
]


def show_notice(item):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="small-label">
                {item['category']} · {item['level']}
            </div>
            <h3>{item['title']}</h3>
            <p>{item['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_event(item):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="small-label">{item['tag']}</div>
            <h3>🎉 {item['title']}</h3>
            <p>🕒 {item['time']}</p>
            <p>📍 {item['place']}</p>
            <p>{item['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- 사이드바 ----------
st.sidebar.title("🎪 행사 한눈에")
st.sidebar.caption("행사 안내 통합 서비스")
page = st.sidebar.radio(
    "메뉴 선택",
    ["홈", "주의사항", "이벤트 안내", "행사 정보"],
    index=0
)

st.sidebar.divider()
st.sidebar.info(
    "실제 행사에 사용하기 전에는 "
    "운영 시간과 안내 내용을 확인해 주세요."
)

# ---------- 홈 ----------
if page == "홈":
    st.markdown("""
    <div class="hero">
        <h1>🎪 행사 한눈에</h1>
        <p>즐거운 행사를 위한 모든 안내를 한곳에서!</p>
        <p>주의사항을 확인하고, 다양한 이벤트를 찾아보세요.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("확인할 주의사항", f"{len(NOTICES)}개")
    with col2:
        st.metric("준비된 이벤트", f"{len(EVENTS)}개")

    st.subheader("📌 먼저 확인해 주세요")
    st.warning(
        "행사장 안전 수칙을 먼저 확인하고 "
        "운영 요원의 안내에 따라 주세요."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛡️ 주의사항")
        st.write("안전 수칙과 시설 이용 정보를 확인하세요.")
        if st.button("주의사항 확인하기", use_container_width=True):
            st.session_state["page"] = "주의사항"
            st.rerun()

    with col2:
        st.markdown("### 🎉 이벤트 안내")
        st.write("공연과 체험, 참여 이벤트를 찾아보세요.")
        if st.button("이벤트 둘러보기", use_container_width=True):
            st.session_state["page"] = "이벤트 안내"
            st.rerun()

    st.subheader("✨ 추천 이벤트")
    for event in EVENTS[:3]:
        show_event(event)

# ---------- 주의사항 ----------
elif page == "주의사항":
    st.title("🛡️ 행사장 주의사항")
    st.write("안전하고 즐거운 행사 참여를 위해 확인해 주세요.")

    categories = ["전체"] + list(dict.fromkeys(
        item["category"] for item in NOTICES
    ))
    selected_category = st.selectbox(
        "항목별로 보기",
        categories,
        key="notice_category"
    )
    keyword = st.text_input(
        "🔎 주의사항 검색",
        placeholder="예: 안전, 쓰레기, 분실물"
    )

    filtered = []
    for item in NOTICES:
        if selected_category != "전체" and item["category"] != selected_category:
            continue
        search_text = (
            item["title"] + " " +
            item["description"] + " " +
            item["category"]
        )
        if keyword.strip() and keyword.strip().lower() not in search_text.lower():
            continue
        filtered.append(item)

    st.caption(f"검색 결과 {len(filtered)}개")

    if filtered:
        for item in filtered:
            show_notice(item)
    else:
        st.info("검색 결과가 없습니다. 다른 단어로 검색해 주세요.")

# ---------- 이벤트 안내 ----------
elif page == "이벤트 안내":
    st.title("🎉 이벤트 안내")
    st.write("관심 있는 이벤트를 선택해 자세한 정보를 확인하세요.")

    categories = ["전체"] + list(dict.fromkeys(
        item["category"] for item in EVENTS
    ))
    selected_category = st.selectbox(
        "이벤트 종류",
        categories,
        key="event_category"
    )
    keyword = st.text_input(
        "🔎 이벤트 검색",
        placeholder="예: 공연, 키링, 포토존"
    )

    filtered = []
    for item in EVENTS:
        if selected_category != "전체" and item["category"] != selected_category:
            continue
        search_text = (
            item["title"] + " " +
            item["description"] + " " +
            item["place"] + " " +
            item["category"]
        )
        if keyword.strip() and keyword.strip().lower() not in search_text.lower():
            continue
        filtered.append(item)

    st.caption(f"이벤트 {len(filtered)}개")

    if filtered:
        for item in filtered:
            with st.expander(f"🎊 {item['title']}"):
                st.write(f"**종류:** {item['category']}")
                st.write(f"**시간:** {item['time']}")
                st.write(f"**장소:** {item['place']}")
                st.write(item["description"])
    else:
        st.info("조건에 맞는 이벤트가 없습니다.")

# ---------- 행사 정보 ----------
elif page == "행사 정보":
    st.title("ℹ️ 행사 정보")
    st.write("아래 정보는 수정해서 사용할 수 있는 예시입니다.")

    st.markdown("""
    <div class="info-card">
        <h3>📅 행사 일정</h3>
        <p>행사 날짜: 실제 일정 입력 필요</p>
        <p>운영 시간: 실제 운영 시간 입력 필요</p>
    </div>
    <div class="info-card">
        <h3>📍 행사 장소</h3>
        <p>행사장 이름과 주소를 입력해 주세요.</p>
        <p>정확한 장소와 이동 경로는 공식 안내를 확인해 주세요.</p>
    </div>
    <div class="info-card">
        <h3>☎️ 문의 안내</h3>
        <p>행사 운영본부: 실제 연락처 입력 필요</p>
        <p>긴급 상황: 112 또는 119</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("행사 한눈에 · 행사 안내를 쉽고 빠르게")

