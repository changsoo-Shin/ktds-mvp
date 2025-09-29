#!/usr/bin/env python3
"""
환경 변수 설정 도우미 스크립트
Azure AI Search 인덱스 이름 누락 문제 해결
"""

import os
from pathlib import Path

def setup_environment():
    """환경 변수 설정"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env 파일을 찾을 수 없습니다.")
        return False
    
    # 현재 .env 파일 읽기
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # AZURE_SEARCH_INDEX_NAME이 있는지 확인
    has_index_name = 'AZURE_SEARCH_INDEX_NAME' in content
    
    # 현재 인덱스 이름 확인
    current_index = os.getenv('AZURE_SEARCH_INDEX_NAME')
    correct_index = 'smartdoc-index'
    
    if not has_index_name:
        print("✅ AZURE_SEARCH_INDEX_NAME 환경 변수를 추가합니다...")
        
        # 새 줄 추가
        with open(env_file, 'a', encoding='utf-8') as f:
            f.write(f'\nAZURE_SEARCH_INDEX_NAME={correct_index}\n')
        
        print("✅ 환경 변수 설정 완료!")
        return True
    elif current_index != correct_index:
        print(f"⚠️ 잘못된 인덱스 이름 발견: '{current_index}' -> '{correct_index}'로 수정합니다...")
        
        # 기존 라인 교체
        updated_content = content
        if 'AZURE_SEARCH_INDEX_NAME=' in content:
            import re
            updated_content = re.sub(
                r'AZURE_SEARCH_INDEX_NAME=.*',
                f'AZURE_SEARCH_INDEX_NAME={correct_index}',
                content
            )
        else:
            updated_content += f'\nAZURE_SEARCH_INDEX_NAME={correct_index}\n'
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ 인덱스 이름 수정 완료!")
        return True
    else:
        print("✅ AZURE_SEARCH_INDEX_NAME이 올바르게 설정되어 있습니다.")
        return True

def check_environment():
    """환경 변수 확인"""
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_SEARCH_ENDPOINT',
        'AZURE_SEARCH_API_KEY',
        'AZURE_SEARCH_INDEX_NAME'
    ]
    
    print("환경 변수 확인:")
    print("-" * 50)
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # API 키는 일부만 표시
            if 'KEY' in var:
                display_value = value[:10] + "..." if len(value) > 10 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 설정되지 않음")
            missing_vars.append(var)
    
    print("-" * 50)
    
    if missing_vars:
        print(f"❌ 누락된 환경 변수: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ 모든 필수 환경 변수가 설정되었습니다!")
        return True

if __name__ == "__main__":
    print("SmartDoc AI 환경 설정 도우미")
    print("=" * 50)
    
    # 환경 변수 로드
    from dotenv import load_dotenv
    load_dotenv()
    
    # 환경 설정
    setup_success = setup_environment()
    
    if setup_success:
        # 다시 로드
        load_dotenv()
        
        # 환경 변수 확인
        check_environment()
        
        print("\n다음 단계:")
        print("1. 애플리케이션을 다시 시작하세요")
        print("2. 문서를 업로드하여 AI 컴포넌트 초기화를 테스트하세요")
    else:
        print("❌ 환경 설정에 실패했습니다.")
