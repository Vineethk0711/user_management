from minio import Minio
from minio.error import S3Error
from fastapi import UploadFile
from uuid import uuid4
from settings.config import (MINIO_ENDPOINT, MINIO_ACCESS_KEY,
                              MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_SECURE)

def get_client() -> Minio:
    return Minio(
        endpoint=MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )

def ensure_bucket(client: Minio):
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)

def save_profile_picture(file: UploadFile, user_id: int) -> str:
    client = get_client()
    ensure_bucket(client)
    object_name = f"{user_id}/{uuid4()}.{file.filename.split('.')[-1]}"
    client.put_object(
        MINIO_BUCKET,
        object_name,
        data=file.file,
        length=-1,
        part_size=10*1024*1024,   # stream any size
        content_type=file.content_type,
    )
    return f"{MINIO_ENDPOINT}/{MINIO_BUCKET}/{object_name}"
