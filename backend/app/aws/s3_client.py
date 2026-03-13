import json
import logging
import os
from app.aws.session import s3_client


logger = logging.getLogger(__name__)
LOCAL_CACHE_DIR = "/tmp/ccai_s3_fallback"
os.makedirs(LOCAL_CACHE_DIR, exist_ok=True)


def _local_cache_path(key: str) -> str:
    return os.path.join(LOCAL_CACHE_DIR, key.replace("/", "_"))


def _write_local(key: str, data: str):
    with open(_local_cache_path(key), "w", encoding="utf-8") as file_obj:
        file_obj.write(data)


def upload_to_s3(bucket: str, key: str, data: str):
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data.encode("utf-8"),
            ContentType="application/json",
        )
        return True
    except Exception as error:
        logger.warning(json.dumps({
            "event": "s3_upload_fallback",
            "bucket": bucket,
            "key": key,
            "error": str(error),
        }))
        _write_local(key, data)
        return True


def download_from_s3(bucket: str, key: str):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read().decode("utf-8")
    except Exception as error:
        logger.warning(json.dumps({
            "event": "s3_download_fallback",
            "bucket": bucket,
            "key": key,
            "error": str(error),
        }))
        local_path = _local_cache_path(key)
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as file_obj:
                return file_obj.read()
        return None
