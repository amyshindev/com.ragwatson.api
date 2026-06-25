import torch

print("안녕하세요! 파이토치 실행 중입니다.")
print(f"사용한 파이토치 버전: {torch.__version__}")
print(f"그래픽카드(GPU) 사용 가능 여부: {torch.cuda.is_available()}")
