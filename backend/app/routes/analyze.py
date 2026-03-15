from flask import Blueprint, request, jsonify
from app.models.analysis_model import AnalysisRequest, ValidationError
from app.services.analysis_service import analyze_communication
from app.aws.dynamodb_client import get_item
from app.security.rate_limit import limiter
from app.utils.http import error_response

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/', methods=['POST'])
@limiter.limit("50 per minute")
def create_analysis():
    try:
        data = request.get_json()
        if not data:
            return error_response("BAD_REQUEST", "No JSON payload", 400)
            
        validated_data = AnalysisRequest(**data)
        
        result = analyze_communication(
            text=validated_data.communication_text,
            channel_type=validated_data.channel_type,
            metadata=validated_data.metadata
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", e.errors(), 400)
    except Exception as e:
        return error_response("SERVICE_ERROR", str(e), 500)

@analyze_bp.route('/<analysis_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_analysis(analysis_id):
    result = get_item('AnalysisResults', {'analysis_id': analysis_id})
    if result:
        return jsonify(result), 200
    return error_response("NOT_FOUND", "Analysis ID not found", 404)
