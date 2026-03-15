import json
import logging
import time
import uuid
from flask import Blueprint, jsonify, request
from app.aws.dynamodb_client import put_item
from app.aws.session import sqs_client
from app.config import Config
from app.models.translation_model import AppealRequest, ValidationError
from app.utils.http import error_response


appeals_bp = Blueprint("appeals", __name__)
logger = logging.getLogger(__name__)


@appeals_bp.route("/", methods=["POST"])
def submit_appeal():
    try:
        data = request.get_json()
        if not data:
            return error_response("BAD_REQUEST", "No JSON payload", 400)

        validated_data = AppealRequest(**data)
        appeal_id = str(uuid.uuid4())
        appeal_record = {
            "appeal_id": appeal_id,
            "analysis_id": validated_data.analysis_id,
            "reason": validated_data.reason,
            "contact_email": validated_data.contact_email,
            "status": "PENDING",
            "created_at": int(time.time()),
        }

        put_item("Appeals", appeal_record)

        queue_status = "stored_only"
        if Config.APPEALS_QUEUE_URL:
            try:
                sqs_client.send_message(
                    QueueUrl=Config.APPEALS_QUEUE_URL,
                    MessageBody=json.dumps(appeal_record),
                )
                queue_status = "queued"
            except Exception as error:
                logger.warning(json.dumps({
                    "event": "appeal_queue_fallback",
                    "appeal_id": appeal_id,
                    "error": str(error),
                }))

        return jsonify({
            "message": "Appeal submitted successfully",
            "appeal_id": appeal_id,
            "status": "PENDING",
            "queue_status": queue_status,
        }), 201
    except ValidationError as error:
        return error_response("VALIDATION_ERROR", error.errors(), 400)
    except Exception as error:
        return error_response("SERVICE_ERROR", str(error), 500)
