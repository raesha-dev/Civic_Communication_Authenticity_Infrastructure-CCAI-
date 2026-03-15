resource "aws_api_gateway_rest_api" "ccai_api" {
  name        = "${var.project_name}-${var.environment}-api"
  description = "REST API for the CCAI Flask Lambda backend"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_cloudwatch_log_group" "ccai_api_gateway_logs" {
  name              = "/aws/apigateway/${var.project_name}-${var.environment}-api"
  retention_in_days = var.api_gateway_log_retention_days
}

resource "aws_api_gateway_resource" "analyze" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "analyze"
}

resource "aws_api_gateway_resource" "analyze_id" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_resource.analyze.id
  path_part   = "{analysis_id}"
}

resource "aws_api_gateway_resource" "translate" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "translate"
}

resource "aws_api_gateway_resource" "appeals" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "appeals"
}

resource "aws_api_gateway_resource" "registry" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "registry"
}

resource "aws_api_gateway_resource" "registry_search" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_resource.registry.id
  path_part   = "search"
}

resource "aws_api_gateway_resource" "methodology" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "methodology"
}

resource "aws_api_gateway_resource" "health" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  parent_id   = aws_api_gateway_rest_api.ccai_api.root_resource_id
  path_part   = "health"
}

resource "aws_api_gateway_method" "post_analyze" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.analyze.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_analyze_id" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.analyze_id.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_translate" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.translate.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_appeals" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.appeals.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_registry_search" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.registry_search.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_methodology" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.methodology.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_health" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = aws_api_gateway_resource.health.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_analyze" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.analyze.id
  http_method             = aws_api_gateway_method.post_analyze.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "get_analyze_id" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.analyze_id.id
  http_method             = aws_api_gateway_method.get_analyze_id.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "post_translate" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.translate.id
  http_method             = aws_api_gateway_method.post_translate.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "post_appeals" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.appeals.id
  http_method             = aws_api_gateway_method.post_appeals.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "get_registry_search" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.registry_search.id
  http_method             = aws_api_gateway_method.get_registry_search.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "get_methodology" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.methodology.id
  http_method             = aws_api_gateway_method.get_methodology.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

resource "aws_api_gateway_integration" "get_health" {
  rest_api_id             = aws_api_gateway_rest_api.ccai_api.id
  resource_id             = aws_api_gateway_resource.health.id
  http_method             = aws_api_gateway_method.get_health.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ccai_backend.invoke_arn
}

locals {
  cors_resources = {
    analyze         = aws_api_gateway_resource.analyze.id
    analyze_id      = aws_api_gateway_resource.analyze_id.id
    translate       = aws_api_gateway_resource.translate.id
    appeals         = aws_api_gateway_resource.appeals.id
    registry_search = aws_api_gateway_resource.registry_search.id
    methodology     = aws_api_gateway_resource.methodology.id
    health          = aws_api_gateway_resource.health.id
  }
}

resource "aws_api_gateway_method" "cors" {
  for_each = local.cors_resources

  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  resource_id   = each.value
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "cors" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  resource_id = each.value
  http_method = aws_api_gateway_method.cors[each.key].http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "cors" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  resource_id = each.value
  http_method = aws_api_gateway_method.cors[each.key].http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "cors" {
  for_each = local.cors_resources

  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  resource_id = each.value
  http_method = aws_api_gateway_method.cors[each.key].http_method
  status_code = aws_api_gateway_method_response.cors[each.key].status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Request-Id'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'${var.allowed_cors_origin}'"
  }
}

resource "aws_api_gateway_gateway_response" "default_4xx" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  response_type = "DEFAULT_4XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'${var.allowed_cors_origin}'"
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Request-Id'"
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
  }
}

resource "aws_api_gateway_gateway_response" "default_5xx" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  response_type = "DEFAULT_5XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'${var.allowed_cors_origin}'"
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Request-Id'"
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
  }
}

resource "aws_lambda_permission" "allow_apigw_invoke" {
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ccai_backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ccai_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "ccai_api" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.analyze.id,
      aws_api_gateway_resource.analyze_id.id,
      aws_api_gateway_resource.translate.id,
      aws_api_gateway_resource.appeals.id,
      aws_api_gateway_resource.registry_search.id,
      aws_api_gateway_resource.methodology.id,
      aws_api_gateway_resource.health.id,
      aws_api_gateway_integration.post_analyze.id,
      aws_api_gateway_integration.get_analyze_id.id,
      aws_api_gateway_integration.post_translate.id,
      aws_api_gateway_integration.post_appeals.id,
      aws_api_gateway_integration.get_registry_search.id,
      aws_api_gateway_integration.get_methodology.id,
      aws_api_gateway_integration.get_health.id,
      values(aws_api_gateway_integration.cors)[*].id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.post_analyze,
    aws_api_gateway_integration.get_analyze_id,
    aws_api_gateway_integration.post_translate,
    aws_api_gateway_integration.post_appeals,
    aws_api_gateway_integration.get_registry_search,
    aws_api_gateway_integration.get_methodology,
    aws_api_gateway_integration.get_health,
    aws_api_gateway_integration_response.cors,
  ]
}

resource "aws_api_gateway_stage" "ccai_api" {
  rest_api_id   = aws_api_gateway_rest_api.ccai_api.id
  deployment_id = aws_api_gateway_deployment.ccai_api.id
  stage_name    = var.api_stage_name

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.ccai_api_gateway_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      responseLength = "$context.responseLength"
    })
  }

  xray_tracing_enabled = false
}

resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.ccai_api.id
  stage_name  = aws_api_gateway_stage.ccai_api.stage_name
  method_path = "*/*"

  settings {
    logging_level      = "ERROR"
    metrics_enabled    = true
    data_trace_enabled = false
  }
}
