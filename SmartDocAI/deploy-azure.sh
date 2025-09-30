#!/bin/bash

# Azure Web App Deployment Script for SmartDocAI
# Make sure you have Azure CLI installed and are logged in

# Configuration
RESOURCE_GROUP="css-rg-092601"
APP_SERVICE_PLAN="smartdoc-plan"
WEB_APP_NAME="smartdocai"  # Existing web app name
LOCATION="Korea Central"  # Korea Central region
PYTHON_VERSION="3.11"

echo "🚀 Starting Azure Web App deployment for SmartDocAI..."

# Create resource group
echo "📦 Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Create App Service Plan
echo "🏗️  Creating App Service Plan: $APP_SERVICE_PLAN"
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Create Web App
echo "🌐 Creating Web App: $WEB_APP_NAME"
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --runtime "PYTHON|$PYTHON_VERSION" \
    --deployment-local-git

# Configure Web App settings
echo "⚙️  Configuring Web App settings..."
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

# Set startup command
echo "🚀 Setting startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "startup.py"

# Deploy code
echo "📤 Deploying application code..."
az webapp deployment source config-local-git \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP

# Get deployment URL
DEPLOY_URL=$(az webapp deployment list-publishing-credentials \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query scmUri -o tsv)

echo ""
echo "✅ Deployment setup complete!"
echo "🌍 Web App URL: https://$WEB_APP_NAME.azurewebsites.net"
echo "📤 Git deployment URL: $DEPLOY_URL"
echo ""
echo "📋 Next steps:"
echo "1. Add your Azure services configuration to App Settings:"
echo "   - OPENAI_API_KEY"
echo "   - AZURE_FORM_RECOGNIZER_ENDPOINT"
echo "   - AZURE_FORM_RECOGNIZER_KEY"
echo "   - AZURE_SEARCH_SERVICE_NAME"
echo "   - AZURE_SEARCH_API_KEY"
echo "   - AZURE_STORAGE_CONNECTION_STRING"
echo ""
echo "2. Deploy your code:"
echo "   git remote add azure $DEPLOY_URL"
echo "   git push azure main"
echo ""
echo "3. Monitor deployment logs:"
echo "   az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
