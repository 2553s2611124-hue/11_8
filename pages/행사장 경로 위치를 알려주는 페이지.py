import os
import streamlit as st
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="스마트 행사장 통합 안내 Center",
    page_icon="🎪",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. 행사장 기초 데이터 설정 (필요에 따라 수정 가능)
# -----------------------------------------------------------------------------
VENUE_INFO = {
    "title": "2026 글로벌 테크 박람회 (Tech Expo 2026)",
    "date": "2026년 10월 20일(화) ~ 10월 22일(목)",
    "location": "코엑스(COEX) Hall A & B",
    "operating_hours": "10:00 - 18:00",
    "emergency_contact": "02-1234-5678 (운영본부)"
}

SECTIONS = {
    "A구역 (메인 스테이지)": "키노트 강연, 개막식, 패널 토론 진행",
    "B구역 (전시 & 체험존)": "신기술 스타트업 부스 및 스폰서 체험관",
    "C구역 (네트워킹 라운지)": "참가자 및 바이어 간 비즈니스 미팅 공간 (음료 제공)",
    "D구역 (푸드코트 & 편의시설)": "식음료 판매대, 휴게 공간, 의무실",
    "안내데스크 / 의무실": "Hall A 입구 우측 위치 (응급 처치 및 분실물 센터)"
}

PROGRAM_SCHEDULE = [
    {"time": "10:00 - 11:00", "program": "개막식 및 키노트 연설", "location": "A구역 메인 스테이지"},
    {"time": "11:30 - 13:00", "program": "AI & 로보틱스 세션", "location": "A구역 메인 스테이지"},
    {"time": "13:00 - 14:00", "program": "점심 시간 & 자유 관람", "location": "전 전체"},
    {"time": "14:00 - 16:30", "program": "스타트업 피칭 데모데이", "location": "B구역 피칭 무대"},
    {"time": "16:30 - 18:00", "program": "네트워킹 파티", "location": "C구역 라운지"}
]

# -----------------------------------------------------------------------------
# 3. Gemini AI 설정 및 유틸리티 함수
# -----------------------------------------------------------------------------
def get_gemini_response(prompt: str) -> str:
    """Gemini API를 호출하여 행사장 관련 답변을 생성하는 함수"""
    # Streamlit Secrets 또는 환경 변수에서 API 키 확인
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    
    if not api_key:
        return "⚠️ Secrets 설정에 `GEMINI_API_KEY`가 등록되지 않았습니다. 관리자에게 문의하세요."
    
    try:
        genai.configure(api_key=api_key)
        # gemini-2.5-flash-lite 모델 호출
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # 시스템 프롬프트 부여하여 행사장 안내원 역할 수행
        system_context = f"""
        당신은 '{VENUE_INFO['title']}'의 친절한 행사장 안내 AI입니다.
        행사 정보:
        - 기간: {VENUE_INFO['date']}
        - 장소: {VENUE_INFO['location']}
        - 운영시간: {VENUE_INFO['operating_hours']}
        - 주요 구역: {SECTIONS}
        
        방문객의 질문에 맞춰 명확하고 정중하게 3문장 이내로 답변해주세요.
        만약 행사와 관련 없는 질문이라면 행사장 안내 도우미로서 행사 관련 문의를 부탁한다고 답변하세요.
        """
        
        response = model.generate_content(f"{system_context}\n\n질문: {prompt}")
        return response.text
    except Exception as e:
        return f"❌ AI 답변을 가져오는 중 오류가 발생했습니다: {str(e)}"

# -----------------------------------------------------------------------------
# 4. 화면 UI 구성
# -----------------------------------------------------------------------------
# 헤더 영역
st.title(f"🎪 {VENUE_INFO['title']}")
st.caption("행사장 통합 안내 및 AI 실시간 Q&A 서비스")

