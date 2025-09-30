# SmartDocAI Azure 배포 가이드

## 사전 준비사항

### 1. Azure 리소스 생성
Azure Portal에서 다음 리소스들을 생성해야 합니다:

1. **Resource Group**: `smartdoc-rg`
2. **App Service Plan**: `smartdoc-plan` (Linux, B1 SKU 이상)
3. **Web App**: `smartdocai-app` (Python 3.11 런타임)

### 2. GitHub Secrets 설정
Repository Settings → Secrets and variables → Actions에서 다음 secrets를 설정:

- `AZURE_WEBAPP_PUBLISH_PROFILE`: Azure Web App의 Publish Profile (이미 설정됨)
- `AZURE_CREDENTIALS`: Azure Service Principal 인증 정보 (선택사항)

### 3. 환경 변수 설정
Azure Portal → App Service → Configuration → Application Settings에서 다음 환경 변수들을 설정:

#### 필수 환경 변수
```
OPENAI_API_KEY=your_openai_api_key
AZURE_FORM_RECOGNIZER_ENDPOINT=your_form_recognizer_endpoint
AZURE_FORM_RECOGNIZER_KEY=your_form_recognizer_key
AZURE_SEARCH_SERVICE_NAME=your_search_service_name
AZURE_SEARCH_API_KEY=your_search_api_key
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
```

#### 시스템 환경 변수 (자동 설정됨)
```
SCM_DO_BUILD_DURING_DEPLOYMENT=true
ENABLE_ORYX_BUILD=true
PYTHONPATH=/home/site/wwwroot
STREAMLIT_SERVER_PORT=8000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 배포 방법

### 자동 배포 (권장)
1. 코드를 main 브랜치에 push
2. GitHub Actions가 자동으로 배포 실행
3. Actions 탭에서 배포 상태 확인

### 수동 배포
1. Azure Portal에서 Web App 생성
2. Publish Profile 다운로드
3. GitHub Secrets에 `AZURE_WEBAPP_PUBLISH_PROFILE` 설정
4. 코드 push

## 배포 후 확인사항

### 1. 애플리케이션 접속
- URL: `https://smartdocai-app.azurewebsites.net`
- Streamlit 인터페이스가 정상적으로 로드되는지 확인

### 2. 로그 확인
```bash
az webapp log tail --name smartdocai-app --resource-group smartdoc-rg
```

### 3. 기능 테스트
- 문서 업로드 기능
- AI 어시스턴트 기능
- 검색 기능

## 트러블슈팅

### 일반적인 문제들

1. **502 Bad Gateway 오류**
   - 시작 명령이 올바르게 설정되었는지 확인
   - Python 런타임 버전 확인 (3.11)
   - 포트 설정 확인 (8000번 포트)

2. **애플리케이션이 시작되지 않는 경우**
   - 로그 확인: `az webapp log tail --name smartdocai-app --resource-group smartdoc-rg`
   - 환경 변수가 올바르게 설정되었는지 확인
   - requirements.txt의 종속성 문제 확인

3. **메모리 부족 오류**
   - App Service Plan을 상위 SKU로 업그레이드 (B2 이상 권장)

4. **종속성 설치 실패**
   - requirements.txt 파일이 올바른 위치에 있는지 확인
   - `SCM_DO_BUILD_DURING_DEPLOYMENT=true` 설정 확인

## 성능 최적화

1. **App Service Plan 업그레이드**
   ```bash
   az appservice plan update --name smartdoc-plan --resource-group smartdoc-rg --sku S1
   ```

2. **Always On 설정 활성화**
   ```bash
   az webapp config set --name smartdocai-app --resource-group smartdoc-rg --always-on true
   ```

## 보안 고려사항

1. **API 키 보안**
   - Key Vault를 사용하여 민감한 정보 저장
   - 환경 변수로 API 키 관리

2. **HTTPS 강제 설정**
   ```bash
   az webapp update --name smartdocai-app --resource-group smartdoc-rg --https-only true
   ```

## 비용 최적화

1. **개발/테스트 환경**: B1 SKU 사용
2. **프로덕션 환경**: S1 이상 SKU 사용
3. **자동 스케일링 설정**으로 트래픽에 따른 비용 최적화
