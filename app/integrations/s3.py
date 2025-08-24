from datetime import timedelta
from typing import Any

import boto3

from app.core.settings import get_settings


def get_s3_client():
    settings = get_settings()
    return boto3.client(
        service_name="s3",
        region_name=settings.s3_region,
        aws_access_key_id=settings.s3_access_key_id,
        aws_secret_access_key=settings.s3_secret_access_key,
    )


def create_presigned_put_url(
    key: str,
    expires_in: int = 900,
) -> str:
    settings = get_settings()
    client = get_s3_client()
    return client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def create_presigned_get_url(
    key: str,
    expires_in: int = 900,
) -> str:
    settings = get_settings()
    client = get_s3_client()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expires_in,
    )


