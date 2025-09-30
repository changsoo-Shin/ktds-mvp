#!/bin/bash

# Azure Web App 배포 스크립트 - 기존 웹앱에 배포
# 기존 웹앱: smartdocai-hvbwfketcse7g9ff.koreacentral-01.azurewebsites.net

# Configuration
RESOURCE_GROUP="css-rg-092601"  # 기존 리소스 그룹명
WEB_APP_NAME="smartdocai"  # 기존 웹앱명
LOCATION="Korea Central"  # 기존 위치

echo "🚀 기존 Azure Web App에 SmartDocAI 배포 중..."
echo "웹앱: $WEB_APP_NAME"

# Azure CLI 로그인 확인
echo "🔐 Azure CLI 로그인 상태 확인..."
LOGIN_STATUS=$(az account show --query "user.name" -o tsv 2>/dev/null)
if [ -z "$LOGIN_STATUS" ]; then
    echo "❌ Azure CLI에 로그인되지 않았습니다. 먼저 'az login'을 실행하세요."
    exit 1
fi
echo "✅ 로그인됨: $LOGIN_STATUS"

# 웹앱 존재 확인
echo "🔍 웹앱 존재 확인..."
WEB_APP_EXISTS=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query "name" -o tsv 2>/dev/null)
if [ -z "$WEB_APP_EXISTS" ]; then
    echo "❌ 웹앱을 찾을 수 없습니다. 리소스 그룹명과 웹앱명을 확인하세요."
    echo "리소스 그룹: $RESOURCE_GROUP"
    echo "웹앱명: $WEB_APP_NAME"
    exit 1
fi
echo "✅ 웹앱 확인됨: $WEB_APP_EXISTS"

# 웹앱 설정 업데이트
echo "⚙️ 웹앱 설정 업데이트..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        ENABLE_ORYX_BUILD=true \
        PYTHONPATH=/home/site/wwwroot \
        STREAMLIT_SERVER_PORT=8000 \
        STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
        STREAMLIT_SERVER_HEADLESS=true \
        STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 시작 명령 설정
echo "🚀 시작 명령 설정..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "startup.py"

# Git 배포 설정
echo "📤 Git 배포 설정..."
az webapp deployment source config-local-git \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP

# 배포 URL 가져오기
DEPLOY_URL=$(az webapp deployment list-publishing-credentials \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query scmUri -o tsv)

echo ""
echo "✅ 배포 설정 완료!"
echo "🌍 웹앱 URL: https://$WEB_APP_NAME.koreacentral-01.azurewebsites.net"
echo "📤 Git 배포 URL: $DEPLOY_URL"
echo ""
echo "📋 다음 단계:"
echo "1. 코드 배포:"
echo "   git remote add azure $DEPLOY_URL"
echo "   git push azure main"
echo ""
echo "2. 환경 변수 설정 (Azure Portal에서):"
echo "   - AZURE_OPENAI_API_KEY"
echo "   - AZURE_OPENAI_ENDPOINT"
echo "   - AZURE_FORM_RECOGNIZER_ENDPOINT"
echo "   - AZURE_FORM_RECOGNIZER_KEY"
echo "   - AZURE_SEARCH_SERVICE_NAME"
echo "   - AZURE_SEARCH_API_KEY"
echo "   - AZURE_SEARCH_INDEX_NAME"
echo "   - AZURE_STORAGE_CONNECTION_STRING"
echo ""
echo "3. 배포 로그 모니터링:"
echo "   az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
