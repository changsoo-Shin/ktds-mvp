# Azure Web App 배포 스크립트 - 기존 웹앱에 배포
# 기존 웹앱: smartdocai-hvbwfketcse7g9ff.koreacentral-01.azurewebsites.net

# Configuration
$RESOURCE_GROUP = "css-rg-092601"  # 기존 리소스 그룹명
$WEB_APP_NAME = "smartdocai"  # 기존 웹앱명
$LOCATION = "Korea Central"  # 기존 위치

Write-Host "🚀 기존 Azure Web App에 SmartDocAI 배포 중..." -ForegroundColor Green
Write-Host "웹앱: $WEB_APP_NAME" -ForegroundColor Cyan

# Azure CLI 로그인 확인
Write-Host "🔐 Azure CLI 로그인 상태 확인..." -ForegroundColor Yellow
$loginStatus = az account show --query "user.name" -o tsv 2>$null
if (-not $loginStatus) {
    Write-Host "❌ Azure CLI에 로그인되지 않았습니다. 먼저 'az login'을 실행하세요." -ForegroundColor Red
    exit 1
}
Write-Host "✅ 로그인됨: $loginStatus" -ForegroundColor Green

# 웹앱 존재 확인
Write-Host "🔍 웹앱 존재 확인..." -ForegroundColor Yellow
$webAppExists = az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "name" -o tsv 2>$null
if (-not $webAppExists) {
    Write-Host "❌ 웹앱을 찾을 수 없습니다. 리소스 그룹명과 웹앱명을 확인하세요." -ForegroundColor Red
    Write-Host "리소스 그룹: $RESOURCE_GROUP" -ForegroundColor Yellow
    Write-Host "웹앱명: $WEB_APP_NAME" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ 웹앱 확인됨: $webAppExists" -ForegroundColor Green

# 웹앱 설정 업데이트
Write-Host "⚙️ 웹앱 설정 업데이트..." -ForegroundColor Yellow
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --settings `
        SCM_DO_BUILD_DURING_DEPLOYMENT=true `
        ENABLE_ORYX_BUILD=true `
        PYTHONPATH=/home/site/wwwroot `
        STREAMLIT_SERVER_PORT=8000 `
        STREAMLIT_SERVER_ADDRESS=0.0.0.0 `
        STREAMLIT_SERVER_HEADLESS=true `
        STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 시작 명령 설정
Write-Host "🚀 시작 명령 설정..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --startup-file "startup.py"

# Git 배포 설정
Write-Host "📤 Git 배포 설정..." -ForegroundColor Yellow
az webapp deployment source config-local-git `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP

# 배포 URL 가져오기
$DEPLOY_URL = az webapp deployment list-publishing-credentials `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query scmUri -o tsv

Write-Host ""
Write-Host "✅ 배포 설정 완료!" -ForegroundColor Green
Write-Host "🌍 웹앱 URL: https://$WEB_APP_NAME.koreacentral-01.azurewebsites.net" -ForegroundColor Cyan
Write-Host "📤 Git 배포 URL: $DEPLOY_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 다음 단계:" -ForegroundColor Yellow
Write-Host "1. 코드 배포:" -ForegroundColor White
Write-Host "   git remote add azure $DEPLOY_URL" -ForegroundColor Gray
Write-Host "   git push azure main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 환경 변수 설정 (Azure Portal에서):" -ForegroundColor White
Write-Host "   - AZURE_OPENAI_API_KEY" -ForegroundColor Gray
Write-Host "   - AZURE_OPENAI_ENDPOINT" -ForegroundColor Gray
Write-Host "   - AZURE_FORM_RECOGNIZER_ENDPOINT" -ForegroundColor Gray
Write-Host "   - AZURE_FORM_RECOGNIZER_KEY" -ForegroundColor Gray
Write-Host "   - AZURE_SEARCH_SERVICE_NAME" -ForegroundColor Gray
Write-Host "   - AZURE_SEARCH_API_KEY" -ForegroundColor Gray
Write-Host "   - AZURE_SEARCH_INDEX_NAME" -ForegroundColor Gray
Write-Host "   - AZURE_STORAGE_CONNECTION_STRING" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 배포 로그 모니터링:" -ForegroundColor White
Write-Host "   az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP" -ForegroundColor Gray
