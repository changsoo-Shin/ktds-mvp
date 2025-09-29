"""
SmartDoc AI 설치 스크립트
"""

import subprocess
import sys
import os

def install_requirements():
    """requirements.txt 설치"""
    print("📦 의존성 패키지 설치 중...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True)
        print("✅ 의존성 설치 완료!")
    except subprocess.CalledProcessError as e:
        print(f"❌ 설치 실패: {e}")
        return False
    return True

def create_env_file():
    """환경 변수 파일 생성"""
    env_file = '.env'
    env_sample = '.env.sample'
    
    if not os.path.exists(env_file):
        if os.path.exists(env_sample):
            print("📝 환경 변수 파일 생성 중...")
            with open(env_sample, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ .env 파일이 생성되었습니다.")
            print("⚠️  .env 파일을 열어서 Azure 서비스 정보를 입력해주세요.")
        else:
            print("❌ .env.sample 파일을 찾을 수 없습니다.")
            return False
    else:
        print("ℹ️  .env 파일이 이미 존재합니다.")
    
    return True

def main():
    """메인 설치 함수"""
    print("🛠️  SmartDoc AI 설치 시작...")
    
    # 의존성 설치
    if not install_requirements():
        return
    
    # 환경 변수 파일 생성
    if not create_env_file():
        return
    
    print("\n🎉 SmartDoc AI 설치 완료!")
    print("\n📋 다음 단계:")
    print("1. .env 파일을 열어서 Azure 서비스 정보를 입력하세요")
    print("2. python run.py 명령어로 애플리케이션을 실행하세요")
    print("\n🔗 필요한 Azure 서비스:")
    print("- Azure OpenAI (GPT-4o-mini 모델)")
    print("- Azure AI Search")

if __name__ == "__main__":
    main()
