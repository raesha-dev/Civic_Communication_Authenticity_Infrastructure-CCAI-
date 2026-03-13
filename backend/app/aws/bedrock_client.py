import json
import logging
from app.aws.session import bedrock_client
from app.config import Config
from app.utils.embedding_cache import get_cached_embedding, set_cached_embedding
from app.utils.mock_services import mock_get_embedding, mock_translate


logger = logging.getLogger(__name__)


def get_embedding(text: str) -> list:
    if Config.MOCK_MODE and Config.ALLOW_MOCK_FALLBACK:
        return mock_get_embedding(text)

    cached = get_cached_embedding(text)
    if cached is not None:
        return cached

    try:
        response = bedrock_client.invoke_model(
            modelId=Config.BEDROCK_EMBED_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": text}),
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding")
        if not embedding:
            raise ValueError("Bedrock embedding response did not include an embedding")
        set_cached_embedding(text, embedding)
        return embedding
    except Exception as error:
        logger.warning(json.dumps({
            "event": "bedrock_embedding_fallback",
            "model_id": Config.BEDROCK_EMBED_MODEL_ID,
            "error": str(error),
        }))
        return mock_get_embedding(text)


def translate_text(text: str, target_lang: str) -> str:
    if Config.MOCK_MODE and Config.ALLOW_MOCK_FALLBACK:
        return mock_translate(text, target_lang)

    try:
        prompt = (
            "Translate the following communication faithfully. "
            "Preserve meaning, legal tone, and risk indicators. "
            f"Target language: {target_lang}.\n\n{text}"
        )
        response = bedrock_client.invoke_model(
            modelId=Config.BEDROCK_TEXT_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {"maxTokenCount": 512, "temperature": 0.1},
            }),
        )
        response_body = json.loads(response["body"].read())
        return response_body["results"][0]["outputText"].strip()
    except Exception as error:
        logger.warning(json.dumps({
            "event": "bedrock_translation_fallback",
            "model_id": Config.BEDROCK_TEXT_MODEL_ID,
            "target_lang": target_lang,
            "error": str(error),
        }))
        return mock_translate(text, target_lang)
