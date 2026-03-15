locals {
  lambda_zip_abspath = abspath("${path.module}/${var.lambda_zip_path}")
}

resource "aws_cloudwatch_log_group" "ccai_backend_logs" {
  name              = "/aws/lambda/${var.project_name}-${var.environment}-backend"
  retention_in_days = var.lambda_log_retention_days
}

resource "aws_lambda_function" "ccai_backend" {
  function_name    = "${var.project_name}-${var.environment}-backend"
  role             = aws_iam_role.ccai_lambda_role.arn
  filename         = local.lambda_zip_abspath
  source_code_hash = filebase64sha256(local.lambda_zip_abspath)

  runtime       = var.lambda_runtime
  handler       = var.lambda_handler
  memory_size   = var.lambda_memory_size
  timeout       = var.lambda_timeout
  architectures = ["x86_64"]

  environment {
    variables = {
      AWS_REGION                 = var.aws_region
      MOCK_MODE                  = "false"
      ALLOW_MOCK_FALLBACK        = "true"
      REGISTRY_TABLE             = aws_dynamodb_table.institutional_registry.name
      ANALYSIS_RESULTS_TABLE     = aws_dynamodb_table.analysis_results.name
      APPEALS_TABLE              = aws_dynamodb_table.appeals.name
      AUDIT_LOGS_TABLE           = aws_dynamodb_table.audit_logs.name
      TRANSLATIONS_TABLE         = aws_dynamodb_table.translations.name
      REGISTRY_DOMAIN_INDEX_NAME = "domain-index"
      REGISTRY_ENTITY_INDEX_NAME = "entity-name-index"
      S3_BUCKET_EMBEDDINGS       = aws_s3_bucket.ccai_corpus.bucket
      S3_BUCKET_LOGS             = aws_s3_bucket.ccai_audit.bucket
      APPEALS_QUEUE_URL          = aws_sqs_queue.human_review_queue.id
      CORS_ALLOWED_ORIGINS       = var.allowed_cors_origin
      JWT_SECRET                 = var.jwt_secret
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.ccai_backend_logs,
    aws_iam_role_policy.ccai_lambda_inline_policy,
  ]
}
