import logging
import os

import boto3


class S3:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION")
        )
        self.bucket = os.environ.get("DEFAULT_S3_BUCKET")

    def download_file(self, file_name: str, download_file_path: str):
        try:
            self.s3.download_file(self.bucket, file_name, download_file_path)
        except Exception as ex:
            logging.error(f"S3 파일 다운로드 간 오류 발생 : {ex}")
            return False
        return True

    def upload_file(self, file_name: str, upload_file_path: str = None):
        if upload_file_path is None:
            upload_file_path = file_name
        try:
            self.s3.upload_file(file_name, self.bucket, upload_file_path)
        except Exception as ex:
            logging.error(f"S3 파일 업로드 간 오류 발생 : {ex}")
            return False
        return True
