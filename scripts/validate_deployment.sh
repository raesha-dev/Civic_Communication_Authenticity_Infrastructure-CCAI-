#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TF_DIR="${ROOT_DIR}/terraform"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

api_url="$(terraform -chdir="${TF_DIR}" output -raw api_gateway_invoke_url)"
aws_region="$(terraform -chdir="${TF_DIR}" output -raw aws_region)"
lambda_name="$(terraform -chdir="${TF_DIR}" output -raw lambda_function_name)"
registry_table="$(terraform -chdir="${TF_DIR}" output -raw institutional_registry_table_name)"
analysis_table="$(terraform -chdir="${TF_DIR}" output -raw analysis_results_table_name)"
config_bucket="$(terraform -chdir="${TF_DIR}" output -raw config_bucket_name)"
queue_url="$(terraform -chdir="${TF_DIR}" output -raw human_review_queue_url)"

sample_text="Official civic communication from CCAI. Verify your account status through the citizen portal only."

echo "Seeding registry baseline"
aws --region "${aws_region}" dynamodb put-item \
  --table-name "${registry_table}" \
  --item "{
    \"registry_id\": {\"S\": \"seed-ccai-official\"},
    \"entity_name\": {\"S\": \"ccai official\"},
    \"domain\": {\"S\": \"notifications.ccai.gov\"},
    \"entity_type\": {\"S\": \"hackathon\"},
    \"confidence\": {\"N\": \"0.99\"},
    \"reference_text\": {\"S\": \"${sample_text}\"}
  }" >/dev/null

echo "Checking API Gateway connectivity and live service health"
health_response="$(curl -fsS "${api_url}/health")"
methodology_response="$(curl -fsS "${api_url}/methodology")"
registry_response="$(curl -fsS "${api_url}/registry/search?domain=notifications.ccai.gov")"

python3 - "$health_response" "$methodology_response" "$registry_response" <<'PY'
import json
import sys

health = json.loads(sys.argv[1])
methodology = json.loads(sys.argv[2])
registry = json.loads(sys.argv[3])

assert health["status"] in {"online", "degraded"}
assert "services" in health
assert methodology["registry_data_source"]["table_name"]
assert registry["count"] >= 1
PY

echo "Running analysis request"
analyze_response="$(
  curl -fsS -X POST "${api_url}/analyze" \
    -H "Content-Type: application/json" \
    --data "{
      \"communication_text\": \"${sample_text}\",
      \"channel_type\": \"email\",
      \"metadata\": {
        \"domain\": \"notifications.ccai.gov\",
        \"entity_name\": \"CCAI Official\"
      }
    }"
)"

analysis_id="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["analysis_id"])' <<<"${analyze_response}")"
authenticity_score="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["authenticity_score"])' <<<"${analyze_response}")"

if [[ "${authenticity_score}" -lt 4 ]]; then
  echo "Expected authenticity score >= 4, got ${authenticity_score}" >&2
  exit 1
fi

echo "Checking persisted analysis and direct DynamoDB write"
curl -fsS "${api_url}/analyze/${analysis_id}" >/dev/null
aws --region "${aws_region}" dynamodb get-item \
  --table-name "${analysis_table}" \
  --key "{\"analysis_id\": {\"S\": \"${analysis_id}\"}}" >/dev/null

echo "Checking translation path, Bedrock embedding path, and Comprehend path"
translate_response="$(
  curl -fsS -X POST "${api_url}/translate" \
    -H "Content-Type: application/json" \
    --data "{
      \"analysis_id\": \"${analysis_id}\",
      \"original_text\": \"${sample_text}\",
      \"target_lang\": \"hi\"
    }"
)"

python3 - "$translate_response" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
assert payload["translation_id"]
assert payload["translated_text"]
PY

echo "Checking appeals workflow and SQS"
appeal_response="$(
  curl -fsS -X POST "${api_url}/appeals" \
    -H "Content-Type: application/json" \
    --data "{
      \"analysis_id\": \"${analysis_id}\",
      \"reason\": \"Official message came from the expected verified sender domain.\",
      \"contact_email\": \"official@notifications.ccai.gov\"
    }"
)"

python3 - "$appeal_response" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
assert payload["appeal_id"]
assert payload["status"] == "PENDING"
PY

message_id="$(aws --region "${aws_region}" sqs send-message --queue-url "${queue_url}" --message-body "validation" --query 'MessageId' --output text)"
receipt_handle="$(aws --region "${aws_region}" sqs receive-message --queue-url "${queue_url}" --max-number-of-messages 1 --wait-time-seconds 1 --query 'Messages[0].ReceiptHandle' --output text)"
if [[ "${receipt_handle}" != "None" ]]; then
  aws --region "${aws_region}" sqs delete-message --queue-url "${queue_url}" --receipt-handle "${receipt_handle}" >/dev/null
fi

echo "Checking S3 access"
printf '{"status":"ok"}' > "${TMP_DIR}/smoke.json"
aws --region "${aws_region}" s3api put-object --bucket "${config_bucket}" --key "smoke-tests/smoke.json" --body "${TMP_DIR}/smoke.json" >/dev/null
aws --region "${aws_region}" s3api head-object --bucket "${config_bucket}" --key "smoke-tests/smoke.json" >/dev/null
aws --region "${aws_region}" s3api delete-object --bucket "${config_bucket}" --key "smoke-tests/smoke.json" >/dev/null

echo "Checking direct Lambda invoke"
cat > "${TMP_DIR}/lambda_event.json" <<JSON
{
  "path": "/health",
  "httpMethod": "GET",
  "headers": {},
  "queryStringParameters": {},
  "requestContext": {
    "http": {
      "method": "GET",
      "path": "/health",
      "sourceIp": "127.0.0.1"
    }
  },
  "body": null,
  "isBase64Encoded": false
}
JSON

aws --region "${aws_region}" lambda invoke \
  --function-name "${lambda_name}" \
  --payload "fileb://${TMP_DIR}/lambda_event.json" \
  "${TMP_DIR}/lambda_response.json" >/dev/null

python3 - "${TMP_DIR}/lambda_response.json" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    payload = json.load(handle)

assert payload["statusCode"] == 200
PY

echo "Validation complete"
echo "API URL: ${api_url}"
echo "Lambda message id check: ${message_id}"
