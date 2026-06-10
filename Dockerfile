# 1. 파이썬 기본 이미지 (로컬 환경: Python 3.13)
FROM python:3.13-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 종속성 설치를 위해 requirements.txt 복사
COPY requirements.txt .

# 4. 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 백엔드 코드 전체 복사
COPY . .

# apps/ 모듈 import (main.py, titanic, domain_intake 등)
ENV PYTHONPATH=.:apps

# 6. FastAPI가 실행될 포트 명시
EXPOSE 8000

# 7. Uvicorn을 이용해 FastAPI 실행 (main.py의 app 객체 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
