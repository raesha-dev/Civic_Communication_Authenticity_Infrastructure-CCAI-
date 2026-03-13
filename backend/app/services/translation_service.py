import json
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from app.aws.bedrock_client import get_embedding, translate_text
from app.aws.dynamodb_client import put_item
from app.config import Config
from app.utils.similarity_engine import compute_cosine_similarity


logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=3)


def translate_verified_message(original_text: str, target_lang: str) -> dict:
    start_time = time.time()
    original_embedding_future = executor.submit(get_embedding, original_text)
    translated_text = translate_text(original_text, target_lang)

    orig_emb = original_embedding_future.result()
    trans_emb = get_embedding(translated_text)
    similarity = compute_cosine_similarity(orig_emb, trans_emb)
    integrity_status = "HIGH" if similarity >= Config.TRANSLATION_THRESHOLD else "WARNING"

    result = {
        "translation_id": str(uuid.uuid4()),
        "original_text_length": len(original_text),
        "translated_text": translated_text,
        "target_language": target_lang,
        "translation_integrity_score": round(similarity, 4),
        "integrity_status": integrity_status,
        "processing_time_ms": int((time.time() - start_time) * 1000),
        "created_at": int(time.time()),
    }

    put_item("Translations", result)
    logger.info(json.dumps({
        "event": "translation_request",
        "translation_id": result["translation_id"],
        "target_language": target_lang,
        "latency_ms": result["processing_time_ms"],
        "aws_calls": 3,
    }))
    return result
