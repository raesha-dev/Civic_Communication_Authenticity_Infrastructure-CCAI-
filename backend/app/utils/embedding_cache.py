import json
from hashlib import sha256
from app.config import Config
from app.aws.s3_client import download_from_s3, upload_to_s3

_MEMORY_CACHE = {}

def _embedding_key(text: str) -> str:
    digest = sha256(text.encode("utf-8")).hexdigest()
    return f"embeddings/{digest}.json"

def get_cached_embedding(text: str):
    if text in _MEMORY_CACHE:
        return _MEMORY_CACHE[text]

    s3_key = _embedding_key(text)
    s3_data = download_from_s3(Config.S3_BUCKET_EMBEDDINGS, s3_key)
    if s3_data:
        data = json.loads(s3_data)
        _MEMORY_CACHE[text] = data["embedding"]
        return data["embedding"]

    return None

def set_cached_embedding(text: str, embedding: list):
    _MEMORY_CACHE[text] = embedding

    s3_key = _embedding_key(text)
    upload_to_s3(
        Config.S3_BUCKET_EMBEDDINGS,
        s3_key,
        json.dumps({"text": text, "embedding": embedding})
    )
