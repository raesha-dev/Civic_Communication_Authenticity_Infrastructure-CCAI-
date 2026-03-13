from flask import Blueprint, request, jsonify
from app.aws.dynamodb_client import query_registry
from app.utils.http import error_response

registry_bp = Blueprint('registry', __name__)

@registry_bp.route('/search', methods=['GET'])
def search_registry():
    entity_name = request.args.get('entity_name')
    domain = request.args.get('domain')
    entity_type = request.args.get('entity_type')
    
    if not entity_name and not domain and not entity_type:
        return error_response("BAD_REQUEST", "Must provide at least one search parameter (entity_name, domain, or entity_type)", 400)
        
    results = query_registry(entity_name, domain)
    
    if entity_type and results:
        results = [r for r in results if r.get('entity_type', '').lower() == entity_type.lower()]
        
    return jsonify({
        "results": results,
        "count": len(results)
    }), 200
