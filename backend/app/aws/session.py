import boto3
from botocore.config import Config as BotoConfig
from app.config import Config


_BOTO_CONFIG = BotoConfig(
    region_name=Config.AWS_REGION,
    retries={"max_attempts": 3, "mode": "standard"},
    max_pool_connections=Config.AWS_MAX_POOL_CONNECTIONS,
    tcp_keepalive=True,
    connect_timeout=2,
    read_timeout=4,
)

session = boto3.session.Session(region_name=Config.AWS_REGION)

bedrock_client = session.client("bedrock-runtime", config=_BOTO_CONFIG)
dynamodb = session.resource(
    "dynamodb",
    endpoint_url=Config.DYNAMODB_ENDPOINT,
    config=_BOTO_CONFIG,
)
dynamodb_client = session.client(
    "dynamodb",
    endpoint_url=Config.DYNAMODB_ENDPOINT,
    config=_BOTO_CONFIG,
)
s3_client = session.client(
    "s3",
    endpoint_url=Config.S3_ENDPOINT,
    config=_BOTO_CONFIG,
)
comprehend_client = session.client("comprehend", config=_BOTO_CONFIG)
sqs_client = session.client(
    "sqs",
    endpoint_url=Config.SQS_ENDPOINT,
    config=_BOTO_CONFIG,
)
