import base64
import logging
from io import BytesIO
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Response
from app import create_app


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = create_app()


def _body_from_event(event):
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        return base64.b64decode(body)
    return body.encode("utf-8")


def lambda_handler(event, context):
    request_context = event.get("requestContext", {})
    http_context = request_context.get("http", {})
    headers = event.get("headers") or {}
    query = event.get("queryStringParameters") or {}
    method = http_context.get("method") or event.get("httpMethod", "GET")
    path = http_context.get("path") or event.get("path", "/")
    body = _body_from_event(event)

    builder = EnvironBuilder(
        path=path,
        method=method,
        headers=headers,
        query_string=query,
        data=body,
    )
    environ = builder.get_environ()
    environ["REMOTE_ADDR"] = http_context.get("sourceIp", "")
    environ["wsgi.input"] = BytesIO(body)

    response = Response.from_app(app, environ)
    payload = response.get_data()
    is_text = response.mimetype.startswith("text/") or response.mimetype == "application/json"

    return {
        "statusCode": response.status_code,
        "headers": dict(response.headers),
        "body": payload.decode("utf-8") if is_text else base64.b64encode(payload).decode("ascii"),
        "isBase64Encoded": not is_text,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
