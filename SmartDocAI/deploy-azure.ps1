# Azure Web App Deployment Script for SmartDocAI (PowerShell)
# Make sure you have Azure CLI installed and are logged in

# Configuration
$RESOURCE_GROUP = "css-rg-092601"
$APP_SERVICE_PLAN = "smartdoc-plan"
$WEB_APP_NAME = "smartdocai"  # Existing web app name
$LOCATION = "Korea Central"  # Korea Central region
$PYTHON_VERSION = "3.11"

Write-Host "🚀 Starting Azure Web App deployment for SmartDocAI..." -ForegroundColor Green

# Create resource group
Write-Host "📦 Creating resource group: $RESOURCE_GROUP" -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan
Write-Host "🏗️  Creating App Service Plan: $APP_SERVICE_PLAN" -ForegroundColor Yellow
az appservice plan create `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux

# Create Web App
Write-Host "🌐 Creating Web App: $WEB_APP_NAME" -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $APP_SERVICE_PLAN `
    --name $WEB_APP_NAME `
    --runtime "PYTHON|$PYTHON_VERSION" `
    --deployment-local-git

# Configure Web App settings
Write-Host "⚙️  Configuring Web App settings..." -ForegroundColor Yellow
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

# Set startup command
Write-Host "🚀 Setting startup command..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $WEB_APP_NAME `
    --startup-file "startup.py"

# Deploy code
Write-Host "📤 Deploying application code..." -ForegroundColor Yellow
az webapp deployment source config-local-git `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP

# Get deployment URL
$DEPLOY_URL = az webapp deployment list-publishing-credentials `
    --name $WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query scmUri -o tsv

Write-Host ""
Write-Host "✅ Deployment setup complete!" -ForegroundColor Green
Write-Host "🌍 Web App URL: https://$WEB_APP_NAME.koreacentral-01.azurewebsites.net" -ForegroundColor Cyan
Write-Host "📤 Git deployment URL: $DEPLOY_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Add your Azure services configuration to App Settings:"
Write-Host "   - OPENAI_API_KEY"
Write-Host "   - AZURE_FORM_RECOGNIZER_ENDPOINT" 
Write-Host "   - AZURE_FORM_RECOGNIZER_KEY"
Write-Host "   - AZURE_SEARCH_SERVICE_NAME"
Write-Host "   - AZURE_SEARCH_API_KEY"
Write-Host "   - AZURE_STORAGE_CONNECTION_STRING"
Write-Host ""
Write-Host "2. Deploy your code:"
Write-Host "   git remote add azure $DEPLOY_URL"
Write-Host "   git push azure main"
Write-Host ""
Write-Host "3. Monitor deployment logs:"
Write-Host "   az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
