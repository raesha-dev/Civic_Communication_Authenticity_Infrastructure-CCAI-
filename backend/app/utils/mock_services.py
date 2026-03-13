import random

def mock_get_embedding(text: str) -> list:
    return [random.uniform(-1, 1) for _ in range(1536)]

def mock_redact_pii(text: str) -> str:
    from app.utils.pii_redaction import redact_pii_regex
    return redact_pii_regex(text)

def mock_translate(text: str, target_lang: str) -> str:
    return f"[Translated to {target_lang}]: {text}"

def mock_registry_lookup(domain: str, entity_name: str):
    safe_domain = (domain or "").lower()
    safe_entity = (entity_name or "").lower()
    if "gov" in safe_domain or "official" in safe_entity:
        return {
            "entity_name": entity_name,
            "domain": domain,
            "is_verified": True,
            "confidence": 0.95
        }
    return None
