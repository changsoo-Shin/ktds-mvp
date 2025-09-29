"""
SmartDoc AI - 메인 Streamlit 애플리케이션
지능형 문서 분석 어시스턴트
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# 로컬 모듈 임포트
from document_processor import DocumentProcessor
from search_engine import SearchEngine
from ai_assistant import AIAssistant

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="SmartDoc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .ai-message {
        background-color: #f3e5f5;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """세션 상태 초기화"""
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'search_engine' not in st.session_state:
        st.session_state.search_engine = None
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = None

def main():
    """메인 애플리케이션"""
    initialize_session_state()
    
    # 헤더
    st.markdown('<h1 class="main-header">📄 SmartDoc AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">지능형 문서 분석 어시스턴트</p>', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("📋 메뉴")
        
        # 메인 기능 탭
        tab1, tab2, tab3 = st.tabs(["📄 문서", "💬 채팅", "⚙️ 설정"])
        
        with tab1:
            st.subheader("문서 관리")
            
            # 문서 업로드
            uploaded_files = st.file_uploader(
                "문서 업로드",
                type=['pdf', 'docx', 'txt', 'xlsx', 'ppt', 'pptx', 'hwp', 'ipynb'],
                accept_multiple_files=True,
                help="PDF, Word, Excel, PowerPoint, 한글, 텍스트, Jupyter Notebook 파일을 업로드하세요"
            )
            
            if uploaded_files:
                process_documents(uploaded_files)
            
            # 업로드된 문서 목록
            if st.session_state.documents:
                st.subheader("업로드된 문서")
                for i, doc in enumerate(st.session_state.documents):
                    with st.expander(f"📄 {doc['name']}"):
                        st.write(f"**크기**: {doc['size']} KB")
                        st.write(f"**업로드 시간**: {doc['upload_time']}")
                        if st.button(f"삭제", key=f"delete_{i}"):
                            st.session_state.documents.pop(i)
                            st.rerun()
        
        with tab2:
            st.subheader("채팅 설정")
            st.info("문서를 먼저 업로드한 후 채팅을 시작하세요.")
            
        with tab3:
            st.subheader("설정")
            show_settings()
    
    # 메인 컨텐츠 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔍 문서 검색")
        show_search_interface()
    
    with col2:
        st.header("💬 AI 어시스턴트")
        show_chat_interface()

def process_documents(uploaded_files):
    """문서 처리"""
    processor = DocumentProcessor()
    
    for uploaded_file in uploaded_files:
        # 파일 정보 저장
        file_info = {
            'name': uploaded_file.name,
            'size': round(uploaded_file.size / 1024, 2),
            'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': None
        }
        
        try:
            # 문서 내용 추출
            content = processor.extract_content(uploaded_file)
            file_info['content'] = content
            
            # 세션 상태에 추가
            st.session_state.documents.append(file_info)
            
            st.success(f"✅ {uploaded_file.name} 처리 완료!")
            
        except Exception as e:
            st.error(f"❌ {uploaded_file.name} 처리 실패: {str(e)}")
    
    # 검색 엔진 및 AI 어시스턴트 초기화
    initialize_ai_components()

def initialize_ai_components():
    """AI 컴포넌트 초기화"""
    if st.session_state.documents:
        try:
            with st.spinner("AI 컴포넌트 초기화 중..."):
                # 검색 엔진 초기화
                try:
                    st.session_state.search_engine = SearchEngine()
                    st.session_state.search_engine.add_documents(st.session_state.documents)
                    st.info("✅ 검색 엔진 초기화 완료")
                except Exception as search_error:
                    st.warning(f"⚠️ 검색 엔진 초기화 실패: {str(search_error)}")
                    st.info("검색 기능 없이 AI 어시스턴트만 사용됩니다.")
                    st.session_state.search_engine = None
                
                # AI 어시스턴트 초기화
                try:
                    st.session_state.ai_assistant = AIAssistant()
                    st.success("✅ AI 어시스턴트 초기화 완료!")
                except Exception as ai_error:
                    st.error(f"❌ AI 어시스턴트 초기화 실패: {str(ai_error)}")
                    return
                
                st.success("✅ AI 컴포넌트 초기화 완료!")
        except Exception as e:
            st.error(f"❌ AI 컴포넌트 초기화 실패: {str(e)}")
            st.info("환경 변수 설정을 확인해주세요.")

def show_search_interface():
    """검색 인터페이스 표시"""
    if not st.session_state.search_engine:
        st.info("문서를 먼저 업로드해주세요.")
        return
    
    search_query = st.text_input("검색어를 입력하세요:", placeholder="예: 인공지능, 데이터 분석...")
    
    if st.button("🔍 검색") and search_query:
        with st.spinner("검색 중..."):
            try:
                results = st.session_state.search_engine.search(search_query)
                display_search_results(results)
            except Exception as e:
                st.error(f"검색 실패: {str(e)}")

def display_search_results(results):
    """검색 결과 표시"""
    if not results:
        st.info("검색 결과가 없습니다.")
        return
    
    st.subheader(f"검색 결과 ({len(results)}개)")
    
    for i, result in enumerate(results):
        with st.expander(f"📄 결과 {i+1}: {result.get('title', '제목 없음')}"):
            st.write(f"**문서**: {result.get('source', '알 수 없음')}")
            st.write(f"**관련도**: {result.get('score', 0):.2f}")
            st.write("**내용**:")
            st.write(result.get('content', '내용 없음'))

def show_chat_interface():
    """채팅 인터페이스 표시"""
    if not st.session_state.ai_assistant:
        st.info("문서를 먼저 업로드해주세요.")
        return
    
    # 채팅 히스토리 표시
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 사용자:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # 채팅 입력
    user_input = st.text_input("질문을 입력하세요:", placeholder="문서에 대해 궁금한 것을 물어보세요...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💬 전송"):
            if user_input:
                process_chat_message(user_input)
    with col2:
        if st.button("🗑️ 채팅 초기화"):
            st.session_state.chat_history = []
            st.rerun()

def process_chat_message(user_input):
    """채팅 메시지 처리"""
    # 사용자 메시지 추가
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    try:
        with st.spinner("AI가 답변을 생성 중..."):
            # AI 어시스턴트에게 질문
            response = st.session_state.ai_assistant.ask_question(
                user_input, 
                st.session_state.documents,
                st.session_state.search_engine
            )
            
            # AI 응답 추가
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
            
    except Exception as e:
        st.error(f"답변 생성 실패: {str(e)}")

def show_settings():
    """설정 표시"""
    st.write("**Azure OpenAI 설정**")
    st.write(f"API 키 설정됨: {'✅' if os.getenv('AZURE_OPENAI_API_KEY') else '❌'}")
    st.write(f"엔드포인트: {os.getenv('AZURE_OPENAI_ENDPOINT', '설정되지 않음')}")
    
    st.write("**Azure AI Search 설정**")
    st.write(f"검색 키 설정됨: {'✅' if os.getenv('AZURE_SEARCH_API_KEY') else '❌'}")
    st.write(f"인덱스: {os.getenv('AZURE_SEARCH_INDEX_NAME', '설정되지 않음')}")

if __name__ == "__main__":
    main()
