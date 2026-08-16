#!/usr/bin/env python3
"""A-Maze-ing: maze generator, solver, exporter, and terminal viewer.

Usage:
    python3 a_maze_ing.py config.txt
"""

import sys

from pydantic import ValidationError

from mazegen.app import run
from mazegen.config import ConfigError, load_config


def main() -> int:
    """Parse arguments, load the config, and run the application.

    Returns:
        Process exit code (0 on success, 1 on any handled error).
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        return 1

    config_path = sys.argv[1]

    try:
        cfg = load_config(config_path)
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(
            f"Error: invalid configuration in {config_path}:",
            file=sys.stderr,
        )
        print(exc, file=sys.stderr)
        return 1

    try:
        run(cfg)
    except KeyboardInterrupt:
        print("\nInterrupted, exiting.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error while running the maze: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
