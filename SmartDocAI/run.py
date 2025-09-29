"""
SmartDoc AI 실행 스크립트
"""

import subprocess
import sys
import os

def main():
    """메인 실행 함수"""
    print("🚀 SmartDoc AI 시작 중...")
    
    # 현재 디렉토리를 src로 변경
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    # Streamlit 앱 실행
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py'
        ], cwd=src_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 실행 실패: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 SmartDoc AI를 종료합니다.")
        sys.exit(0)

if __name__ == "__main__":
    main()
