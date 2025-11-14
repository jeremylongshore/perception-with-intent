#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "== Python formatting =="
if command -v black >/dev/null 2>&1; then
  black --check app scripts || exit 1
else
  echo "black not installed; skipping. // TODO(ask): enforce via tooling?"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff check app scripts
else
  echo "ruff not installed; skipping."
fi

echo
echo "== Terraform formatting =="
if command -v terraform >/dev/null 2>&1; then
  terraform -chdir=infra/terraform/envs/dev init -backend=false -input=false >/dev/null
  terraform -chdir=infra/terraform/envs/dev fmt -check
  terraform -chdir=infra/terraform/envs/dev validate -no-color
else
  echo "terraform not installed; skipping."
fi
