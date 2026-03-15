variable "project_name" {
  type        = string
  description = "Project name used for tagging and resource naming."
  default     = "ccai"
}

variable "environment" {
  type        = string
  description = "Deployment environment name."
  default     = "hackathon"
}

variable "aws_region" {
  type        = string
  description = "AWS region for the deployment."
  default     = "us-east-1"
}

variable "lambda_zip_path" {
  type        = string
  description = "Relative path from terraform/ to the packaged Lambda zip."
  default     = "../lambda_package.zip"
}

variable "lambda_runtime" {
  type        = string
  description = "Lambda runtime."
  default     = "python3.11"
}

variable "lambda_handler" {
  type        = string
  description = "Lambda handler path."
  default     = "run.lambda_handler"
}

variable "lambda_memory_size" {
  type        = number
  description = "Lambda memory size in MB."
  default     = 512
}

variable "lambda_timeout" {
  type        = number
  description = "Lambda timeout in seconds."
  default     = 30
}

variable "lambda_log_retention_days" {
  type        = number
  description = "CloudWatch log retention period."
  default     = 7
}

variable "api_gateway_log_retention_days" {
  type        = number
  description = "CloudWatch log retention period for API Gateway access logs."
  default     = 14
}

variable "api_stage_name" {
  type        = string
  description = "API Gateway stage name."
  default     = "v1"
}

variable "allowed_cors_origin" {
  type        = string
  description = "Allowed origin for API Gateway CORS responses."
  default     = "*"
}

variable "registry_table_name" {
  type        = string
  description = "Institutional registry table name."
  default     = "InstitutionalRegistry"
}

variable "analysis_results_table_name" {
  type        = string
  description = "Analysis results table name."
  default     = "AnalysisResults"
}

variable "appeals_table_name" {
  type        = string
  description = "Appeals table name."
  default     = "Appeals"
}

variable "audit_logs_table_name" {
  type        = string
  description = "Audit log table name."
  default     = "AuditLogs"
}

variable "translations_table_name" {
  type        = string
  description = "Translations table name."
  default     = "Translations"
}

variable "sqs_queue_name" {
  type        = string
  description = "Human review queue name."
  default     = "ccai-human-review-queue"
}

variable "bucket_name_prefix" {
  type        = string
  description = "Prefix for globally unique S3 bucket names."
  default     = "ccai"
}

variable "jwt_secret" {
  type        = string
  description = "JWT/API auth secret for protected backend routes."
  sensitive   = true
  nullable    = false

  validation {
    condition     = length(var.jwt_secret) >= 16
    error_message = "jwt_secret must be at least 16 characters long."
  }
}
