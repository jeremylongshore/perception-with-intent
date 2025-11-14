#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== IAMJVP Repo Sanity Check =="

required_paths=(
  "$ROOT_DIR/app/jvp_agent/agent.yaml"
  "$ROOT_DIR/app/jvp_agent/tools/echo_tool.py"
  "$ROOT_DIR/infra/terraform/envs/dev/main.tf"
  "$ROOT_DIR/scripts/dev_run_adk.sh"
  "$ROOT_DIR/scripts/fmt_vet_lint.sh"
  "$ROOT_DIR/.github/workflows/ci.yml"
)

missing=0
for path in "${required_paths[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "[MISSING] $path"
    missing=1
  fi
done

if [[ $missing -eq 0 ]]; then
  echo "All required files are present."
fi

echo
echo "== Top-level inventory =="
allowed_top_level=(
  ".git"
  ".github"
  ".gitignore"
  "000-docs"
  "000-usermanuals"
  "_archive"
  "AGENTS.md"
  "app"
  "infra"
  "scripts"
  "STATUS.md"
  "README.md"
  "docs"
  "LICENSE"
  "requirements.txt"
)

shopt -s dotglob nullglob
for entry in "$ROOT_DIR"/*; do
  name="$(basename "$entry")"
  if [[ " ${allowed_top_level[*]} " == *" $name "* ]]; then
    continue
  fi
  echo "[CHECK] Consider archiving top-level item: $name"
done

echo
echo "Review 000-docs/USER-MANUALS.md for next actions."
