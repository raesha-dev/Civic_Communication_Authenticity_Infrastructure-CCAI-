data "aws_kms_alias" "dynamodb" {
  name = "alias/aws/dynamodb"
}

resource "aws_dynamodb_table" "institutional_registry" {
  name         = var.registry_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "registry_id"

  attribute {
    name = "registry_id"
    type = "S"
  }

  attribute {
    name = "domain"
    type = "S"
  }

  attribute {
    name = "entity_name"
    type = "S"
  }

  global_secondary_index {
    name            = "domain-index"
    hash_key        = "domain"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "entity-name-index"
    hash_key        = "entity_name"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = data.aws_kms_alias.dynamodb.target_key_arn
  }
}

resource "aws_dynamodb_table" "analysis_results" {
  name         = var.analysis_results_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "analysis_id"

  attribute {
    name = "analysis_id"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = data.aws_kms_alias.dynamodb.target_key_arn
  }
}

resource "aws_dynamodb_table" "appeals" {
  name         = var.appeals_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "appeal_id"

  attribute {
    name = "appeal_id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = data.aws_kms_alias.dynamodb.target_key_arn
  }
}

resource "aws_dynamodb_table" "audit_logs" {
  name         = var.audit_logs_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "audit_id"

  attribute {
    name = "audit_id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = data.aws_kms_alias.dynamodb.target_key_arn
  }
}

resource "aws_dynamodb_table" "translations" {
  name         = var.translations_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "translation_id"

  attribute {
    name = "translation_id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = data.aws_kms_alias.dynamodb.target_key_arn
  }
}
