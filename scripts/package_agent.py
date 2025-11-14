#!/usr/bin/env python
"""
Package the IAMJVP agent for Vertex AI Agent Engine deployment.

This script produces the three artifacts expected by the Reasoning Engine
(`pickle.pkl`, `dependencies.tar.gz`, `requirements.txt`) in the `build/`
directory so Terraform or manual uploads can deploy the agent.
"""

from __future__ import annotations

import argparse
import importlib
import shutil
import tarfile
from pathlib import Path

import cloudpickle

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_IMPORT_PATH = "app.main:app"
BUILD_DIR = PROJECT_ROOT / "build"
PICKLE_PATH = BUILD_DIR / "pickle.pkl"
DEPS_TAR_PATH = BUILD_DIR / "dependencies.tar.gz"
REQUIREMENTS_PATH = BUILD_DIR / "requirements.txt"
APP_DIR = PROJECT_ROOT / "app"
ROOT_REQUIREMENTS = PROJECT_ROOT / "requirements.txt"


def _import_app(path: str):
    module_name, attr = path.split(":")
    module = importlib.import_module(module_name)
    try:
        return getattr(module, attr)
    except AttributeError as exc:
        raise SystemExit(f"Failed to load app object '{attr}' from '{module_name}': {exc}")


def serialize_app() -> None:
    app_obj = _import_app(APP_IMPORT_PATH)
    PICKLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PICKLE_PATH.open("wb") as fh:
        cloudpickle.dump(app_obj, fh)


def archive_dependencies() -> None:
    with tarfile.open(DEPS_TAR_PATH, "w:gz") as tar:
        tar.add(APP_DIR, arcname="app")


def copy_requirements() -> None:
    if not ROOT_REQUIREMENTS.exists():
        raise SystemExit("Repository requirements.txt not found; cannot package dependencies.")
    shutil.copy(ROOT_REQUIREMENTS, REQUIREMENTS_PATH)


def main() -> None:
    parser = argparse.ArgumentParser(description="Package IAMJVP agent for Vertex AI.")
    parser.add_argument(
        "--app",
        default=APP_IMPORT_PATH,
        help="Import path to the ADK App object (default: app.main:app).",
    )
    args = parser.parse_args()

    global APP_IMPORT_PATH  # type: ignore[global-statement]
    APP_IMPORT_PATH = args.app

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    serialize_app()
    archive_dependencies()
    copy_requirements()

    print("Artifacts written to build/:")
    for path in (PICKLE_PATH, DEPS_TAR_PATH, REQUIREMENTS_PATH):
        print(f"- {path.name}")


if __name__ == "__main__":
    main()
