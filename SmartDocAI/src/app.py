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
from utils import (
    load_documents_content_from_file, 
    save_documents_content_to_file,
    get_documents_directory
)

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
        # 기존 저장된 문서 로드
        docs_dir = get_documents_directory()
        documents_file = os.path.join(docs_dir, "documents_content.pkl")
        st.session_state.documents = load_documents_content_from_file(documents_file)
        
        # 문서가 있으면 AI 컴포넌트 자동 초기화
        if st.session_state.documents:
            initialize_ai_components()
    
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
                help="📄 PDF, Word, Excel, PowerPoint, 📝 한글(.hwp), 텍스트, Jupyter Notebook 파일을 업로드하세요"
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
                            save_documents()  # 문서 삭제 후 저장
                            st.rerun()
        
        with tab2:
            st.subheader("채팅 설정")
            if st.session_state.documents:
                st.success(f"✅ {len(st.session_state.documents)}개 문서가 업로드되어 있습니다.")
                if st.session_state.ai_assistant:
                    st.success("✅ AI 어시스턴트가 활성화되어 있습니다.")
                else:
                    st.warning("⚠️ AI 어시스턴트를 초기화하려면 환경 변수를 설정해주세요.")
            else:
                st.info("📄 문서를 업로드하면 AI 어시스턴트와 채팅할 수 있습니다.")
            
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
            # 한글 문서인 경우 특별 안내
            if uploaded_file.name.lower().endswith('.hwp'):
                st.info("🔄 한글 문서를 처리 중입니다. 복잡한 구조로 인해 시간이 다소 걸릴 수 있습니다...")
            
            # 문서 내용 추출
            content = processor.extract_content(uploaded_file)
            file_info['content'] = content
            
            # 세션 상태에 추가
            st.session_state.documents.append(file_info)
            
            # 한글 문서인 경우 특별한 성공 메시지
            if uploaded_file.name.lower().endswith('.hwp'):
                st.success(f"✅ {uploaded_file.name} 한글 문서 처리 완료! 텍스트와 표 내용이 추출되었습니다.")
            else:
                st.success(f"✅ {uploaded_file.name} 처리 완료!")
            
        except Exception as e:
            # 한글 문서 처리 실패 시 특별한 안내
            if uploaded_file.name.lower().endswith('.hwp'):
                st.error(f"❌ {uploaded_file.name} 한글 문서 처리 실패: {str(e)}")
                st.warning("💡 한글 문서가 손상되었거나 지원되지 않는 형식일 수 있습니다. 다른 방법으로 텍스트를 추출해보세요.")
            else:
                st.error(f"❌ {uploaded_file.name} 처리 실패: {str(e)}")
    
    # 문서 저장
    save_documents()
    
    # 검색 엔진 및 AI 어시스턴트 초기화
    initialize_ai_components()

def save_documents():
    """문서 저장"""
    if st.session_state.documents:
        docs_dir = get_documents_directory()
        documents_file = os.path.join(docs_dir, "documents_content.pkl")
        if save_documents_content_to_file(st.session_state.documents, documents_file):
            print(f"문서 {len(st.session_state.documents)}개 저장 완료")

