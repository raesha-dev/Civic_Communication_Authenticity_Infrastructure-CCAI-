output "aws_region" {
  value = var.aws_region
}

output "api_gateway_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.ccai_api.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.ccai_api.stage_name}"
}

output "lambda_function_name" {
  value = aws_lambda_function.ccai_backend.function_name
}

output "institutional_registry_table_name" {
  value = aws_dynamodb_table.institutional_registry.name
}

output "analysis_results_table_name" {
  value = aws_dynamodb_table.analysis_results.name
}

output "appeals_table_name" {
  value = aws_dynamodb_table.appeals.name
}

output "audit_logs_table_name" {
  value = aws_dynamodb_table.audit_logs.name
}

output "translations_table_name" {
  value = aws_dynamodb_table.translations.name
}

output "corpus_bucket_name" {
  value = aws_s3_bucket.ccai_corpus.bucket
}

output "audit_bucket_name" {
  value = aws_s3_bucket.ccai_audit.bucket
}

output "config_bucket_name" {
  value = aws_s3_bucket.ccai_config.bucket
}

output "human_review_queue_url" {
  value = aws_sqs_queue.human_review_queue.id
}
