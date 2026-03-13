from flask import Blueprint, jsonify
from app.aws.dynamodb_client import describe_table
from app.config import Config

methodology_bp = Blueprint('methodology', __name__)

@methodology_bp.route('/', methods=['GET'])
def get_methodology():
    registry_metadata = describe_table("InstitutionalRegistry")
    return jsonify({
        "scoring_weights": {
            "domain_verification": Config.DOMAIN_VERIFICATION_WEIGHT,
            "semantic_similarity": Config.SEMANTIC_SIMILARITY_WEIGHT,
            "fraud_detection_penalty": Config.FRAUD_DETECTION_WEIGHT
        },
        "score_mapping": {
            "5": ">= 0.80",
            "4": "0.60 - 0.79",
            "3": "0.40 - 0.59",
            "2": "0.20 - 0.39",
            "1": "< 0.20"
        },
        "translation_threshold": {
            "similarity_required_for_integrity": Config.TRANSLATION_THRESHOLD
        },
        "principles": [
            "Citizen empowerment",
            "Political neutrality",
            "Explainable scoring",
            "No enforcement of content",
            "Human oversight via appeals",
            "Privacy protection with PII redaction"
        ],
        "registry_data_source": {
            "table_name": Config.REGISTRY_TABLE,
            "table_status": registry_metadata.get("TableStatus") if registry_metadata else "unavailable",
            "item_count": registry_metadata.get("ItemCount") if registry_metadata else None,
            "global_secondary_indexes": [
                index.get("IndexName")
                for index in registry_metadata.get("GlobalSecondaryIndexes", [])
            ] if registry_metadata else [],
        }
    })
