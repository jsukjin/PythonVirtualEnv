import sys
import platform

print("=" * 40)
print("Docker + Miniforge 테스트")
print("=" * 40)
print(f"Python 버전: {sys.version}")
print(f"OS: {platform.system()} {platform.release()}")
print("정상 실행 확인!")