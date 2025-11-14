"""Developer entrypoint helpers for running the JVP (IAMJVP) agent locally."""

from __future__ import annotations

import argparse

import uvicorn

from jvp_agent import build_a2a_agent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the IAMJVP commander locally.")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Bind host for the dev server."
    )
    parser.add_argument(
        "--port", default=8080, type=int, help="Port for the dev server."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agent = build_a2a_agent()
    uvicorn.run(agent.app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
