resource "aws_sqs_queue" "human_review_queue" {
  name                       = var.sqs_queue_name
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600
  sqs_managed_sse_enabled    = true
}
