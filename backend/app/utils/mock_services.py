import random

def mock_generate_embedding(text: str) -> list:
    return [random.uniform(-1, 1) for _ in range(1536)]

def mock_get_embedding(text: str) -> list:
    return mock_generate_embedding(text)

def mock_detect_pii(text: str) -> list:
    return []

def mock_redact_pii(text: str) -> str:
    from app.utils.pii_redaction import redact_pii_regex
    return redact_pii_regex(text)

def mock_translate(text: str, target_lang: str) -> str:
    return text

def mock_registry_lookup(entity_id_or_domain: str | None = None, entity_name: str | None = None):
    safe_domain = (entity_id_or_domain or "").lower()
    safe_entity = (entity_name or "").lower()
    if "gov" in safe_domain or "official" in safe_entity:
        return {
            "entity_id": entity_id_or_domain or "mock-entity",
            "entity_name": entity_name,
            "domain": entity_id_or_domain,
            "verified_domains": [entity_id_or_domain or "example.gov"],
            "is_verified": True,
            "confidence": 0.95
        }
    return {
        "entity_id": entity_id_or_domain or "mock-entity",
        "entity_name": entity_name or "Mock Institution",
        "domain": entity_id_or_domain or "example.gov",
        "verified_domains": ["example.gov"],
        "is_verified": False,
        "confidence": 0.5,
    }
