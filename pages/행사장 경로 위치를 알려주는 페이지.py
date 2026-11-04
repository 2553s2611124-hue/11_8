import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정 및 스타일링
# ==========================================
st.set_page_config(
    page_title="행사장 오시는 길 & 경로 안내",
    page_icon="📍",
    layout="wide"
)

# 커스텀 CSS (안내 카드 및 스타일링)
st.markdown("""
    <style>
    .venue-card {
        background-color: #F0FDF4;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #16A34A;
        margin-bottom: 20px;
    }
    .transport-card {
        background-color: #F9FAFB;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 행사장 기본 정보 설정
# ==========================================
VENUE_NAME = "햇살가득 플리마켓 & 행사 잔디광장"
VENUE_ADDRESS = "서울특별시 성동구 뚝섬로 273 (서울숲 잔디광장)"
VENUE_LAT = 37.5444
VENUE_LON = 127.0374

# ==========================================
# 3. 사이드바 - 오시는 길 메뉴
# ==========================================
st.sidebar.title("📍 오시는 길 안내")
menu = st.sidebar.radio(
    "원하는 안내 메뉴를 선택하세요:",
    [
        "🗺️ 행사장 위치 & 지도 링크",
        "🚌 대중교통 & 주차 안내",
        "⏱️ 출발지별 소요시간 계산",
        "📌 행사장 내부 시설 배치도"
    ]
)

st.sidebar.divider()
st.sidebar.markdown(f"**📍 행사장:** {VENUE_NAME}")
st.sidebar.markdown(f"**🏢 주소:** {VENUE_ADDRESS}")
st.sidebar.markdown("⏰ **운영 시간:** 매주 토/일 11:00 ~ 17:00")

# ==========================================
# 4. 헤더 및 기본 배너
# ==========================================
st.title("📍 행사장 오시는 길 & 경로 위치 안내")
st.caption("방문하시는 모든 분들의 편리한 이동을 위해 상세 경로와 교통편을 안내해 드립니다.")

st.markdown(f"""
<div class="venue-card">
    <h3>🎪 {VENUE_NAME}</h3>
    <p><b>주소:</b> {VENUE_ADDRESS}</p>
    <p>💡 <b>방문 팁:</b> 주말에는 주차장이 혼잡할 수 있으니 <b>대중교통(지하철)</b> 이용을 권장합니다.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 메뉴별 기능 구현
# ==========================================

# ------------------------------------------
# [메뉴 1] 행사장 위치 & 지도 링크
# ------------------------------------------
if menu == "🗺️ 행사장 위치 & 지도 링크":
    st.subheader("🗺️ 지도 위치 및 길찾기 앱 바로가기")
    
    # 지도 표시 (Streamlit 내장 map 활용)
    map_data = pd.DataFrame({
        'lat': [VENUE_LAT],
        'lon': [VENUE_LON]
    })
    st.map(map_data, zoom=15)
    
    st.markdown("#### 🔗 내비게이션 / 지도 앱 바로열기")
    st.caption("스마트폰에서 아래 버튼을 클릭하시면 길찾기 화면으로 이동합니다.")
    
    col1, col2, col3 = st.columns(3)
    
    # 지도 앱 검색 링크
    kakao_map_url = f"https://map.kakao.com/link/search/{VENUE_ADDRESS.replace(' ', '%20')}"
    naver_map_url = f"https://map.naver.com/v5/search/{VENUE_ADDRESS.replace(' ', '%20')}"
    tmap_url = "https://tmap.co.kr"
    
    col1.link_button("💛 카카오맵에서 보기", kakao_map_url, use_container_width=True)
    col2.link_button("💚 네이버 지도에서 보기", naver_map_url, use_container_width=True)
    col3.link_button("🔴 TMAP 내비 연결", tmap_url, use_container_width=True)

# ------------------------------------------
# [메뉴 2] 대중교통 & 주차 안내
# ------------------------------------------
elif menu == "🚌 대중교통 & 주차 안내":
    st.subheader("🚌 수단별 오시는 길 상세 안내")
    
    tab1, tab2, tab3 = st.tabs(["🚇 지하철 이용", "🚌 버스 이용", "🚗 자차 및 주차장"])
    
    with tab1:
        st.markdown("""
        <div class="transport-card">
            <h4>🚇 수인분당선 서울숲역</h4>
            <ul>
                <li><b>출구:</b> 4번 출구로 나와 도보 3분 (약 200m)</li>
                <li><b>경로:</b> 출구 직진 ➡️ 잔디광장 입구 간판 확인 ➡️ 행사장 도착</li>
            </ul>
        </div>
        <div class="transport-card">
            <h4>🚇 2호선 뚝섬역</h4>
            <ul>
                <li><b>출구:</b> 8번 출구로 나와 도보 8분 (약 550m)</li>
                <li><b>경로:</b> 출구 나와 골목 직진 ➡️ 서울숲 방면 건너목 건너기 ➡️ 행사장 도착</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="transport-card">
            <h4>🚌 버스 정류장 안내</h4>
            <p><b>[서울숲 남문 정류장 하차 (도보 2분)]</b></p>
            <ul>
                <li><b>지선 버스:</b> 2014, 2224, 2413</li>
                <li><b>간선 버스:</b> 121, 141, 145, 148, 463</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
        <div class="transport-card">
            <h4>🚗 자차 및 주차장 안내</h4>
            <ul>
                <li><b>행사장 공영 주차장:</b> 서울숲 공영주차장 (24시간 운영)</li>
                <li><b>주차 요금:</b> 5분당 150원 (1시간 1,800원)</li>
                <li><b>주차 꿀팁:</b> 만차 시 인근 '성동구민종합체육센터 주차장' 이용 가능</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------
# [메뉴 3] 출발지별 소요시간 계산
# ------------------------------------------
elif menu == "⏱️ 출발지별 소요시간 계산":
    st.subheader("⏱️ 주요 출발지별 예상 소요시간 계산기")
    st.caption("출발 위치를 선택하면 행사장까지의 예상 이동 시간과 추천 경로를 확인하실 수 있습니다.")
    
    # 미리 설정된 거점 데이터
    route_data = {
        "강남역 (2호선/신분당선)": {"시간": "약 20분", "추천": "지하철 (강남역 ➡️ 선릉역 환승 ➡️ 서울숲역 하차)", "거리": "7.5km"},
        "홍대입구역 (2호선)": {"시간": "약 35분", "추천": "지하철 (2호선 뚝섬역 하차 후 도보)", "거리": "14.2km"},
        "서울역 (KTX/1호선)": {"시간": "약 25분", "추천": "지하철 (4호선 동대문역사문화공원 ➡️ 2호선 뚝섬역)", "거리": "9.1km"},
        "고속터미널역 (3/7/9호선)": {"시간": "약 25분", "추천": "지하철 (7호선 강남구청역 환승 ➡️ 서울숲역)", "거리": "8.3km"},
        "잠실역 (2호선/8호선)": {"시간": "약 18분", "추천": "지하철 (2호선 뚝섬역 하차)", "거리": "6.8km"}
    }
    
    selected_origin = st.selectbox("출발지 거점을 선택하세요:", list(route_data.keys()))
    
    if selected_origin:
        info = route_data[selected_origin]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("예상 소요시간", info["시간"])
        c2.metric("이동 거리", info["거리"])
        c3.metric("추천 수단", "지하철 이용")
        
        st.info(f"💡 **추천 경로:** {info['추천']}")

# ------------------------------------------
# [메뉴 4] 행사장 내부 시설 배치도
# ------------------------------------------
elif menu == "📌 행사장 내부 시설 배치도":
    st.subheader("📌 행사장 내부 구역 및 편의시설 배치도")
    st.caption("행사장 내 부스 구역, 안내소, 화장실, 쉼터의 위치를 확인하세요.")
    
    # 배치도 안내 데이터
    zones = [
        {"구역명": "🎪 메인 무대 / 개회식장", "위치": "잔디광장 중앙", "비고": "공연 및 경품 추첨 진행"},
        {"구역명": "🛍️ 플리마켓 셀러 부스 (A~C구역)", "위치": "잔디광장 동측 산책로", "비고": "수제 소품, 디저트, 잡화"},
        {"구역명": "ℹ️ 종합 안내소 & 의무실", "위치": "행사장 입구 정면", "비고": "리플렛 배부 및 분실물 센터"},
        {"구역명": "🚻 공용 화장실", "위치": "입구 좌측 건물 및 공원 중앙", "비고": "남/녀 구분 및 장애인 편의시설"},
        {"구역명": "☕ 쉼터 & 푸드트럭 구역", "위치": "잔디광장 서측 야외 테이블", "비고": "취식 및 휴식 공간"}
    ]
    
    zone_df = pd.DataFrame(zones)
    st.table(zone_df)
