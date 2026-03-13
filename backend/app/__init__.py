import json
import logging
import time
from flask import Flask, g, request
from flask_cors import CORS
from flask_compress import Compress
from app.config import Config
from app.security.rate_limit import limiter
from app.utils.http import error_response


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    CORS(app, resources={r"/*": {"origins": "*"}})
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
        return response

    @app.errorhandler(429)
    def ratelimit_handler(_error):
        return error_response("RATE_LIMIT_EXCEEDED", "Too many requests. Please try again later.", 429)

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
