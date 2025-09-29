# GitHub Secrets 설정 가이드

## 1. GitHub 리포지토리에서 시크릿 설정

### 단계별 설정 방법

1. **GitHub 리포지토리로 이동**
   - 브라우저에서 GitHub 리포지토리 페이지로 이동

2. **Settings 탭 클릭**
   - 리포지토리 상단 메뉴에서 "Settings" 탭 클릭

3. **Secrets and variables 섹션으로 이동**
   - 왼쪽 사이드바에서 "Secrets and variables" → "Actions" 클릭

4. **New repository secret 클릭**
   - "New repository secret" 버튼 클릭

## 2. 필요한 시크릿 목록

### 필수 애플리케이션 시크릿

| 시크릿 이름 | 설명 | 예시 값 |
|------------|------|---------|
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-...` |
| `AZURE_FORM_RECOGNIZER_ENDPOINT` | Azure Form Recognizer 엔드포인트 | `https://your-form-recognizer.cognitiveservices.azure.com/` |
| `AZURE_FORM_RECOGNIZER_KEY` | Azure Form Recognizer 키 | `your_form_recognizer_key_here` |
| `AZURE_SEARCH_SERVICE_NAME` | Azure Cognitive Search 서비스 이름 | `your-search-service-name` |
| `AZURE_SEARCH_API_KEY` | Azure Cognitive Search API 키 | `your_search_api_key_here` |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage Account 연결 문자열 | `DefaultEndpointsProtocol=https;AccountName=...` |
| `AZURE_STORAGE_CONTAINER_NAME` | Azure Storage 컨테이너 이름 | `documents` |

### Azure 배포용 시크릿

| 시크릿 이름 | 설명 | 설정 방법 |
|------------|------|-----------|
| `CSS_AZ_SECRET` | Azure 서비스 주체 인증 정보 | 아래 "Azure 서비스 주체 생성" 섹션 참조 |
| `AZURE_WEBAPP_NAME` | Azure Web App 이름 | `your-unique-app-name` |
| `AZURE_RESOURCE_GROUP` | Azure 리소스 그룹 이름 | `smartdoc-rg` |

## 3. Azure 서비스 주체 생성

### 3.1 Azure CLI로 서비스 주체 생성

```bash
# Azure에 로그인
az login

# 서비스 주체 생성
az ad sp create-for-rbac --name "smartdoc-github-actions" \
    --role contributor \
    --scopes /subscriptions/{subscription-id}/resourceGroups/smartdoc-rg \
    --sdk-auth
```

### 3.2 출력된 JSON을 CSS_AZ_SECRET로 설정

위 명령어 실행 후 출력되는 JSON을 복사하여 GitHub 시크릿 `CSS_AZ_SECRET`에 설정합니다.

```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

## 4. 시크릿 설정 예시

### 4.1 OpenAI API 키 설정

1. GitHub 리포지토리 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. Name: `OPENAI_API_KEY`
4. Secret: `sk-your-actual-openai-api-key`
5. "Add secret" 클릭

### 4.2 Azure Form Recognizer 설정

1. Name: `AZURE_FORM_RECOGNIZER_ENDPOINT`
2. Secret: `https://your-form-recognizer.cognitiveservices.azure.com/`

1. Name: `AZURE_FORM_RECOGNIZER_KEY`
2. Secret: `your-actual-form-recognizer-key`

### 4.3 Azure Storage 설정

1. Name: `AZURE_STORAGE_CONNECTION_STRING`
2. Secret: `DefaultEndpointsProtocol=https;AccountName=yourstorageaccount;AccountKey=your-key;EndpointSuffix=core.windows.net`

## 5. 시크릿 확인 방법

### 5.1 GitHub Actions에서 시크릿 사용

```yaml
- name: Deploy to Azure
  uses: azure/webapps-deploy@v2
  with:
    app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
    publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### 5.2 애플리케이션에서 환경 변수로 사용

```python
import os

openai_api_key = os.getenv('OPENAI_API_KEY')
azure_form_endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
```

## 6. 보안 주의사항

1. **시크릿 값은 절대 코드에 하드코딩하지 마세요**
2. **시크릿은 GitHub Actions에서만 사용하고 로그에 출력하지 마세요**
3. **정기적으로 API 키를 로테이션하세요**
4. **최소 권한 원칙을 적용하여 필요한 권한만 부여하세요**

## 7. 트러블슈팅

### 7.1 시크릿이 인식되지 않는 경우

- 시크릿 이름이 정확한지 확인 (대소문자 구분)
- GitHub Actions 워크플로우에서 올바른 문법 사용 확인
- 시크릿이 설정된 후 워크플로우가 실행되었는지 확인

### 7.2 Azure 인증 실패

- `CSS_AZ_SECRET` JSON 형식이 올바른지 확인
- 서비스 주체에 필요한 권한이 부여되었는지 확인
- 구독 ID와 리소스 그룹 이름이 정확한지 확인

## 8. 추가 리소스

- [GitHub Secrets 문서](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure 서비스 주체 생성 가이드](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
- [Azure Web Apps 배포 가이드](https://docs.microsoft.com/en-us/azure/app-service/deploy-github-actions)
