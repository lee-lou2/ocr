FROM     ubuntu:20.04

RUN      apt-get update -y
RUN      apt-get upgrade -y
RUN      apt update -y

# Tesseract5 설치를 위한 라이브러리 설치
RUN      apt-get install software-properties-common -y
RUN      apt-get install -y git
RUN      apt-get install -y python3-pip
RUN      apt-get update -y

# Tesseract5 설치
RUN      add-apt-repository -y ppa:alex-p/tesseract-ocr5
RUN      apt install -y tesseract-ocr
RUN      apt-get install tesseract-ocr-kor -y

# 필수 라이브러리
RUN      apt-get install poppler-utils -y
RUN      apt-get install libgl1-mesa-glx -y

# 학습 데이터 다운로드
WORKDIR  /usr/share/tesseract-ocr/5
RUN      git clone https://github.com/tesseract-ocr/tessdata_best.git
RUN      mv tessdata tessdata_default
RUN      mv tessdata_best tessdata

COPY     ./requirements.txt /app/requirements.txt
RUN      pip3 install -U pip
RUN      pip3 install -r /app/requirements.txt

WORKDIR  /app

CMD      uvicorn main:app --host 0 --port 80

EXPOSE   80
