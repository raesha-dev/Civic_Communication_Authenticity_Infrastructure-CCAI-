import json
import logging
import os
from app.config import Config

try:
    import boto3
    from botocore.config import Config as BotoConfig
except ModuleNotFoundError:
    boto3 = None

    class BotoConfig:  # type: ignore[override]
        def __init__(self, **_kwargs):
            pass


os.environ.setdefault("AWS_EC2_METADATA_DISABLED", "true")

logger = logging.getLogger(__name__)
_BOTO_CONFIG = BotoConfig(
    region_name=Config.AWS_REGION,
    retries={"max_attempts": 3, "mode": "standard"},
    max_pool_connections=Config.AWS_MAX_POOL_CONNECTIONS,
    tcp_keepalive=True,
    connect_timeout=2,
    read_timeout=4,
)

SERVICE_STATUS = {
    "bedrock": False,
    "dynamodb": False,
    "dynamodb_client": False,
    "s3": False,
    "comprehend": False,
    "sqs": False,
}

RUNTIME_MOCK_MODE = False
RUNTIME_MOCK_REASON = "aws_ready"


def _activate_mock_mode(reason: str, error: Exception | None = None):
    global RUNTIME_MOCK_MODE, RUNTIME_MOCK_REASON
    RUNTIME_MOCK_MODE = True
    RUNTIME_MOCK_REASON = reason
    logger.warning(json.dumps({
        "event": "mock_mode_activated",
        "reason": reason,
        "error": str(error) if error else None,
    }))


def _create_session():
    if Config.MOCK_MODE:
        _activate_mock_mode("env_mock_mode")
        return None

    if boto3 is None:
        _activate_mock_mode("boto3_unavailable")
        return None

    try:
        session = boto3.session.Session(region_name=Config.AWS_REGION)
    except Exception as error:
        _activate_mock_mode("session_init_failed", error)
        return None

    if session.get_credentials() is None:
        _activate_mock_mode("missing_aws_credentials")
        return None

    return session


def _safe_client(session, service_name: str, *, endpoint_url: str | None = None, resource: bool = False):
    if session is None:
        return None

    try:
        client = (
            session.resource(service_name, endpoint_url=endpoint_url, config=_BOTO_CONFIG)
            if resource
            else session.client(service_name, endpoint_url=endpoint_url, config=_BOTO_CONFIG)
        )
        SERVICE_STATUS[service_name if not resource else "dynamodb"] = True
        return client
    except Exception as error:
        SERVICE_STATUS[service_name if not resource else "dynamodb"] = False
        _activate_mock_mode(f"{service_name}_init_failed", error)
        return None


session = _create_session()
bedrock_client = _safe_client(session, "bedrock-runtime")
dynamodb = _safe_client(session, "dynamodb", endpoint_url=Config.DYNAMODB_ENDPOINT, resource=True)
dynamodb_client = _safe_client(session, "dynamodb", endpoint_url=Config.DYNAMODB_ENDPOINT)
s3_client = _safe_client(session, "s3", endpoint_url=Config.S3_ENDPOINT)
comprehend_client = _safe_client(session, "comprehend")
sqs_client = _safe_client(session, "sqs", endpoint_url=Config.SQS_ENDPOINT)

if dynamodb_client is not None:
    SERVICE_STATUS["dynamodb_client"] = True


def is_mock_mode() -> bool:
    return Config.MOCK_MODE or RUNTIME_MOCK_MODE


def mock_mode_reason() -> str:
    return "env_mock_mode" if Config.MOCK_MODE else RUNTIME_MOCK_REASON


def service_available(service_name: str) -> bool:
    return SERVICE_STATUS.get(service_name, False) and not is_mock_mode()