# 사이드바 (기본 정보)
st.sidebar.header("📌 행사 기본 정보")
st.sidebar.markdown(f"**🗓️ 일시:**\n{VENUE_INFO['date']}")
st.sidebar.markdown(f"**📍 장소:**\n{VENUE_INFO['location']}")
st.sidebar.markdown(f"**⏰ 운영시간:**\n{VENUE_INFO['operating_hours']}")
st.sidebar.markdown(f"**🚨 비상 연락처:**\n{VENUE_INFO['emergency_contact']}")
st.sidebar.divider()
st.sidebar.info("💡 팁: 행사장에 관한 무엇이든 탭에서 AI 스마트 안내원에게 물어보세요!")

# 메인 탭 구획
tab1, tab2, tab3, tab4 = st.tabs(["🏛️ 구역 및 시설 안내", "📅 프로그램 일정", "🤖 AI 스마트 안내원", "❓ 자주 묻는 질문(FAQ)"])

# -----------------------------------------------------------------------------
# 탭 1: 구역 및 시설 안내
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("🗺️ 행사장 구역 안내")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_section = st.selectbox(
            "확인하고 싶은 구역을 선택하세요:",
            list(SECTIONS.keys())
        )
        if selected_section:
            st.success(f"**{selected_section}**")
            st.write(SECTIONS[selected_section])
            
    with col2:
        st.subheader("💡 시설 이용 안내")
        st.write("- **Free Wi-Fi:** `TechExpo_Guest` (PW: `expo2026!`)")
        st.write("- **물품 보관함:** Hall A 입구 좌측 위치 (무료 이용)")
        st.write("- **주차 지원:** 안내데스크에서 등록 시 3시간 무료")

# -----------------------------------------------------------------------------
# 탭 2: 프로그램 일정
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("📅 주요 타임테이블")
    st.dataframe(
        PROGRAM_SCHEDULE,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 탭 3: AI 스마트 안내원 (Gemini 연동)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("🤖 AI 행사장 스마트 안내원")
    st.write("행사장 동선, 시설 위치, 기타 궁금한 점을 질문해 보세요!")
    
    # 예시 질문 버튼
    st.markdown("**💡 추천 질문 예시:**")
    example_cols = st.columns(3)
    user_query = ""
    
    if example_cols[0].button("화장실과 편의시설 위치는?"):
        user_query = "화장실과 편의시설 위치 알려줘"
    elif example_cols[1].button("주차 등록은 어디서 하나요?"):
        user_query = "주차 등록 어디서 해?"
    elif example_cols[2].button("점심 식사 할 수 있는 곳은?"):
        user_query = "점심 식사 할 곳 알려줘"
        
    # 질문 입력 폼
    input_query = st.text_input(
        "질문을 입력하세요:",
        value=user_query,
        placeholder="예: 메인 스테이지는 어디에 있나요?"
    )
    
    if st.button("질문하기", type="primary"):
        if input_query.strip():
            with st.spinner("AI가 행사장 정보를 확인하는 중입니다..."):
                answer = get_gemini_response(input_query)
                st.markdown("### 💬 AI 답변")
                st.info(answer)
        else:
            st.warning("질문을 입력해 주세요.")

# -----------------------------------------------------------------------------
# 탭 4: FAQ 및 응급 대처
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("❓ 자주 묻는 질문")
    
    with st.expander("Q. 재입장이 가능한가요?"):
        st.write("네, 입구에서 발급받은 네임택/명찰을 착용하고 계시면 당일 자유롭게 재입장이 가능합니다.")
        
    with st.expander("Q. 유모차나 휠체어 대여가 가능한가요?"):
        st.write("Hall A 안내데스크에서 신분증 확인 후 무료로 대여하실 수 있습니다. (수량 소한)")
        
    with st.expander("Q. 비상 상황이나 분실물이 발생하면 어떻게 하나요?"):
        st.write("즉시 운영본부(02-1234-5678)로 연락하시거나 가장 가까운 안내데스크 스태프에게 알려주시기 바랍니다.")
