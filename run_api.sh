#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=./src
export CONFIG_PATH="${CONFIG_PATH:-configs/evalops.yaml}"
uvicorn evalops_lab.api:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8098}" --reload
