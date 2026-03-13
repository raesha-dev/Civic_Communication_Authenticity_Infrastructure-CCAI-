import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
    ALLOW_MOCK_FALLBACK = os.getenv("ALLOW_MOCK_FALLBACK", "true").lower() == "true"
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", None)
    S3_ENDPOINT = os.getenv("S3_ENDPOINT", None)
    SQS_ENDPOINT = os.getenv("SQS_ENDPOINT", None)
    AWS_MAX_POOL_CONNECTIONS = int(os.getenv("AWS_MAX_POOL_CONNECTIONS", "50"))

    ANALYSIS_RESULTS_TABLE = os.getenv("ANALYSIS_RESULTS_TABLE", "AnalysisResults")
    TRANSLATIONS_TABLE = os.getenv("TRANSLATIONS_TABLE", "Translations")
    APPEALS_TABLE = os.getenv("APPEALS_TABLE", "Appeals")
    REGISTRY_TABLE = os.getenv("REGISTRY_TABLE", "InstitutionalRegistry")
    AUDIT_LOGS_TABLE = os.getenv("AUDIT_LOGS_TABLE", "AuditLogs")

    REGISTRY_DOMAIN_INDEX_NAME = os.getenv("REGISTRY_DOMAIN_INDEX_NAME", "domain-index")
    REGISTRY_ENTITY_INDEX_NAME = os.getenv("REGISTRY_ENTITY_INDEX_NAME", "entity-name-index")
    REGISTRY_DOMAIN_ATTRIBUTE = os.getenv("REGISTRY_DOMAIN_ATTRIBUTE", "domain")
    REGISTRY_ENTITY_ATTRIBUTE = os.getenv("REGISTRY_ENTITY_ATTRIBUTE", "entity_name")

    BEDROCK_EMBED_MODEL_ID = os.getenv("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v1")
    BEDROCK_TEXT_MODEL_ID = os.getenv("BEDROCK_TEXT_MODEL_ID", "amazon.titan-text-express-v1")
    APPEALS_QUEUE_URL = os.getenv("APPEALS_QUEUE_URL", "")

    # Weights
    DOMAIN_VERIFICATION_WEIGHT = 0.40
    SEMANTIC_SIMILARITY_WEIGHT = 0.35
    FRAUD_DETECTION_WEIGHT = 0.25

    # Thresholds
    TRANSLATION_THRESHOLD = 0.75

    S3_BUCKET_EMBEDDINGS = os.getenv("S3_BUCKET_EMBEDDINGS", "ccai-embeddings")
    S3_BUCKET_LOGS = os.getenv("S3_BUCKET_LOGS", "ccai-audit-logs")

    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-for-mvp")
    REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "4.5"))
