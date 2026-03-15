from flask import Blueprint, request, jsonify
from app.models.translation_model import TranslationRequest, ValidationError
from app.services.translation_service import translate_verified_message
from app.aws.dynamodb_client import get_item
from app.utils.http import error_response

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/', methods=['POST'])
def translate_message():
    try:
        data = request.get_json()
        if not data:
            return error_response("BAD_REQUEST", "No JSON payload", 400)
            
        validated_data = TranslationRequest(**data)
        
        analysis = get_item('AnalysisResults', {'analysis_id': validated_data.analysis_id})
        
        if not analysis:
            return error_response("NOT_FOUND", "Analysis ID not found", 404)
            
        if float(analysis.get('authenticity_score', 0)) < 4.0:
            return error_response("SECURITY_ERROR", "Translation is only allowed for highly verified messages (score >= 4).", 403)
            
        result = translate_verified_message(
            original_text=validated_data.original_text,
            target_lang=validated_data.target_lang
        )
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", e.errors(), 400)
    except Exception as e:
        return error_response("SERVICE_ERROR", str(e), 500)
