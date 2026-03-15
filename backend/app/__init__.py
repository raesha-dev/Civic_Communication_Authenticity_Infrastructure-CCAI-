import json
import logging
import time
from flask import Flask, g, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from app.config import Config
from app.security.rate_limit import limiter
from app.utils.http import error_response

try:
    from flask_cors import CORS
except ModuleNotFoundError:
    def CORS(_app, **_kwargs):
        return None

try:
    from flask_compress import Compress
except ModuleNotFoundError:
    class Compress:  # type: ignore[override]
        def __init__(self, app=None):
            if app is not None:
                self.init_app(app)

        def init_app(self, app):
            return app


def _cors_origin_for_request():
    allowed_origins = Config.CORS_ALLOWED_ORIGINS
    request_origin = request.headers.get("Origin")
    if "*" in allowed_origins:
        return "*"
    if request_origin and request_origin in allowed_origins:
        return request_origin
    return allowed_origins[0] if allowed_origins else "*"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_REQUEST_BYTES
    app.url_map.strict_slashes = False

    CORS(app, resources={r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}})
    Compress(app)
    limiter.init_app(app)

    from app.routes.analyze import analyze_bp
    from app.routes.translate import translate_bp
    from app.routes.appeals import appeals_bp
    from app.routes.registry import registry_bp
    from app.routes.methodology import methodology_bp
    from app.routes.health import health_bp

    app.register_blueprint(analyze_bp, url_prefix="/analyze")
    app.register_blueprint(translate_bp, url_prefix="/translate")
    app.register_blueprint(appeals_bp, url_prefix="/appeals")
    app.register_blueprint(registry_bp, url_prefix="/registry")
    app.register_blueprint(methodology_bp, url_prefix="/methodology")
    app.register_blueprint(health_bp, url_prefix="/health")

    logger = logging.getLogger(__name__)

    @app.before_request
    def before_request():
        g.request_started_at = time.perf_counter()

    @app.after_request
    def after_request(response):
        started_at = getattr(g, "request_started_at", time.perf_counter())
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info(json.dumps({
            "event": "api_request",
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "latency_ms": duration_ms,
            "request_id": request.headers.get("X-Request-Id"),
        }))
        response.headers["Cache-Control"] = "no-store"
        response.headers.setdefault("Access-Control-Allow-Origin", _cors_origin_for_request())
        response.headers.setdefault("Vary", "Origin")
        response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Request-Id")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

    @app.errorhandler(429)
    def ratelimit_handler(_error):
        return error_response("RATE_LIMIT_EXCEEDED", "Too many requests. Please try again later.", 429)

    @app.errorhandler(BadRequest)
    def bad_request(_error):
        return error_response("BAD_REQUEST", "Malformed or invalid request payload", 400)

    @app.errorhandler(RequestEntityTooLarge)
    def request_too_large(_error):
        return error_response("PAYLOAD_TOO_LARGE", "Request payload exceeds the allowed size", 413)

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("NOT_FOUND", "Endpoint not found", 404)

    @app.errorhandler(500)
    def server_error(_error):
        return error_response("INTERNAL_SERVER_ERROR", "An internal error occurred", 500)

    @app.errorhandler(Exception)
    def unhandled_error(_error):
        logger.exception("Unhandled application error")
        return error_response("SERVICE_ERROR", "Unexpected backend failure", 500)

    return app