def simple_search(query: str, documents: list) -> list:
    """간단한 키워드 검색"""
    query_lower = query.lower()
    results = []
    
    for doc in documents:
        if doc.get('content'):
            content_lower = doc['content'].lower()
            
            # 키워드가 포함된 문장들 찾기
            sentences = doc['content'].split('.')
            relevant_sentences = []
            
            for sentence in sentences:
                if query_lower in sentence.lower():
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                # 관련도 계산 (간단한 키워드 빈도 기반)
                content_count = content_lower.count(query_lower)
                relevance_score = min(content_count / 10.0, 1.0)  # 최대 1.0으로 제한
                
                results.append({
                    'title': doc['name'],
                    'source': doc['name'],
                    'content': '. '.join(relevant_sentences[:3]),  # 최대 3개 문장
                    'score': relevance_score
                })
    
    # 관련도 순으로 정렬
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:10]  # 최대 10개 결과

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
    # 문서가 없으면 안내 메시지
    if not st.session_state.documents:
        st.info("📄 문서를 업로드하면 검색 기능을 사용할 수 있습니다.")
        return
    
    # 검색 엔진이 없으면 간단한 검색 기능 제공
    if not st.session_state.search_engine:
        st.warning("⚠️ 검색 엔진이 초기화되지 않았습니다. 간단한 검색을 시도합니다.")
        
        search_query = st.text_input("검색어를 입력하세요:", placeholder="예: 인공지능, 데이터 분석...")
        
        if st.button("🔍 검색") and search_query:
            with st.spinner("검색 중..."):
                try:
                    # 간단한 키워드 검색
                    results = simple_search(search_query, st.session_state.documents)
                    display_search_results(results)
                except Exception as e:
                    st.error(f"검색 실패: {str(e)}")
    else:
        # 정상적인 검색 엔진 사용
        search_query = st.text_input("검색어를 입력하세요:", placeholder="예: 인공지능, 데이터 분석...")
        
        if st.button("🔍 검색") and search_query:
            with st.spinner("검색 중..."):
                try:
                    results = st.session_state.search_engine.search(search_query)
                    display_search_results(results)
                except Exception as e:
                    st.error(f"검색 실패: {str(e)}")
                    # 검색 엔진 실패 시 간단한 검색으로 대체
                    st.info("간단한 검색을 시도합니다...")
                    results = simple_search(search_query, st.session_state.documents)
                    display_search_results(results)

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
    # 문서가 없으면 안내 메시지
    if not st.session_state.documents:
        st.info("📄 문서를 업로드하면 AI 어시스턴트와 채팅할 수 있습니다.")
        return
    
    # AI 어시스턴트가 없으면 간단한 응답 기능 제공
    if not st.session_state.ai_assistant:
        st.warning("⚠️ AI 어시스턴트가 초기화되지 않았습니다. 간단한 응답을 제공합니다.")
        
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
                    process_simple_chat_message(user_input)
        with col2:
            if st.button("🗑️ 채팅 초기화"):
                st.session_state.chat_history = []
                st.rerun()
    else:
        # 정상적인 AI 어시스턴트 사용
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

def process_simple_chat_message(user_input):
    """간단한 채팅 메시지 처리 (AI 어시스턴트 없이)"""
    # 사용자 메시지 추가
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    try:
        with st.spinner("답변을 생성 중..."):
            # 간단한 키워드 기반 응답 생성
            response = generate_simple_response(user_input, st.session_state.documents)
            
            # AI 응답 추가
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
            
    except Exception as e:
        st.error(f"답변 생성 실패: {str(e)}")

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

def generate_simple_response(question: str, documents: list) -> str:
    """간단한 응답 생성 (AI 어시스턴트 없이)"""
    question_lower = question.lower()
    
    # 문서에서 관련 내용 찾기
    relevant_content = []
    for doc in documents:
        if doc.get('content'):
            content_lower = doc['content'].lower()
            if any(keyword in content_lower for keyword in question_lower.split()):
                # 관련 문장들 추출
                sentences = doc['content'].split('.')
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in question_lower.split()):
                        relevant_content.append(f"📄 {doc['name']}: {sentence.strip()}")
                        if len(relevant_content) >= 3:  # 최대 3개
                            break
    
    if relevant_content:
        response = f"업로드된 문서에서 관련 내용을 찾았습니다:\n\n" + "\n\n".join(relevant_content)
        response += f"\n\n💡 더 정확한 답변을 위해서는 AI 어시스턴트를 초기화해주세요."
    else:
        response = f"죄송합니다. '{question}'에 대한 관련 내용을 업로드된 문서에서 찾을 수 없습니다.\n\n"
        response += f"업로드된 문서 목록:\n"
        for doc in documents:
            response += f"📄 {doc['name']}\n"
        response += f"\n💡 더 정확한 답변을 위해서는 AI 어시스턴트를 초기화해주세요."
    
    return response

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
