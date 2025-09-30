# SmartDoc AI - 지능형 문서 분석 어시스턴트

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io)
[![Azure](https://img.shields.io/badge/Azure-OpenAI%20%7C%20Search%20%7C%20Storage-0078d4.svg)](https://azure.microsoft.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)](https://langchain.com)

## 🎯 서비스 개요
SmartDoc AI는 업로드한 문서를 AI로 분석하고, RAG(Retrieval-Augmented Generation) 기술을 활용하여 지능형 질문-답변 서비스를 제공하는 웹 애플리케이션입니다. Azure의 강력한 AI 서비스들을 활용하여 정확하고 빠른 문서 분석을 제공합니다.

## 🌐 라이브 데모
**배포된 웹 애플리케이션**: [https://smartdocai-hvbwfketcse7g9ff.koreacentral-01.azurewebsites.net/](https://smartdocai-hvbwfketcse7g9ff.koreacentral-01.azurewebsites.net/)

위 링크를 통해 실제 배포된 SmartDoc AI 서비스를 바로 체험해보실 수 있습니다. 문서를 업로드하고 AI 어시스턴트와 대화해보세요!

## ✨ 주요 기능
- 📄 **다양한 문서 지원**: PDF, Word, PowerPoint, 텍스트, Excel 파일 지원
- 🔍 **지능형 검색**: Azure AI Search 기반 벡터 검색으로 정확한 문서 검색
- 💬 **AI 챗봇**: GPT-4o-mini 기반 문서 내용 질문-답변
- 📊 **자동 요약**: 문서 내용 요약 및 핵심 인사이트 제공
- 🎯 **문서 분류**: AI 기반 문서 카테고리 자동 분류
- 🔐 **보안**: Azure Key Vault 통합 및 환경 변수 관리
- 🚀 **원클릭 배포**: Azure Web App 자동 배포 스크립트
- 📱 **반응형 UI**: Streamlit 기반 모던 웹 인터페이스

## 🛠️ 기술 스택
- **Frontend**: Streamlit (Latest)
- **AI/ML**: Azure OpenAI (GPT-4o-mini), LangChain 0.1.0+
- **Search**: Azure AI Search, Azure Form Recognizer
- **Storage**: Azure Blob Storage
- **Document Processing**: PyPDF2, python-docx, python-pptx, openpyxl, pandas
- **Vector Search**: FAISS-CPU, Azure AI Search
- **Deployment**: Azure Web App, Azure CLI
- **Environment**: python-dotenv, tiktoken

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/css-MVP.git
cd css-MVP/SmartDocAI
```

### 2. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. Azure 서비스 설정
Azure Portal에서 다음 서비스들을 생성하고 설정:

1. **Azure OpenAI 리소스**
   - GPT-4.1-mini 모델 배포
   - API 키 및 엔드포인트 확인

2. **Azure AI Search 서비스**
   - 검색 서비스 생성
   - API 키 및 엔드포인트 확인

3. **Azure Storage Account**
   - Blob Storage 생성
   - 연결 문자열 확인

### 4. 환경 변수 설정
```bash
# 환경 설정 스크립트 실행 (권장)
python setup_env_vars.py

# 또는 수동으로 .env 파일 생성
cp azure-config.sample .env
```

`.env` 파일에 Azure 서비스 정보 입력:
```env
# Azure OpenAI 설정
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini

# Azure AI Search 설정
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your_search_key_here

# Azure Storage 설정
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here

# Azure Form Recognizer 설정 (선택사항)
AZURE_FORM_RECOGNIZER_ENDPOINT=https://your-form-recognizer.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=your_form_recognizer_key_here
```

### 5. 애플리케이션 실행
```bash
# 간편 실행 (권장)
python run.py

# 또는 직접 실행
streamlit run src/app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용하세요!

## 📁 프로젝트 구조
```
SmartDocAI/
├── src/                           # 소스 코드
│   ├── app.py                    # 메인 Streamlit 애플리케이션
│   ├── document_processor.py     # 문서 처리 및 파싱 모듈
│   ├── search_engine.py          # Azure AI Search 엔진
│   ├── ai_assistant.py           # AI 어시스턴트 및 챗봇
│   └── utils.py                  # 유틸리티 함수
├── static/                       # 정적 파일
│   └── style.css                 # 커스텀 스타일시트
├── docs/                         # 문서화
│   ├── quick_start.md            # 빠른 시작 가이드
│   ├── github-secrets-setup.md   # GitHub Secrets 설정
│   └── sample_document.txt       # 샘플 문서
├── azure-app-service-settings.json  # Azure App Service 설정
├── azure-config.sample           # Azure 환경 변수 샘플
├── deploy-azure.ps1              # Azure 배포 스크립트 (Windows)
├── deploy-azure.sh               # Azure 배포 스크립트 (Linux/macOS)
├── deploy-to-existing-app.ps1    # 기존 앱 배포 (Windows)
├── deploy-to-existing-app.sh     # 기존 앱 배포 (Linux/macOS)
├── startup.py                    # Azure Web App 시작 스크립트
├── startup.sh                    # Linux 시작 스크립트
├── startup2.sh                   # 대체 시작 스크립트
├── web.config                    # IIS 설정 파일
├── run.py                        # 로컬 실행 스크립트
├── setup_env.py                  # 환경 설정 스크립트
├── setup_env_vars.py             # 환경 변수 설정 스크립트
├── setup_environment.md          # 환경 설정 가이드
├── requirements.txt              # Python 의존성
├── smartdoc.zip                  # 압축된 프로젝트 파일
├── AZURE_DEPLOYMENT.md           # Azure 배포 가이드
└── README.md                     # 프로젝트 설명
```

## 🚀 Azure 배포

### 자동 배포 (권장)
```bash
# Windows PowerShell
.\deploy-azure.ps1

# Linux/macOS
chmod +x deploy-azure.sh
./deploy-azure.sh
```

### 수동 배포
자세한 배포 가이드는 [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)를 참조하세요.

### 기존 앱에 배포
```bash
# Windows
.\deploy-to-existing-app.ps1

# Linux/macOS
chmod +x deploy-to-existing-app.sh
./deploy-to-existing-app.sh
```

### 배포 전 체크리스트
- [ ] Azure CLI 설치 및 로그인 완료
- [ ] 필요한 Azure 서비스 생성 완료 (OpenAI, Search, Storage)
- [ ] 환경 변수 설정 완료
- [ ] 로컬에서 애플리케이션 정상 실행 확인
- [ ] Azure 구독에 충분한 할당량 확인

## 📝 사용법

### 1. 문서 업로드
- 사이드바의 "문서" 탭에서 파일 업로드
- 지원 형식: PDF, Word, PowerPoint, Excel, 텍스트 파일
- 업로드된 문서는 자동으로 분석 및 인덱싱

### 2. AI 챗봇과 대화
- "채팅" 탭에서 AI 어시스턴트와 대화
- 업로드한 문서 내용에 대해 질문
- GPT-4.1-mini가 문서를 바탕으로 정확한 답변 제공

### 3. 문서 검색
- "문서 검색" 섹션에서 키워드 검색
- Azure AI Search 기반 벡터 검색
- 관련 문서 내용과 유사도 점수 확인

### 4. 문서 요약 및 분석
- 자동 문서 요약 기능
- 핵심 키워드 추출
- 문서 카테고리 자동 분류

## 🔧 설정 가이드

### Azure 서비스 설정
1. **Azure OpenAI 리소스 생성**
   - Azure Portal에서 OpenAI 리소스 생성
   - GPT-4.1-mini 모델 배포
   - API 키 및 엔드포인트 확인

2. **Azure AI Search 서비스 생성**
   - 검색 서비스 생성 및 인덱스 설정
   - API 키 및 엔드포인트 확인

3. **Azure Storage Account 생성**
   - Blob Storage 컨테이너 생성
   - 연결 문자열 확인

### 환경 변수 설정
자세한 설정 방법은 [docs/quick_start.md](docs/quick_start.md)를 참조하세요.

## 🛠️ 문제 해결

### 일반적인 문제
1. **Azure 서비스 연결 오류**
   - API 키와 엔드포인트 확인
   - 리소스 지역 및 모델 배포 상태 확인
   - 네트워크 방화벽 설정 확인
   - 환경 변수가 올바르게 설정되었는지 확인

2. **문서 업로드 실패**
   - 파일 형식 확인 (지원 형식: PDF, DOCX, PPTX, XLSX, TXT)
   - 파일 크기 확인 (기본 10MB 제한)
   - 파일 손상 여부 확인
   - Azure Storage 연결 상태 확인

3. **검색 결과 없음**
   - 문서가 제대로 업로드되었는지 확인
   - 검색어를 다양하게 시도
   - Azure AI Search 인덱스 상태 확인
   - 벡터 임베딩 생성 상태 확인

4. **AI 응답 오류**
   - Azure OpenAI 서비스 상태 확인
   - API 할당량 및 제한 확인
   - 모델 배포 상태 확인
   - LangChain 설정 확인

5. **환경 설정 오류**
   - `python setup_env_vars.py` 실행으로 환경 변수 재설정
   - `.env` 파일이 프로젝트 루트에 있는지 확인
   - 가상환경이 올바르게 활성화되었는지 확인

6. **의존성 설치 오류**
   - Python 버전 확인 (3.11+ 권장)
   - pip 업그레이드: `pip install --upgrade pip`
   - 캐시 클리어: `pip cache purge`
   - 의존성 재설치: `pip install -r requirements.txt --force-reinstall`

### 로그 확인
```bash
# 로컬 실행 시
python run.py

# Azure 배포 시
az webapp log tail --name your-app-name --resource-group smartdoc-rg

# 상세 로그 확인
az webapp log download --name your-app-name --resource-group smartdoc-rg
```

### 성능 최적화
- 대용량 문서 처리 시 청크 크기 조정
- FAISS 인덱스 메모리 사용량 모니터링
- Azure AI Search 쿼리 최적화
- 캐싱 전략 적용

## 💻 시스템 요구사항

### 최소 요구사항
- **Python**: 3.11 이상
- **메모리**: 4GB RAM (8GB 권장)
- **디스크**: 2GB 여유 공간
- **네트워크**: 인터넷 연결 (Azure 서비스 접근용)

### 권장 사양
- **Python**: 3.11+
- **메모리**: 8GB RAM 이상
- **디스크**: 5GB 여유 공간
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+

### Azure 서비스 요구사항
- Azure OpenAI Service (GPT-4.1-mini)
- Azure AI Search (Standard S1 이상 권장)
- Azure Storage Account (Standard 계층)
- Azure Form Recognizer (선택사항)

## 📚 추가 문서
- [빠른 시작 가이드](docs/quick_start.md)
- [Azure 배포 가이드](AZURE_DEPLOYMENT.md)
- [GitHub Secrets 설정](docs/github-secrets-setup.md)
- [환경 설정 가이드](setup_environment.md)
