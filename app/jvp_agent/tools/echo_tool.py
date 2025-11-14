"""Command echo tool for the JVP (IAMJVP) agent."""

from __future__ import annotations


def echo_command(command: str) -> dict[str, str]:
    """
    Return the command payload in a structured response.

    This placeholder demonstrates tool plumbing for future command routing.
    """
    return {
        "command": command,
        "note": (
            "Echo command executed. Replace with real command routing when ready."
        ),
    }
