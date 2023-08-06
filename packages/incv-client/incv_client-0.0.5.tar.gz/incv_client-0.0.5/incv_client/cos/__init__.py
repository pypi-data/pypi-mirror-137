from io import BytesIO

from django.conf import settings
from qcloud_cos import CosConfig, CosS3Client


class COSClient:
    def __init__(self, union):
        self.__union = union
        self.__client = CosS3Client(
            CosConfig(
                Region=settings.COS_REGION,
                SecretId=settings.TCLOUD_SECRET_ID,
                SecretKey=settings.TCLOUD_SECRET_KEY,
            )
        )
        self.bucket = settings.COS_BUCKET

    def upload(self, key: str, file: BytesIO):
        """上传文件"""
        try:
            # 上传文件
            resp = self.__client.put_object(Bucket=self.bucket, Key=key, Body=file)
            if resp.get("ETag"):
                return True, resp
            else:
                return False, resp
        except Exception as err:
            return False, err
