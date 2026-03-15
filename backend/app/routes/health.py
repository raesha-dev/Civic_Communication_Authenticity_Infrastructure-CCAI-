from flask import Blueprint, jsonify
from app.aws.dynamodb_client import describe_table
from app.aws.session import (
    is_mock_mode,
    mock_mode_reason,
    s3_client,
    service_available,
    sqs_client,
)
from app.config import Config


health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def health_check():
    mock_mode = is_mock_mode()
    status = {
        "status": "online" if not mock_mode else "degraded",
        "mock_mode": mock_mode,
        "mock_reason": mock_mode_reason() if mock_mode else None,
        "services": {
            "dynamodb": "mock" if mock_mode else "ok",
            "s3": "mock" if mock_mode else "ok",
            "bedrock": "mock" if mock_mode else "ok",
            "comprehend": "mock" if mock_mode else "ok",
            "sqs": "mock" if mock_mode else "ok",
        },
    }

    if mock_mode:
        return jsonify(status)

    if not service_available("dynamodb_client") or not describe_table("InstitutionalRegistry"):
        status["services"]["dynamodb"] = "error"

    if service_available("s3") and s3_client is not None:
        try:
            s3_client.head_bucket(Bucket=Config.S3_BUCKET_EMBEDDINGS)
        except Exception:
            status["services"]["s3"] = "error"
    else:
        status["services"]["s3"] = "error"

    if not service_available("bedrock"):
        status["services"]["bedrock"] = "error"

    if not service_available("comprehend"):
        status["services"]["comprehend"] = "error"

    if Config.APPEALS_QUEUE_URL:
        if service_available("sqs") and sqs_client is not None:
            try:
                sqs_client.get_queue_attributes(
                    QueueUrl=Config.APPEALS_QUEUE_URL,
                    AttributeNames=["QueueArn"],
                )
            except Exception:
                status["services"]["sqs"] = "error"
        else:
            status["services"]["sqs"] = "error"
    elif not mock_mode:
        status["services"]["sqs"] = "not_configured"

    if any(value == "error" for value in status["services"].values()):
        status["status"] = "degraded"

    return jsonify(status)
