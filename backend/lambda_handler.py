import base64
from io import BytesIO
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Response
from run import app


def _body_from_event(event):
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        return base64.b64decode(body)
    return body.encode("utf-8")


def handler(event, context):
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
