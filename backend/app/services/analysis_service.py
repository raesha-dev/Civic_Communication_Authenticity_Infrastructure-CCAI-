import json
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from app.aws.bedrock_client import get_embedding
from app.aws.comprehend_client import detect_and_redact_pii
from app.aws.dynamodb_client import put_item
from app.services.fraud_detection_service import detect_fraud_signals
from app.services.registry_service import verify_institutional_source
from app.services.scoring_service import calculate_authenticity_score
from app.utils.similarity_engine import compute_cosine_similarity


logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=4)


def _reference_text(registry_match: dict | None) -> str | None:
    if not registry_match:
        return None
    for field in ("reference_text", "official_message", "official_summary", "description"):
        value = registry_match.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def analyze_communication(text: str, channel_type: str, metadata: dict) -> dict:
    start_time = time.time()
    domain = metadata.get("domain", "")
    entity_name = metadata.get("entity_name", "")

    pii_future = executor.submit(detect_and_redact_pii, text)
    registry_future = executor.submit(verify_institutional_source, domain, entity_name)

    redacted_text = pii_future.result()
    registry_result = registry_future.result()

    embedding_future = executor.submit(get_embedding, redacted_text)
    fraud_future = executor.submit(detect_fraud_signals, redacted_text)
    embedding = embedding_future.result()
    fraud_result = fraud_future.result()

    reference_text = _reference_text(registry_result.get("match"))
    if reference_text:
        reference_embedding = get_embedding(reference_text)
        semantic_similarity = compute_cosine_similarity(embedding, reference_embedding)
    else:
        semantic_similarity = 0.65 if registry_result["is_verified"] else 0.3

    score_result = calculate_authenticity_score(
        domain_verified=registry_result["is_verified"],
        semantic_similarity=semantic_similarity,
        fraud_penalty=fraud_result["fraud_score_penalty"],
    )

    explainable_flags = []
    if registry_result["is_verified"]:
        explainable_flags.append("Domain verified against institutional registry.")
    else:
        explainable_flags.append("Origin domain not found in institutional registry.")

    if fraud_result["has_fraud_signals"]:
        for flag in fraud_result["flags"]:
            explainable_flags.append(f"Caution: {flag['description']}")

    if reference_text:
        if semantic_similarity > 0.8:
            explainable_flags.append("High semantic coherence with known institutional tone.")
    else:
        explainable_flags.append("No official semantic baseline found in registry; conservative similarity weighting applied.")

    analysis_id = str(uuid.uuid4())
    processing_time_ms = int((time.time() - start_time) * 1000)
    result = {
        "analysis_id": analysis_id,
        "authenticity_score": score_result["authenticity_score"],
        "raw_score": score_result["raw_score"],
        "breakdown": score_result["breakdown"],
        "confidence": registry_result["confidence"] if registry_result["is_verified"] else 0.5,
        "explainable_flags": explainable_flags,
        "fraud_signals": fraud_result["flags"],
        "redacted_text": redacted_text,
        "registry_match": registry_result.get("match"),
        "semantic_similarity": round(semantic_similarity, 4),
        "translation_allowed": score_result["authenticity_score"] >= 4,
        "processing_time_ms": processing_time_ms,
        "channel_type": channel_type,
        "created_at": int(time.time()),
        "ttl": int(time.time()) + (90 * 24 * 60 * 60),
    }

    put_item("AnalysisResults", result)
    logger.info(json.dumps({
        "event": "analysis_request",
        "analysis_id": analysis_id,
        "latency_ms": processing_time_ms,
        "aws_calls": 3,
        "fallback_active": reference_text is None,
    }))
    return result
