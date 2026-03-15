data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "ccai_lambda_role" {
  name               = "${var.project_name}-${var.environment}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "ccai_lambda_policy" {
  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      aws_cloudwatch_log_group.ccai_backend_logs.arn,
      "${aws_cloudwatch_log_group.ccai_backend_logs.arn}:*",
    ]
  }

  statement {
    sid    = "DynamoDBAccess"
    effect = "Allow"
    actions = [
      "dynamodb:DescribeTable",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:UpdateItem",
    ]
    resources = [
      aws_dynamodb_table.institutional_registry.arn,
      aws_dynamodb_table.analysis_results.arn,
      aws_dynamodb_table.appeals.arn,
      aws_dynamodb_table.audit_logs.arn,
      aws_dynamodb_table.translations.arn,
      "${aws_dynamodb_table.institutional_registry.arn}/index/*",
    ]
  }

  statement {
    sid    = "S3Access"
    effect = "Allow"
    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.ccai_corpus.arn,
      aws_s3_bucket.ccai_audit.arn,
      aws_s3_bucket.ccai_config.arn,
    ]
  }

  statement {
    sid    = "S3ObjectAccess"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = [
      "${aws_s3_bucket.ccai_corpus.arn}/*",
      "${aws_s3_bucket.ccai_audit.arn}/*",
      "${aws_s3_bucket.ccai_config.arn}/*",
    ]
  }

  statement {
    sid    = "QueueAccess"
    effect = "Allow"
    actions = [
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:GetQueueUrl",
      "sqs:ReceiveMessage",
      "sqs:SendMessage",
    ]
    resources = [aws_sqs_queue.human_review_queue.arn]
  }

  statement {
    sid       = "BedrockAccess"
    effect    = "Allow"
    actions   = ["bedrock:InvokeModel"]
    resources = ["*"]
  }

  statement {
    sid       = "ComprehendAccess"
    effect    = "Allow"
    actions   = ["comprehend:DetectPiiEntities"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "ccai_lambda_inline_policy" {
  name   = "${var.project_name}-${var.environment}-lambda-policy"
  role   = aws_iam_role.ccai_lambda_role.id
  policy = data.aws_iam_policy_document.ccai_lambda_policy.json
}
