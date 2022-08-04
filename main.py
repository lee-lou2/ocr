import os
import threading
import time
from typing import Union

import requests
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel
from utils.convert import (
    pdf_url_to_images,
)
from utils.crop_image import make_scan_image, focus_target_range
from utils.get_text import (
    get_text,
)
from utils.image_control import read_image, write_image_and_text


# 환경 변수 조회
load_dotenv(dotenv_path=".env", verbose=True)

# 앱 생성
app = FastAPI()


class RequestBody(BaseModel):
    name: Union[str, None] = None
    number: Union[str, None] = None
    call_back: Union[str, None] = None
    url: str


def _check_ocr(data: RequestBody):
    start = time.time()
    url = data.url
    name = data.name
    number = data.number
    call_back = data.call_back

    # 이미지 다운로드 및 변환
    images = pdf_url_to_images(pdf_url=url, dip=300, image_width=6000)
    image_file_name = images[0].filename

    # 이미지 범위 지정
    origin_image = read_image(image_file_name)

    # # 이미지 전처리
    # pre = ImagePreprocessing(origin_image)
    # origin_image = pre.remove_noise().opening().closing().image

    # 이미지 외곽 크롭
    origin_receipt_image = make_scan_image(origin_image)

    # 사용자 정보 포커스
    result_image = focus_target_range(origin_receipt_image)

    # 이미지 파일 제거
    for image in images:
        if os.path.isfile(image.filename):
            os.remove(image.filename)

    # 텍스트 추출
    text = get_text(result_image)

    if len(text) == 0:
        result_image = origin_image
        text = get_text(result_image)

    # 이미지 저장
    write_image_and_text(
        name if name else number if number else "-", text, result_image
    )

    # 결과 값 조회
    response = {"is_matched": {}, "text": text, "seconds": time.time() - start}
    if name:
        response["is_matched"]["name"] = name in text
    if number:
        response["is_matched"]["number"] = number in text

    # 결과 콜백
    if call_back:
        requests.post(call_back, json=response)
    return response


@app.post("/v1/ocr/check/")
def check_ocr(data: RequestBody):
    response = _check_ocr(data)
    return response


class T(threading.Thread):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self) -> None:
        _check_ocr(self.data)


@app.post("/v1/ocr/check/async/")
async def check_ocr(data: RequestBody):
    t = T(data=data)
    t.start()
    return {"success": True}
