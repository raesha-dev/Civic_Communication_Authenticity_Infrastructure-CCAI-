from functools import wraps
from flask import request, jsonify
from app.config import Config

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != Config.JWT_SECRET and not Config.MOCK_MODE:
            # Simplified for MVP hackathon scope. Real implementation would use flask_jwt_extended
            return jsonify({
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Invalid or missing API key."
                }
            }), 401
        return f(*args, **kwargs)
    return decorated
