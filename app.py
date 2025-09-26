import streamlit as st
import os
from datetime import datetime, timedelta
from travel_rag import TravelRAG
from image_analyzer import ImageAnalyzer
from weather_service import WeatherService

# 페이지 설정
st.set_page_config(
    page_title="🧳 AI 여행 플래너",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 헤더
    current_date = datetime.now().strftime("%Y년 %m월 %d일 (%A)")
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🧳 AI 여행 플래너</h1>
        <p>AI가 추천하는 맞춤 여행일정을 만들어보세요!</p>
        <p style="font-size: 14px; margin-top: 10px;">📅 오늘: {current_date}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바 - 기본 설정
    with st.sidebar:
        st.header("⚙️ 여행 설정")
        
        # 여행지 입력
        destination = st.text_input(
            "🏙️ 여행지",
            placeholder="예: 파리, 도쿄, 제주도",
            help="방문하고 싶은 도시나 지역을 입력하세요"
        )
        
        # 여행 시작일
        start_date = st.date_input(
            "📅 여행 시작일",
            value=datetime.now().date(),
            min_value=datetime.now().date(),
            help="여행을 시작할 날짜를 선택하세요"
        )
        
        # 여행 기간
        days = st.slider("📅 여행 기간 (일)", 1, 14, 3)
        
        # 여행 스타일
        travel_style = st.selectbox(
            "🎯 여행 스타일",
            ["관광 중심", "휴양 중심", "문화 체험", "맛집 탐방", "자연 탐험", "쇼핑"]
        )
        
        # 예산
        budget = st.selectbox(
            "💰 예산",
            ["저예산 (일 5만원 이하)", "중간 (일 5-10만원)", "고급 (일 10만원 이상)"]
        )
        
        # 여행 일정 미리보기
        if start_date and days:
            end_date = start_date + timedelta(days=days-1)
            st.markdown("---")
            st.markdown("### 📋 여행 일정 미리보기")
            st.info(f"**시작일:** {start_date.strftime('%Y년 %m월 %d일 (%A)')}\n\n**종료일:** {end_date.strftime('%Y년 %m월 %d일 (%A)')}\n\n**총 기간:** {days}일")
    
    # 메인 컨텐츠
    tab1, tab2, tab3 = st.tabs(["🗺️ 여행일정 생성", "📸 이미지 분석", "💬 AI 상담"])
    
    with tab1:
        st.header("🗺️ 맞춤 여행일정 생성")
        
        if destination:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🚀 여행일정 생성하기", type="primary", use_container_width=True):
                    with st.spinner("AI가 여행일정을 생성하고 있습니다..."):
                        try:
                            # 여행 RAG 시스템 초기화
                            travel_rag = TravelRAG()
                            
                            # 여행일정 생성
                            result = travel_rag.generate_itinerary(
                                destination=destination,
                                days=days,
                                interests=[travel_style],
                                budget=budget,
                                start_date=start_date
                            )
                            
                            if "error" not in result:
                                st.success("✅ 여행일정이 생성되었습니다!")
                                
                                # 결과 표시
                                st.markdown("### 📋 생성된 여행일정")
                                st.markdown(result["itinerary"])
                                
                                # 다운로드 버튼
                                st.download_button(
                                    label="📄 일정 다운로드",
                                    data=result["itinerary"],
                                    file_name=f"{destination}_여행일정_{days}일.txt",
                                    mime="text/plain"
                                )
                            else:
                                st.error(f"❌ 오류: {result['error']}")
                                
                        except Exception as e:
                            st.error(f"❌ 여행일정 생성 중 오류가 발생했습니다: {str(e)}")
            
            with col2:
                # 날씨 정보
                st.subheader("🌤️ 현재 날씨")
                if st.button("날씨 확인", use_container_width=True):
                    try:
                        weather_service = WeatherService()
                        weather = weather_service.get_current_weather(destination)
                        
                        if "error" not in weather:
                            st.markdown(f"""
                            <div class="success-box">
                                <h4>🌍 {weather['city']}, {weather['country']}</h4>
                                <p><strong>온도:</strong> {weather['temperature']}°C</p>
                                <p><strong>체감온도:</strong> {weather['feels_like']}°C</p>
                                <p><strong>날씨:</strong> {weather['description']}</p>
                                <p><strong>습도:</strong> {weather['humidity']}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("날씨 정보를 가져올 수 없습니다.")
                    except Exception as e:
                        st.warning("날씨 서비스를 사용할 수 없습니다.")
        else:
            st.info("👈 사이드바에서 여행지를 입력해주세요!")
    
    with tab2:
        st.header("📸 이미지로 여행지 추천")
        
        uploaded_file = st.file_uploader(
            "여행하고 싶은 장소의 사진을 업로드하세요",
            type=['png', 'jpg', 'jpeg'],
            help="AI가 이미지를 분석해서 유사한 여행지를 추천해드립니다"
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
            
            with col2:
                if st.button("🔍 이미지 분석하기", type="primary", use_container_width=True):
                    with st.spinner("이미지를 분석하고 있습니다..."):
                        try:
                            image_analyzer = ImageAnalyzer()
                            image_data = uploaded_file.read()
                            
                            analysis = image_analyzer.analyze_travel_image(image_data)
                            
                            if "error" not in analysis:
                                st.success("✅ 이미지 분석 완료!")
                                
                                st.markdown("### 📝 분석 결과")
                                st.write(f"**설명:** {analysis['caption']}")
                                
                                if analysis['tags']:
                                    st.write("**태그:**")
                                    for tag in analysis['tags'][:5]:  # 상위 5개만 표시
                                        st.write(f"- {tag['name']} ({tag['confidence']:.2f})")
                                
                                # 여행지 추천
                                suggestions = image_analyzer.suggest_destinations_from_image(analysis)
                                if suggestions:
                                    st.markdown("### 🎯 추천 여행지")
                                    for suggestion in suggestions:
                                        st.write(f"• {suggestion}")
                            else:
                                st.error(f"❌ 오류: {analysis['error']}")
                                
                        except Exception as e:
                            st.error(f"❌ 이미지 분석 중 오류가 발생했습니다: {str(e)}")
    
    with tab3:
        st.header("💬 AI 여행 상담")
        
        # 채팅 히스토리 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "안녕하세요! 🧳 AI 여행 플래너입니다. 어떤 여행에 대해 궁금한 것이 있으신가요?"}
            ]
        
        # 채팅 메시지 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 사용자 입력
        if prompt := st.chat_input("여행에 대해 질문해보세요..."):
            # 사용자 메시지 추가
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("AI가 답변을 생성하고 있습니다..."):
                    try:
                        travel_rag = TravelRAG()
                        
                        # 간단한 여행 상담 프롬프트
                        chat_prompt = f"""
                        당신은 친근한 여행 전문가입니다. 사용자의 질문에 대해 도움이 되는 답변을 해주세요.
                        
                        사용자 질문: {prompt}
                        
                        답변 시 다음을 고려해주세요:
                        - 친근하고 도움이 되는 톤
                        - 구체적이고 실용적인 조언
                        - 이모지를 적절히 사용
                        - 한국어로 답변
                        """
                        
                        response = travel_rag.llm.invoke(chat_prompt)
                        st.markdown(response.content)
                        
                        # AI 응답을 메시지에 추가
                        st.session_state.messages.append({"role": "assistant", "content": response.content})
                        
                    except Exception as e:
                        error_msg = f"죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요. (오류: {str(e)})"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
