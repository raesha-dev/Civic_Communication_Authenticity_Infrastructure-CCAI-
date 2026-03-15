locals {
  bucket_suffix      = "${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  corpus_bucket_name = "${var.bucket_name_prefix}-corpus-${local.bucket_suffix}"
  audit_bucket_name  = "${var.bucket_name_prefix}-audit-${local.bucket_suffix}"
  config_bucket_name = "${var.bucket_name_prefix}-config-${local.bucket_suffix}"
}

resource "aws_s3_bucket" "ccai_corpus" {
  bucket = local.corpus_bucket_name
}

resource "aws_s3_bucket" "ccai_audit" {
  bucket = local.audit_bucket_name
}

resource "aws_s3_bucket" "ccai_config" {
  bucket = local.config_bucket_name
}

resource "aws_s3_bucket_versioning" "ccai_corpus" {
  bucket = aws_s3_bucket.ccai_corpus.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "ccai_audit" {
  bucket = aws_s3_bucket.ccai_audit.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "ccai_config" {
  bucket = aws_s3_bucket.ccai_config.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ccai_corpus" {
  bucket = aws_s3_bucket.ccai_corpus.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ccai_audit" {
  bucket = aws_s3_bucket.ccai_audit.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ccai_config" {
  bucket = aws_s3_bucket.ccai_config.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "ccai_corpus" {
  bucket                  = aws_s3_bucket.ccai_corpus.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "ccai_audit" {
  bucket                  = aws_s3_bucket.ccai_audit.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "ccai_config" {
  bucket                  = aws_s3_bucket.ccai_config.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "ccai_corpus" {
  bucket = aws_s3_bucket.ccai_corpus.id

  rule {
    id     = "abort-incomplete-multipart-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ccai_audit" {
  bucket = aws_s3_bucket.ccai_audit.id

  rule {
    id     = "abort-incomplete-multipart-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ccai_config" {
  bucket = aws_s3_bucket.ccai_config.id

  rule {
    id     = "abort-incomplete-multipart-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
