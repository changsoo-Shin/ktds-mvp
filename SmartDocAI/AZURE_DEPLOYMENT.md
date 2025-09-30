# Azure Web App 배포 가이드

SmartDocAI를 Azure Web App에 배포하는 방법을 안내합니다.

## 사전 준비사항

1. **Azure CLI 설치**
   ```bash
   # Windows (PowerShell)
   Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
   
   # macOS
   brew update && brew install azure-cli
   
   # Ubuntu/Debian
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Azure에 로그인**
   ```bash
   az login
   ```

3. **필요한 Azure 서비스 준비**
   - OpenAI API 키
   - Azure Form Recognizer 서비스
   - Azure Cognitive Search 서비스
   - Azure Storage Account

## 자동 배포 방법

### Windows (PowerShell)
```powershell
# 실행 권한 설정
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 배포 스크립트 실행
.\deploy-azure.ps1
```

### Linux/macOS (Bash)
```bash
# 실행 권한 부여
chmod +x deploy-azure.sh

# 배포 스크립트 실행
./deploy-azure.sh
```

## 수동 배포 방법

### 1. 리소스 그룹 생성
```bash
az group create --name css-rg-092601 --location "Korea Central"
```

### 2. App Service Plan 생성
```bash
az appservice plan create \
    --name smartdoc-plan \
    --resource-group css-rg-092601 \
    --sku B1 \
    --is-linux
```

### 3. Web App 생성
```bash
az webapp create \
    --resource-group css-rg-092601 \
    --plan smartdoc-plan \
    --name smartdocai \
    --runtime "PYTHON|3.11" \
    --deployment-local-git
```

### 4. 환경 변수 설정
Azure Portal에서 App Service → Configuration → Application Settings에 다음 환경 변수들을 추가:

#### 필수 환경 변수
- `OPENAI_API_KEY`: OpenAI API 키
- `AZURE_FORM_RECOGNIZER_ENDPOINT`: Form Recognizer 엔드포인트
- `AZURE_FORM_RECOGNIZER_KEY`: Form Recognizer 키
- `AZURE_SEARCH_SERVICE_NAME`: Cognitive Search 서비스 이름
- `AZURE_SEARCH_API_KEY`: Cognitive Search API 키
- `AZURE_STORAGE_CONNECTION_STRING`: Storage Account 연결 문자열

#### 시스템 환경 변수
- `SCM_DO_BUILD_DURING_DEPLOYMENT`: true
- `ENABLE_ORYX_BUILD`: true
- `PYTHONPATH`: /home/site/wwwroot
- `STREAMLIT_SERVER_PORT`: 8000
- `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0
- `STREAMLIT_SERVER_HEADLESS`: true
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: false

### 5. 시작 명령 설정
```bash
az webapp config set \
    --resource-group css-rg-092601 \
    --name smartdocai \
    --startup-file "startup.py"
```

### 6. 코드 배포
```bash
# Git remote 추가
git remote add azure https://smartdocai.scm.azurewebsites.net/smartdocai.git

# 코드 푸시
git push azure main
```

## 배포 후 확인사항

### 1. 로그 확인
```bash
az webapp log tail --name smartdocai --resource-group css-rg-092601
```

### 2. 애플리케이션 상태 확인
- 브라우저에서 `https://smartdocai-hvbwfketcse7g9ff.koreacentral-01.azurewebsites.net` 접속
- Streamlit 인터페이스가 정상적으로 로드되는지 확인

### 3. 기능 테스트
- 문서 업로드 기능 테스트
- AI 어시스턴트 기능 테스트
- 검색 기능 테스트

## 트러블슈팅

### 일반적인 문제들

1. **애플리케이션이 시작되지 않는 경우**
   - 로그 확인: `az webapp log tail --name smartdocai --resource-group css-rg-092601`
   - 환경 변수가 올바르게 설정되었는지 확인
   - requirements.txt의 종속성 문제 확인

2. **502 Bad Gateway 오류**
   - 시작 명령이 올바르게 설정되었는지 확인
   - Python 런타임 버전 확인
   - 포트 설정 확인 (8000번 포트 사용)

3. **메모리 부족 오류**
   - App Service Plan을 상위 SKU로 업그레이드 (B2 이상 권장)

4. **종속성 설치 실패**
   - requirements.txt 파일이 루트 디렉토리에 있는지 확인
   - `SCM_DO_BUILD_DURING_DEPLOYMENT=true` 설정 확인

### 성능 최적화

1. **App Service Plan 업그레이드**
   ```bash
   az appservice plan update --name smartdoc-plan --resource-group css-rg-092601 --sku S1
   ```

2. **Always On 설정 활성화**
   ```bash
   az webapp config set --name smartdocai --resource-group css-rg-092601 --always-on true
   ```

3. **CDN 설정** (정적 파일 가속화)
   - Azure CDN 프로필 생성
   - 정적 자산에 대한 CDN 엔드포인트 설정

## 보안 고려사항

1. **API 키 보안**
   - Key Vault를 사용하여 민감한 정보 저장
   - 환경 변수로 API 키 관리

2. **HTTPS 강제 설정**
   ```bash
   az webapp update --name smartdocai --resource-group css-rg-092601 --https-only true
   ```

3. **방화벽 설정**
   - 필요에 따라 IP 제한 설정
   - VNet 통합 고려

## 모니터링 및 로깅

1. **Application Insights 설정**
   ```bash
   az monitor app-insights component create \
       --app smartdocai-insights \
       --location "Korea Central" \
       --resource-group css-rg-092601
   ```

2. **로그 스트림 모니터링**
   ```bash
   az webapp log config --name smartdocai --resource-group css-rg-092601 \
       --application-logging filesystem --level information
   ```

## 비용 최적화

1. **개발/테스트 환경**: B1 SKU 사용
2. **프로덕션 환경**: S1 이상 SKU 사용
3. **자동 스케일링 설정**으로 트래픽에 따른 비용 최적화

---

배포 과정에서 문제가 발생하면 Azure Portal의 App Service 로그를 확인하거나 Azure 지원팀에 문의하세요.
