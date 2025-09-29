# SmartDoc AI - 지능형 문서 분석 어시스턴트

## 🎯 서비스 개요
SmartDoc AI는 업로드한 문서를 AI로 분석하고, RAG(Retrieval-Augmented Generation) 기술을 활용하여 지능형 질문-답변 서비스를 제공하는 웹 애플리케이션입니다.

## ✨ 주요 기능
- 📄 **문서 업로드**: PDF, Word, 텍스트 파일 지원
- 🔍 **지능형 검색**: Azure AI Search 기반 벡터 검색
- 💬 **Q&A 챗봇**: 문서 내용 기반 질문-답변
- 📊 **자동 요약**: 문서 내용 요약 및 인사이트 제공
- 🎯 **주제 분류**: AI 기반 문서 카테고리 자동 분류

## 🛠️ 기술 스택
- **Frontend**: Streamlit
- **AI/ML**: Azure OpenAI (GPT-4o-mini), LangChain
- **Search**: Azure AI Search
- **Storage**: Azure Blob Storage
- **Document Processing**: PyPDF2, python-docx

## 🚀 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
# .env.sample을 .env로 복사 후 값 입력
cp .env.sample .env
```

### 3. 애플리케이션 실행
```bash
streamlit run src/app.py
```

## 📁 프로젝트 구조
```
SmartDocAI/
├── src/                    # 소스 코드
│   ├── app.py             # 메인 Streamlit 앱
│   ├── document_processor.py  # 문서 처리 모듈
│   ├── search_engine.py   # 검색 엔진
│   ├── ai_assistant.py    # AI 어시스턴트
│   └── utils.py           # 유틸리티 함수
├── static/                # 정적 파일 (CSS, JS)
├── templates/             # HTML 템플릿
├── docs/                  # 문서화
├── uploads/               # 업로드된 파일 임시 저장
├── requirements.txt       # Python 의존성
├── .env.sample           # 환경 변수 샘플
└── README.md             # 프로젝트 설명
```

## 🔧 설정 가이드
1. Azure OpenAI 리소스 생성
2. Azure AI Search 서비스 생성
3. 환경 변수에 API 키 및 엔드포인트 설정
4. 필요한 Azure 리소스 권한 설정

## 📝 사용법
1. 웹 브라우저에서 애플리케이션 접속
2. 문서 파일 업로드
3. 문서 분석 완료 후 질문 입력
4. AI가 문서 내용을 바탕으로 답변 제공

## 🤝 기여
이 프로젝트는 MS AI 개발역량 강화 과정의 학습 결과물입니다.
