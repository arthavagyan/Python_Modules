"""Configuration file parsing and validation for A-Maze-ing.

Reads the plain KEY=VALUE file by hand (line numbers, comments, syntax
errors are simple enough to check directly), then hands the resulting raw
string dict to a Pydantic model for schema validation: required fields,
type coercion, and range/consistency checks all come from one declarative
model instead of a long chain of hand-written checks.
"""

import random
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

_MAX_WIDTH = 40
_MAX_HEIGHT = 25
_ALGORITHMS = {"BFS", "ASTAR"}
_REQUIRED_KEYS = {"width", "height", "entry", "exit", "output_file", "perfect"}


class ConfigError(Exception):
    """Raised when the configuration file is missing, unreadable, or has
    a syntax error (missing '=', missing required key). Schema-level
    problems (bad types, out-of-bounds values, ...) surface instead as a
    ``pydantic.ValidationError`` straight out of ``MazeConfig``, so callers
    should catch both."""


class MazeConfig(BaseModel):
    """Validated maze configuration, as returned by load_config."""

    width: int = Field(..., gt=0, le=_MAX_WIDTH)
    height: int = Field(..., gt=0, le=_MAX_HEIGHT)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(..., min_length=1)
    perfect: bool
    seed: int | None = None
    algorithm: str = "BFS"
    min_loops: int = Field(2, ge=1)
    animate: bool = False

    model_config = {"extra": "ignore"}

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def _parse_coordinates(
        cls, value: str | tuple[int, int]
    ) -> tuple[int, int]:
        """Parse an 'x,y' string into an (int, int) tuple.

        Args:
            value: A string in the format 'x,y', or an already-parsed
                tuple (accepted as-is, e.g. when building a MazeConfig
                directly from Python rather than from a config file).

        Returns:
            A tuple of two integers (x, y).
        """
        if isinstance(value, tuple):
            return value
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError(f"coordinates must be 'x,y' (got: {value!r})")
        try:
            return (int(parts[0].strip()), int(parts[1].strip()))
        except ValueError as exc:
            raise ValueError(
                f"coordinates must be integers (got: {value!r})"
            ) from exc

    @field_validator("algorithm", mode="before")
    @classmethod
    def _normalize_algorithm(cls, value: str) -> str:
        """Upper-case and validate the solving algorithm name."""
        normalized = str(value).strip().upper()
        if normalized not in _ALGORITHMS:
            raise ValueError(
                f"ALGORITHM must be one of {sorted(_ALGORITHMS)} "
                f"(got: {value!r})"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_bounds(self) -> "MazeConfig":
        """Cross-field checks that need more than one field at a time."""
        for name in ("entry", "exit"):
            x, y = getattr(self, name)
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(
                    f"{name.upper()} ({x},{y}) is outside the maze "
                    f"bounds ({self.width}x{self.height})"
                )
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different cells")
        return self


def _parse_lines(path: str) -> dict[str, str]:
    """Read KEY=VALUE lines from a config file into a dict.

    Args:
        path: Path to the configuration file.

    Returns:
        Raw (unparsed) string values, keyed by lower-cased key. Blank
        lines and lines starting with '#' are skipped.

    Raises:
        ConfigError: If the file can't be read, or a line is malformed.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigError(f"Configuration file not found: {path}")

    raw: dict[str, str] = {}
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    raise ConfigError(
                        f"{path}:{line_number}: invalid line "
                        f"{stripped!r} (expected KEY=VALUE)"
                    )
                key, _, value = stripped.partition("=")
                raw[key.strip().lower()] = value.strip()
    except OSError as exc:
        raise ConfigError(
            f"Could not read configuration file {path}: {exc}"
        ) from exc
    return raw


def load_config(path: str) -> MazeConfig:
    """Read and validate a maze configuration file.

    Args:
        path: Path to the configuration file.

    Returns:
        A validated MazeConfig.

    Raises:
        ConfigError: If the file is missing, unreadable, or a required
            key is absent.
        pydantic.ValidationError: If a present value fails schema
            validation (wrong type, out of range, inconsistent, ...).
    """
    raw = _parse_lines(path)

    missing = _REQUIRED_KEYS - raw.keys()
    if missing:
        raise ConfigError(
            f"Missing required key(s): "
            f"{', '.join(sorted(k.upper() for k in missing))}"
        )

    if "seed" not in raw:
        generated_seed = random.randint(0, 999_999)
        print(
            f"No SEED given, using generated seed: {generated_seed}",
            flush=True,
        )
        raw["seed"] = str(generated_seed)

    return MazeConfig.model_validate(raw)
