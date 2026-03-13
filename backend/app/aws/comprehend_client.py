import json
import logging
from app.aws.session import comprehend_client
from app.config import Config
from app.utils.mock_services import mock_redact_pii


logger = logging.getLogger(__name__)


def detect_and_redact_pii(text: str) -> str:
    if Config.MOCK_MODE and Config.ALLOW_MOCK_FALLBACK:
        return mock_redact_pii(text)

    try:
        response = comprehend_client.detect_pii_entities(
            Text=text,
            LanguageCode="en",
        )
        entities = response.get("Entities", [])
        if not entities:
            return text

        redacted_text = text
        for entity in sorted(entities, key=lambda item: item["BeginOffset"], reverse=True):
            begin = entity["BeginOffset"]
            end = entity["EndOffset"]
            entity_type = entity["Type"]
            redacted_text = redacted_text[:begin] + f"[{entity_type}]" + redacted_text[end:]
        return redacted_text
    except Exception as error:
        logger.warning(json.dumps({
            "event": "comprehend_pii_fallback",
            "error": str(error),
        }))
        return mock_redact_pii(text)
