#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/build"
ZIP_PATH="${ROOT_DIR}/lambda_package.zip"
HEALTHCHECK_URL="http://127.0.0.1:8099/health"

cd "${ROOT_DIR}"

rm -rf "${BUILD_DIR}" "${ZIP_PATH}"
mkdir -p "${BUILD_DIR}"

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.11 \
  --only-binary=:all: \
  --requirement backend/requirements.txt \
  --target "${BUILD_DIR}"

cp -R backend/app "${BUILD_DIR}/app"
cp backend/run.py "${BUILD_DIR}/run.py"

find "${BUILD_DIR}" -name "__pycache__" -type d -prune -exec rm -rf {} +

PYTHONPATH="${BUILD_DIR}" python3 -c "from run import app, lambda_handler; print(app.url_map)"

PYTHONPATH="${BUILD_DIR}" python3 -m gunicorn \
  --chdir "${BUILD_DIR}" \
  --bind 127.0.0.1:8099 \
  --workers 1 \
  --timeout 30 \
  --daemon \
  --pid "${BUILD_DIR}/gunicorn.pid" \
  run:app

sleep 3
curl -fsS "${HEALTHCHECK_URL}" >/dev/null
kill "$(cat "${BUILD_DIR}/gunicorn.pid")"
rm -f "${BUILD_DIR}/gunicorn.pid"

(
  cd "${BUILD_DIR}"
  zip -qr "${ZIP_PATH}" .
)

echo "Lambda package created at ${ZIP_PATH}"
