import logging
import os
import datetime
import threading

import cv2
from utils.aws_s3 import S3


def read_image(path: str):
    """이미지 불러오기"""
    return cv2.imread(path)


class T(threading.Thread):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self) -> None:
        save_file(self.data)


def save_file(data: dict):
    """파일 저장"""
    image_file_name = data.get("image_file_name")
    image_path = data.get("image_path") + image_file_name
    image = data.get("image")
    text_file_name = data.get("text_file_name")
    text_path = data.get("text_path") + text_file_name
    text = data.get("text")

    # 이미지 저장
    cv2.imwrite(image_path, image)

    # 텍스트 저장
    f = open(text_path, "w")
    f.write(text)
    f.close()

    # 로그 기록
    upload_log(image_path)
    upload_log(text_path)

    # 파일 제거
    if os.path.isfile(image_path):
        os.remove(image_path)
    if os.path.isfile(text_path):
        os.remove(text_path)

    logging.info("로그 기록 완료")


def upload_log(file_name: str, upload_file_path: str = None):
    """로그 기록"""
    S3().upload_file(file_name, upload_file_path)


def write_image_and_text(name: str, text: str, image):
    """이미지 및 텍스트 저장"""
    now = datetime.datetime.now()
    now_str = now.strftime("%H:%M:%S")
    path = f"data/log/{now.year}/{now.month}/{now.day}"

    # 디렉토리 생성
    dir_str = ""
    for _dir in ["data", "log", str(now.year), str(now.month), str(now.day)]:
        dir_str = f"{dir_str}{_dir}/"
        if not os.path.isdir(dir_str):
            os.mkdir(dir_str)

    t = T({
        "image_file_name": f"{now_str}_{name}_image.jpg",
        "image_path": f"{path}/",
        "image": image,
        "text_file_name": f"{now_str}_{name}_text.txt",
        "text_path": f"{path}/",
        "text": text
    })
    t.start()
