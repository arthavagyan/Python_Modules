"""Utility helpers for the A-Maze-ing project: the '42' pattern and the
cells a Pac-Man-style board must always keep open."""

from mazegen.maze import Maze

_GLYPH_4 = [
    "10001",
    "10001",
    "10001",
    "11111",
    "00001",
    "00001",
    "00001",
]
_GLYPH_2 = [
    "11111",
    "00001",
    "00001",
    "11111",
    "10000",
    "10000",
    "11111",
]

_DIGIT_W = len(_GLYPH_4[0])
_DIGIT_H = len(_GLYPH_4)
_GAP = 1
_TOTAL_W = _DIGIT_W * 2 + _GAP
_TOTAL_H = _DIGIT_H


def get_key_cells(width: int, height: int) -> set[tuple[int, int]]:
    """The four corners and the centre: must always stay open corridors."""
    return {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
        (width // 2, height // 2),
    }


def _pattern_cells_at(origin_x: int, origin_y: int) -> list[tuple[int, int]]:
    """The '42' pattern's reserved cells for this top-left origin."""
    cells: list[tuple[int, int]] = []

    for row_index, row in enumerate(_GLYPH_4):
        for col_index, char in enumerate(row):
            if char == "1":
                cells.append((origin_x + col_index, origin_y + row_index))

    offset_x = origin_x + _DIGIT_W + _GAP
    for row_index, row in enumerate(_GLYPH_2):
        for col_index, char in enumerate(row):
            if char == "1":
                cells.append((offset_x + col_index, origin_y + row_index))

    return cells


def get_42_pattern_cells(
    width: int,
    height: int,
    avoid: set[tuple[int, int]] | None = None,
) -> list[tuple[int, int]] | None:
    """Compute the (x, y) coordinates that must stay fully closed to draw
    '42', choosing a placement whose bounding box never touches a cell in
    avoid.

    Args:
        width: Maze width.
        height: Maze height.
        avoid: Cells the pattern must not overlap. Defaults to just the
            four corners and the centre.

    Returns:
        List of (x, y) coordinates, or None if the maze is too small to
        fit the pattern, or if every valid placement collides with an
        avoided cell.
    """
    if width < _TOTAL_W + 2 or height < _TOTAL_H + 2:
        return None

    if avoid is None:
        avoid = get_key_cells(width, height)

    max_x = width - _TOTAL_W - 1
    max_y = height - _TOTAL_H - 1
    centered_x = (width - _TOTAL_W) // 2
    centered_y = (height - _TOTAL_H) // 2

    candidates = sorted(
        (
            (ox, oy)
            for ox in range(1, max_x + 1)
            for oy in range(1, max_y + 1)
        ),
        key=lambda p: (p[0] - centered_x) ** 2 + (p[1] - centered_y) ** 2,
    )
    for origin_x, origin_y in candidates:
        cells = _pattern_cells_at(origin_x, origin_y)
        if not any(cell in avoid for cell in cells):
            return cells

    return None


def apply_42_pattern(
    maze: Maze,
    entry: tuple[int, int] | None = None,
    exit_: tuple[int, int] | None = None,
) -> bool:
    """Reserve the '42' pattern cells so the generator leaves them fully
    closed and unreachable.

    Args:
        maze: The (empty, freshly built) maze to apply the pattern to.
        entry: Optional (x, y) entry coordinates to keep clear.
        exit_: Optional (x, y) exit coordinates to keep clear.

    Returns:
        True if the pattern was applied, False if the maze is too small
        or no placement avoids the cells that must stay open.
    """
    avoid = get_key_cells(maze.width, maze.height)
    if entry is not None:
        avoid.add(entry)
    if exit_ is not None:
        avoid.add(exit_)

    cells = get_42_pattern_cells(maze.width, maze.height, avoid)
    if cells is None:
        return False

    for x, y in cells:
        cell = maze.get_cell(x, y)
        cell.is_visited = True
        cell.reserved = True

    return True
