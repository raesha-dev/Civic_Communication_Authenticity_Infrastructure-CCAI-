try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
except ModuleNotFoundError:
    class _NoOpLimiter:
        def init_app(self, app):
            return app

        def limit(self, _value):
            def decorator(func):
                return func
            return decorator

    limiter = _NoOpLimiter()
