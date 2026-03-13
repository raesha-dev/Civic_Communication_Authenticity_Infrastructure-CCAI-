from flask import Blueprint, jsonify
from app.aws.dynamodb_client import describe_table
from app.aws.session import bedrock_client, comprehend_client, s3_client, sqs_client
from app.config import Config
import json


health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def health_check():
    status = {
        "status": "online",
        "mock_mode": Config.MOCK_MODE,
        "services": {
            "dynamodb": "ok",
            "s3": "ok",
            "bedrock": "ok",
            "comprehend": "ok",
            "sqs": "ok",
        },
    }

    if not describe_table("InstitutionalRegistry"):
        status["services"]["dynamodb"] = "error"
    try:
        s3_client.head_bucket(Bucket=Config.S3_BUCKET_EMBEDDINGS)
    except Exception:
        status["services"]["s3"] = "error"
    try:
        bedrock_client.invoke_model(
            modelId=Config.BEDROCK_EMBED_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": "health"}),
        )
    except Exception:
        status["services"]["bedrock"] = "error"
    try:
        comprehend_client.detect_pii_entities(Text="health check", LanguageCode="en")
    except Exception:
        status["services"]["comprehend"] = "error"
    if Config.APPEALS_QUEUE_URL:
        try:
            sqs_client.get_queue_attributes(
                QueueUrl=Config.APPEALS_QUEUE_URL,
                AttributeNames=["QueueArn"],
            )
        except Exception:
            status["services"]["sqs"] = "error"

    if any(value == "error" for value in status["services"].values()):
        status["status"] = "degraded"

    return jsonify(status)
