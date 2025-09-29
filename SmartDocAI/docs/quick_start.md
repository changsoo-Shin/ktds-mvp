# SmartDoc AI 빠른 시작 가이드

## 🚀 5분 만에 시작하기

### 1단계: 환경 설정
```bash
# 프로젝트 디렉토리로 이동
cd SmartDocAI

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: Azure 서비스 설정
1. **Azure OpenAI 리소스 생성**
   - Azure Portal에서 OpenAI 리소스 생성
   - GPT-4o-mini 모델 배포
   - API 키 및 엔드포인트 확인

2. **Azure AI Search 서비스 생성**
   - Azure Portal에서 AI Search 리소스 생성
   - API 키 및 엔드포인트 확인

### 3단계: 환경 변수 설정
`.env` 파일을 열어서 다음 정보를 입력:

```env
# Azure OpenAI 설정
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# Azure AI Search 설정
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your_search_key_here
```

### 4단계: 애플리케이션 실행
```bash
python run.py
```

브라우저에서 `http://localhost:8501`로 접속하면 SmartDoc AI를 사용할 수 있습니다!

## 📄 사용 방법

### 문서 업로드
1. 사이드바에서 "문서" 탭 선택
2. PDF, Word, 텍스트 파일 업로드
3. 문서 처리 완료 확인

### 질문하기
1. "채팅" 탭에서 AI 어시스턴트와 대화
2. 업로드한 문서 내용에 대해 질문
3. AI가 문서를 바탕으로 답변 제공

### 문서 검색
1. "문서 검색" 섹션에서 키워드 검색
2. 관련 문서 내용 확인
3. 검색 결과에서 상세 정보 확인

## 🎯 주요 기능

- **📄 문서 업로드**: PDF, Word, 텍스트 파일 지원
- **🔍 지능형 검색**: Azure AI Search 기반 벡터 검색
- **💬 Q&A 챗봇**: 문서 내용 기반 질문-답변
- **📊 자동 요약**: 문서 내용 요약 및 분석
- **🎯 문서 분류**: AI 기반 카테고리 자동 분류

## 🛠️ 문제 해결

### 일반적인 문제
1. **Azure 서비스 연결 오류**
   - API 키와 엔드포인트 확인
   - 리소스 지역 및 모델 배포 상태 확인

2. **문서 업로드 실패**
   - 파일 형식 확인 (PDF, DOCX, TXT만 지원)
   - 파일 크기 확인 (기본 10MB 제한)

3. **검색 결과 없음**
   - 문서가 제대로 업로드되었는지 확인
   - 검색어를 다양하게 시도

### 로그 확인
애플리케이션 실행 시 터미널에서 오류 메시지를 확인할 수 있습니다.

## 📞 지원

문제가 지속되면 다음을 확인해주세요:
- Azure 서비스 상태
- 네트워크 연결
- 환경 변수 설정
- 의존성 패키지 버전
