# Azure OpenAI 환경 설정 가이드

## 문제 해결
현재 "AI 어시스턴트 초기화 실패: Azure OpenAI 설정이 필요합니다" 오류가 발생하고 있습니다.

## 해결 방법

### 1. Azure OpenAI 서비스 생성
1. [Azure Portal](https://portal.azure.com)에 로그인
2. "Azure OpenAI" 검색하여 서비스 생성
3. 리소스 그룹, 지역, 가격 책정 계층 선택
4. 배포 모델 생성 (예: GPT-4o-mini)

### 2. 환경 변수 설정

#### 방법 A: .env 파일 생성 (권장)
1. `SmartDocAI` 폴더에 `.env` 파일 생성
2. `.env.example` 파일을 복사하여 내용 수정:

```bash
# .env 파일 내용
AZURE_OPENAI_API_KEY=실제_API_키_여기에_입력
AZURE_OPENAI_ENDPOINT=https://실제-리소스-이름.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
```

#### 방법 B: 시스템 환경 변수 설정
PowerShell에서 다음 명령어 실행:

```powershell
$env:AZURE_OPENAI_API_KEY="실제_API_키_여기에_입력"
$env:AZURE_OPENAI_ENDPOINT="https://실제-리소스-이름.openai.azure.com/"
$env:AZURE_OPENAI_API_VERSION="2024-02-15-preview"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4.1-mini"
```

### 3. 필요한 정보 확인
Azure Portal에서 다음 정보를 확인하세요:
- **API 키**: Keys and Endpoint 섹션에서 확인
- **엔드포인트**: Keys and Endpoint 섹션에서 확인
- **배포 이름**: Deployments 섹션에서 확인

### 4. 애플리케이션 실행
환경 변수 설정 후 다음 명령어로 실행:

```bash
cd SmartDocAI
streamlit run src/app.py
```

## 추가 설정 (선택사항)
- Azure AI Search: 고급 검색 기능을 위해 설정
- Azure Form Recognizer: 문서 처리 향상을 위해 설정
- Azure Storage: 파일 저장을 위해 설정

이 설정들은 선택사항이며, 기본 AI 기능은 Azure OpenAI만으로도 작동합니다.
