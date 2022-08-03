import logging

import requests
import os
import uuid
from pdf2image import convert_from_path


def gen_file_name():
    """파일명 생성"""
    pdf_file_name = f"{uuid.uuid4()}.pdf"
    if os.path.isfile(pdf_file_name):
        gen_file_name()
    return pdf_file_name


def pdf_url_to_images(pdf_url: str, dip: int = 400, image_width: int = 2000):
    """PDF To Image"""
    try:
        pdf_file_name = f"data/{gen_file_name()}"

        resp = requests.get(pdf_url)
        if resp.status_code != 200:
            return None

        with open(pdf_file_name, "wb") as f:
            f.write(resp.content)

        jpegopt = {"quality": 100, "progressive": True, "optimize": True}
        images = convert_from_path(
            pdf_file_name,
            dpi=dip,
            fmt="jpeg",
            output_folder="data",
            jpegopt=jpegopt,
            size=(image_width, None),
            single_file=True,
        )

        # 파일 삭제
        if os.path.isfile(pdf_file_name):
            os.remove(pdf_file_name)
    except Exception as ex:
        logging.error(f"pdf_url_to_images : 변환 실패 : {ex}")
        images = None
    finally:
        return images
