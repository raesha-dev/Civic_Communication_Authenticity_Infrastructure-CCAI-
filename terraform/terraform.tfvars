project_name        = "ccai"
environment         = "hackathon"
aws_region          = "us-east-1"
api_stage_name      = "v1"
allowed_cors_origin = "*"
lambda_zip_path     = "../lambda_package.zip"
bucket_name_prefix  = "ccai"

# Provide the JWT secret securely at deploy time, for example:
# export TF_VAR_jwt_secret='replace-with-a-long-random-secret'
