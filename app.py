```python
import streamlit as st
import pandas as pd
import urllib.parse
import urllib.request
import urllib.error
import json


# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="FESTA MAP | 행사장 길찾기",
    page_icon="🎪",
    layout="wide",
)


# ==========================================
# 2. 디자인
# ==========================================
st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background-color: #F7F7FC;
    }

    .hero {
        background: linear-gradient(120deg, #5945E8, #9575FF);
        padding: 35px;
        border-radius: 24px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        font-family: 'Jua', sans-serif;
        font-size: 42px;
        margin-bottom: 12px;
    }

    .hero p {
        font-size: 16px;
        margin-bottom: 0;
    }

    .card {
        background: white;
        border: 1px solid #E8E8F3;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 15px;
    }

    .badge {
        display: inline-block;
        background: #EEEAFE;
        color: #5945E8;
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: bold;
    }

    .muted {
        color: #77778A;
        font-size: 13px;
    }

    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. 장소 검색
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def find_place(query):
    """
    OpenStreetMap Nominatim으로 장소를 검색한다.

    검색 결과:
        {
            "name": 장소 이름,
            "lat": 위도,
            "lon": 경도
        }

    검색 실패 시 None을 반환한다.
    """
    query = query.strip()

    if not query:
        return None

    params = urllib.parse.urlencode({
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "kr",
    })

    url = (
        "https://nominatim.openstreetmap.org/search?"
        + params
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "FestaMapEducationalApp/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=15,
        ) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        if not data:
            return None

        item = data[0]

        return {
            "name": item.get("display_name", query),
            "lat": float(item["lat"]),
            "lon": float(item["lon"]),
        }

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        ValueError,
        KeyError,
        IndexError,
        json.JSONDecodeError,
    ):
        return None


# ==========================================
# 4. 상단 배너
# ==========================================
st.markdown(
    """
    <div class="hero">
        <div style="font-weight:bold; letter-spacing:2px;">
            FIND YOUR FESTIVAL
        </div>
        <h1>🎪 FESTA MAP</h1>
        <p>
            가고 싶은 행사장을 검색하고,
            쉽고 빠르게 위치를 확인해 보세요!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 5. 사이드바
# ==========================================
with st.sidebar:
    st.markdown("## 🎨 FESTA MAP")
    st.caption("행사장 경로를 쉽게 알려주는 페이지")

    st.divider()

    st.markdown("### 💡 이용 방법")
    st.markdown(
        """
        **STEP 1**
        
        행사장 이름을 입력해요.
        
        **STEP 2**
        
        위치 검색 버튼을 눌러요.
        
        **STEP 3**
        
        지도에서 위치를 확인해요.
        
        **STEP 4**
        
        길 찾기 버튼으로 이동 경로를 확인해요.
        """
    )

    st.divider()

    st.markdown("### 📌 검색 팁")
    st.caption(
        "행사장 이름만 입력하는 것보다 "
        "지역명이나 도로명 주소를 함께 입력하면 "
        "정확한 위치를 찾는 데 도움이 됩니다."
    )


# ==========================================
# 6. 행사장 검색 화면
# ==========================================
st.markdown("## 🔎 어디로 가고 싶나요?")
st.write(
    "행사장 이름이나 주소를 입력하면 위치를 찾아줄게요."
)

event_name = st.text_input(
    "🎪 행사장 이름",
    placeholder="예: 서울특별시 중구 플리마켓",
    key="event_name",
)

st.markdown("**✨ 이런 장소를 검색해 보세요**")

suggestion_columns = st.columns(3)

suggestions = [
    ("🛍️ 플리마켓", "서울 플리마켓"),
    ("🎉 축제", "서울 축제 행사장"),
    ("🎨 전시회", "서울 전시회"),
]

for index, (label, value) in enumerate(suggestions):
    with suggestion_columns[index]:
        if st.button(
            label,
            use_container_width=True,
            key=f"suggestion_{index}",
        ):
            st.session_state["event_name"] = value
            st.rerun()


st.markdown("### 🚶 어디에서 출발하나요?")

start_name = st.text_input(
    "출발지",
    placeholder="예: 서울역 또는 학교 이름",
    key="start_name",
)

st.caption(
    "출발지를 모른다면 행사장만 먼저 검색해도 괜찮아요."
)

search_clicked = st.button(
    "🗺️ 행사장 위치 찾기",
    type="primary",
    use_container_width=True,
)


# ==========================================
# 7. 검색 처리
# ==========================================
if search_clicked:
    if not event_name.strip():
        st.warning(
            "행사장 이름을 입력해 주세요."
        )

    else:
        with st.spinner(
            "행사장의 위치를 찾고 있어요..."
        ):
            event_result = find_place(event_name)

        if event_result is None:
            st.error(
                "장소를 찾지 못했어요. "
                "행사장 이름에 지역명이나 주소를 추가하거나 "
                "잠시 후 다시 시도해 주세요."
            )

        else:
            st.session_state["event_result"] = event_result
            st.session_state["event_query"] = event_name.strip()

            # 출발지가 입력되었다면 함께 검색
            if start_name.strip():
                with st.spinner(
                    "출발지의 위치도 찾고 있어요..."
                ):
                    start_result = find_place(start_name)

                if start_result is None:
                    st.session_state.pop(
                        "start_result", None
                    )
                    st.warning(
                        "행사장 위치는 찾았지만 출발지는 찾지 못했어요. "
                        "출발지 이름이나 주소를 확인해 주세요."
                    )
                else:
                    st.session_state["start_result"] = start_result
                    st.session_state["start_query"] = start_name.strip()

            else:
                st.session_state.pop(
                    "start_result", None
                )
                st.session_state.pop(
                    "start_query", None
                )


# ==========================================
# 8. 검색 결과
# ==========================================
if "event_result" in st.session_state:
    event = st.session_state["event_result"]

    st.divider()
    st.markdown("## 📍 행사장 검색 결과")

    st.markdown(
        """
        <div class="card">
            <span class="badge">DESTINATION</span>
            <h3>🎪 찾은 행사장</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("행사장 위치를 찾았어요!")

    st.write("**검색된 장소 주소**")
    st.write(event["name"])

    st.caption(
        f'위도: {event["lat"]:.5f} / '
        f'경도: {event["lon"]:.5f}'
    )

    # 지도에는 행사장과 검색에 성공한 출발지를 표시
    locations = [
        {
            "latitude": event["lat"],
            "longitude": event["lon"],
        }
    ]

    if "start_result" in st.session_state:
        start = st.session_state["start_result"]

        st.markdown("### 🚶 출발지")

        st.write(start["name"])

        locations.append({
            "latitude": start["lat"],
            "longitude": start["lon"],
        })

    st.markdown("### 🗺️ 지도에서 위치 확인")

    try:
        map_df = pd.DataFrame(locations)

        st.map(
            map_df,
            latitude="latitude",
            longitude="longitude",
            size=120,
        )

    except Exception:
        st.warning(
            "앱 안에서 지도를 표시하지 못했어요. "
            "아래의 외부 지도 버튼을 이용해 주세요."
        )

    st.caption(
        "지도에는 검색한 장소의 위치가 표시됩니다. "
        "실제 도로 경로와 이동 시간은 외부 지도에서 확인해 주세요."
    )

    # 행사장 위치를 확인할 수 있는 외부 지도
    destination_params = urllib.parse.urlencode({
        "api": "1",
        "query": event["name"],
    })

    destination_url = (
        "https://www.google.com/maps/search/?"
        + destination_params
    )

    st.link_button(
        "📍 Google 지도에서 행사장 보기",
        destination_url,
        use_container_width=True,
    )

    # 출발지가 있으면 길 찾기 링크 표시
    if (
        "start_result" in st.session_state
        and "start_query" in st.session_state
    ):
        route_params = urllib.parse.urlencode({
            "api": "1",
            "origin": st.session_state["start_query"],
            "destination": st.session_state["event_query"],
            "travelmode": "transit",
        })

        route_url = (
            "https://www.google.com/maps/dir/?"
            + route_params
        )

        st.link_button(
            "🧭 출발지에서 행사장까지 길 찾기",
            route_url,
            use_container_width=True,
        )

    else:
        st.info(
            "출발지를 입력하면 출발지에서 행사장까지 "
            "길 찾기를 이용할 수 있어요."
        )

    st.markdown(
        """
        <div class="card">
            <h4>💡 방문 전 확인해 주세요</h4>
            <p>
                행사장 이름이 비슷한 다른 장소일 수 있으니
                주소가 실제 행사 장소와 일치하는지 확인해 주세요.
                행사 날짜와 운영 시간도 주최 측의 안내를 확인하는 것이 좋아요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 9. 검색 전 안내 화면
# ==========================================
else:
    st.divider()
    st.markdown("## ✨ FESTA MAP으로 할 수 있는 일")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h2>🔍</h2>
                <h4>간편한 검색</h4>
                <p>
                    행사장 이름이나 주소를 입력해서
                    장소를 찾아보세요.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h2>🗺️</h2>
                <h4>위치 확인</h4>
                <p>
                    지도에서 행사장이 어디에 있는지
                    확인할 수 있어요.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h2>🧭</h2>
                <h4>길 찾기</h4>
                <p>
                    외부 지도에서 출발지부터 행사장까지
                    이동 경로를 확인해요.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card">
            <h3>🎪 어디든 쉽게 찾아가기!</h3>
            <p>
                플리마켓, 지역 축제, 전시회 등
                가고 싶은 행사장의 이름을 입력해 보세요.
            </p>
            <p class="muted">
                인터넷 연결이 필요하며, 장소 검색 결과는
                실제 행사장 정보와 다를 수 있습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 10. 하단
# ==========================================
st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#77778A; padding:12px;">
        <strong>🎪 FESTA MAP</strong><br>
        행사장으로 가는 길을 더 쉽고 즐겁게!<br>
        <small>
            장소 검색: OpenStreetMap Nominatim
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)
```
