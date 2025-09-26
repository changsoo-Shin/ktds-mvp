# 🧳 AI 여행 플래너

Azure OpenAI와 LangChain을 활용한 AI 기반 여행일정 추천 서비스입니다.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)](https://streamlit.io)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-green.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

## 🎯 프로젝트 개요

이 프로젝트는 MS AI 개발과정 교육을 통해 학습한 기술들을 활용하여 개발된 MVP 서비스입니다. 사용자가 원하는 여행지와 조건을 입력하면 AI가 맞춤형 여행일정을 생성해주는 서비스입니다.

## ✨ 주요 기능

### 🗺️ 여행일정 생성
- 여행지, 기간, 스타일, 예산을 입력하면 AI가 맞춤 일정 생성
- RAG 기술로 정확한 여행 정보 제공
- 일정 다운로드 기능
- 사용자 지정 여행 시작일 지원

### 📸 이미지 분석
- 여행하고 싶은 장소의 사진 업로드
- Azure Computer Vision으로 이미지 분석
- 유사한 여행지 추천

### 💬 AI 여행 상담
- 실시간 채팅으로 여행 관련 질문 답변
- Azure OpenAI GPT-4 기반 자연어 처리

### 🌤️ 날씨 정보
- 여행지 현재 날씨 확인
- 여행 준비 조언 제공

## 🚀 설치 및 실행

### 1. 로컬 실행
```bash
# 프로젝트 클론
git clone https://github.com/changsoo-Shin/ktds-css.git
cd ktds-css

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. GitHub 저장소 연결
3. 환경 변수 설정:
   - `AZURE_ENDPOINT`: Azure OpenAI 엔드포인트
   - `OPENAI_API_KEY`: Azure OpenAI API 키
   - `OPENAI_API_VERSION`: 2024-02-15-preview
4. 배포 실행

### 3. 환경 변수 설정
`.env` 파일을 생성하고 다음 정보를 입력:

```env
# Azure OpenAI 설정 (필수)
AZURE_ENDPOINT=https://your-resource-name.openai.azure.com/
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search 설정 (선택사항 - RAG 기능용)
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your_azure_search_key_here
AZURE_SEARCH_INDEX_NAME=travel_destinations

# Azure Computer Vision 설정 (선택사항 - 이미지 분석용)
COMPUTER_VISION_KEY=your_computer_vision_key_here
COMPUTER_VISION_ENDPOINT=https://your-computer-vision-resource.cognitiveservices.azure.com/

# OpenWeatherMap API (선택사항 - 날씨 정보용)
WEATHER_API_KEY=your_openweathermap_api_key_here
```

### 4. 실행
```bash
streamlit run app.py
```

## 📁 프로젝트 구조

```
ktds-css/
├── app.py                 # 메인 Streamlit 앱
├── config.py             # 설정 관리
├── travel_rag.py         # RAG 시스템
├── image_analyzer.py     # 이미지 분석
├── weather_service.py    # 날씨 서비스
├── requirements.txt      # 의존성
├── .env.sample          # 환경변수 샘플
├── .gitignore           # Git 무시 파일
├── .github/workflows/   # GitHub Actions
└── README.md            # 프로젝트 설명
```

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI**: Azure OpenAI (GPT-4)
- **RAG**: LangChain + Azure AI Search
- **Computer Vision**: Azure Computer Vision
- **Weather**: OpenWeatherMap API

## 📝 사용법

1. **여행일정 생성**
   - 사이드바에서 여행지, 시작일, 기간, 스타일, 예산 설정
   - "여행일정 생성하기" 버튼 클릭
   - 생성된 일정 확인 및 다운로드

2. **이미지 분석**
   - "이미지 분석" 탭에서 사진 업로드
   - "이미지 분석하기" 버튼 클릭
   - AI가 분석한 결과와 추천 여행지 확인

3. **AI 상담**
   - "AI 상담" 탭에서 채팅 시작
   - 여행 관련 질문 자유롭게 질문

## ⚠️ 주의사항

- Azure OpenAI 서비스가 필요합니다
- 일부 기능은 선택적 API 키가 필요합니다
- 인터넷 연결이 필요합니다

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🎓 교육 과정

이 프로젝트는 다음 교육 과정을 통해 개발되었습니다:
- MS AI 개발과정 (KTDS)
- Azure OpenAI 서비스 활용
- LangChain 프레임워크 학습
- RAG (Retrieval Augmented Generation) 구현
