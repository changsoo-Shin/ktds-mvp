#!/usr/bin/env python3
"""
Azure OpenAI 환경 변수 설정 도우미 스크립트
"""

import os
import sys

def setup_environment():
    """환경 변수 설정 도우미"""
    print("🔧 Azure OpenAI 환경 변수 설정 도우미")
    print("=" * 50)
    
    # 현재 환경 변수 확인
    print("\n📋 현재 설정된 환경 변수:")
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT', 
        'AZURE_OPENAI_API_VERSION',
        'AZURE_OPENAI_DEPLOYMENT_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # API 키는 보안을 위해 일부만 표시
            if 'API_KEY' in var:
                display_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: 설정되지 않음")
            missing_vars.append(var)
    
    if not missing_vars:
        print("\n🎉 모든 필수 환경 변수가 설정되어 있습니다!")
        return True
    
    print(f"\n⚠️  {len(missing_vars)}개의 필수 환경 변수가 설정되지 않았습니다.")
    print("\n📝 설정 방법:")
    print("1. Azure Portal에서 Azure OpenAI 서비스를 생성하세요")
    print("2. API 키와 엔드포인트를 확인하세요")
    print("3. 다음 중 하나의 방법으로 설정하세요:")
    print("\n   방법 A: .env 파일 생성")
    print("   - SmartDocAI 폴더에 .env 파일을 생성하고 다음 내용을 추가:")
    print("   AZURE_OPENAI_API_KEY=your_actual_api_key")
    print("   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
    print("   AZURE_OPENAI_API_VERSION=2024-02-15-preview")
    print("   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini")
    
    print("\n   방법 B: PowerShell에서 환경 변수 설정")
    print("   $env:AZURE_OPENAI_API_KEY='your_actual_api_key'")
    print("   $env:AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'")
    print("   $env:AZURE_OPENAI_API_VERSION='2024-02-15-preview'")
    print("   $env:AZURE_OPENAI_DEPLOYMENT_NAME='gpt-4o-mini'")
    
    print("\n   방법 C: 이 스크립트에서 직접 설정")
    setup_interactive = input("\n지금 설정하시겠습니까? (y/n): ").lower().strip()
    
    if setup_interactive == 'y':
        return setup_interactive_mode()
    
    return False

def setup_interactive_mode():
    """대화형 설정 모드"""
    print("\n🔧 대화형 설정 모드")
    print("=" * 30)
    
    try:
        api_key = input("Azure OpenAI API 키를 입력하세요: ").strip()
        if not api_key:
            print("❌ API 키가 입력되지 않았습니다.")
            return False
            
        endpoint = input("Azure OpenAI 엔드포인트를 입력하세요 (예: https://your-resource.openai.azure.com/): ").strip()
        if not endpoint:
            print("❌ 엔드포인트가 입력되지 않았습니다.")
            return False
            
        api_version = input("API 버전을 입력하세요 (기본값: 2024-02-15-preview): ").strip()
        if not api_version:
            api_version = "2024-02-15-preview"
            
        deployment_name = input("배포 이름을 입력하세요 (기본값: gpt-4o-mini): ").strip()
        if not deployment_name:
            deployment_name = "gpt-4o-mini"
        
        # 환경 변수 설정
        os.environ['AZURE_OPENAI_API_KEY'] = api_key
        os.environ['AZURE_OPENAI_ENDPOINT'] = endpoint
        os.environ['AZURE_OPENAI_API_VERSION'] = api_version
        os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'] = deployment_name
        
        print("\n✅ 환경 변수가 설정되었습니다!")
        print("⚠️  주의: 이 설정은 현재 세션에서만 유효합니다.")
        print("영구적으로 설정하려면 .env 파일을 생성하거나 시스템 환경 변수를 설정하세요.")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n❌ 설정이 취소되었습니다.")
        return False
    except Exception as e:
        print(f"\n❌ 설정 중 오류가 발생했습니다: {str(e)}")
        return False

def test_ai_assistant():
    """AI 어시스턴트 초기화 테스트"""
    print("\n🧪 AI 어시스턴트 초기화 테스트")
    print("=" * 40)
    
    try:
        # AI 어시스턴트 모듈 임포트 및 테스트
        sys.path.append('src')
        from ai_assistant import AIAssistant
        
        print("AI 어시스턴트 초기화 중...")
        assistant = AIAssistant()
        print("✅ AI 어시스턴트 초기화 성공!")
        return True
        
    except Exception as e:
        print(f"❌ AI 어시스턴트 초기화 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("SmartDoc AI - 환경 설정 도우미")
    print("=" * 50)
    
    # 환경 변수 설정 확인
    if setup_environment():
        # AI 어시스턴트 테스트
        if test_ai_assistant():
            print("\n🎉 모든 설정이 완료되었습니다!")
            print("이제 'streamlit run src/app.py' 명령어로 애플리케이션을 실행할 수 있습니다.")
        else:
            print("\n❌ AI 어시스턴트 초기화에 실패했습니다.")
            print("환경 변수 설정을 다시 확인해주세요.")
    else:
        print("\n❌ 환경 변수 설정이 완료되지 않았습니다.")
        print("위의 안내에 따라 환경 변수를 설정한 후 다시 실행해주세요.")
