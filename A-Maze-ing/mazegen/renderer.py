"""Unicode box-drawing terminal renderer for the maze.

Each grid intersection is drawn with the box-drawing character that
matches exactly which of the (up to four) wall segments touch it — a
stub, a straight line, a corner, a T, or a full cross — the same
technique as classic ASCII/Unicode maze art. The shortest path and the
entry/exit cells are overlaid as coloured markers on top of the line
art, so the corridor a player should follow stays visually distinct
from ordinary open space.
"""

import os

from mazegen.maze import Maze

_COLOR_PALETTE = [
    "\033[97m",  # white
    "\033[92m",  # green
    "\033[96m",  # cyan
    "\033[95m",  # pink
]
_RESET = "\033[0m"
_ENTRY_COLOR = "\033[33m"
_EXIT_COLOR = "\033[91m"
_PATH_COLOR = "\033[94m"

_DIRECTION_DELTAS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

Edge = tuple[str, int, int]
Coord = tuple[int, int]

# Box-drawing character for a wall junction, indexed by a 4-bit mask of
# which segments touch it: bit 0=North, 1=East, 2=South, 3=West. A
# junction with 0 or 1 active segments still needs a glyph (a stub end),
# 2 opposite segments needs a straight line, 2 adjacent needs a corner,
# 3 needs a T-piece, and 4 needs a full cross.
_JUNCTION_CHAR = {
    0b0000: " ",
    0b0001: "╵",  # stub up
    0b0010: "╶",  # stub right
    0b0011: "└",  # corner
    0b0100: "╷",  # stub down
    0b0101: "│",  # vertical line
    0b0110: "┌",  # corner
    0b0111: "├",  # T
    0b1000: "╴",  # stub left
    0b1001: "┘",  # corner
    0b1010: "─",  # horizontal line
    0b1011: "┴",  # T
    0b1100: "┐",  # corner
    0b1101: "┤",  # T
    0b1110: "┬",  # T
    0b1111: "┼",  # cross
}


def clear_screen() -> None:
    """Clear the terminal screen, used between animation frames."""
    os.system("cls" if os.name == "nt" else "clear")


def edge_between(a: Coord, b: Coord) -> Edge:
    """Identify the wall-gap segment crossed when moving from a to b.

    Args:
        a: (x, y) coordinates of the cell moved from.
        b: (x, y) coordinates of the neighbouring cell moved to.

    Returns:
        An ("h"|"v", x, y) tuple identifying the shared edge between the
        two cells, used to overlay the solved path onto the line art.
    """
    ax, ay = a
    bx, by = b
    if ay == by:  # horizontal move -> vertical wall-gap segment
        return ("v", max(ax, bx), ay)
    return ("h", ax, max(ay, by))  # vertical move -> horizontal segment


def path_to_cell_sequence(entry: Coord, path: list[str]) -> list[Coord]:
    """Convert a direction-letter path into the ordered sequence of cells
    it visits, from entry to exit (both included).

    Args:
        entry: Starting (x, y) coordinates.
        path: List of direction letters ("N", "E", "S", "W").

    Returns:
        Ordered list of (x, y) coordinates, entry first, exit last.
    """
    x, y = entry
    cells = [(x, y)]
    for letter in path:
        dx, dy = _DIRECTION_DELTAS[letter]
        x, y = x + dx, y + dy
        cells.append((x, y))
    return cells


def _build_corridor_overlay(
    sequence: list[Coord],
) -> tuple[set[Coord], set[Edge]]:
    """Compute the cells and wall-gap segments a cell sequence passes
    through, so it can be rendered as a continuous dotted corridor."""
    cells: set[Coord] = set(sequence)
    edges: set[Edge] = {
        edge_between(sequence[i], sequence[i + 1])
        for i in range(len(sequence) - 1)
    }
    return cells, edges


def _horiz_wall(maze: Maze, x: int, y: int) -> bool:
    """Whether there is a horizontal wall segment at column x, above
    row y (or below the last row, when y == maze.height)."""
    if y < maze.height:
        return maze.get_cell(x, y).north
    return maze.get_cell(x, maze.height - 1).south


def _vert_wall(maze: Maze, x: int, y: int) -> bool:
    """Whether there is a vertical wall segment at row y, left of
    column x (or right of the last column, when x == maze.width)."""
    if x < maze.width:
        return maze.get_cell(x, y).west
    return maze.get_cell(maze.width - 1, y).east


def _junction_glyph(maze: Maze, x: int, y: int) -> str:
    """Pick the box-drawing character for the grid intersection (x, y).

    Args:
        maze: The maze to render.
        x: Intersection column, 0..maze.width.
        y: Intersection row, 0..maze.height.

    Returns:
        A single Unicode box-drawing character.
    """
    mask = 0
    if y > 0 and _vert_wall(maze, x, y - 1):
        mask |= 0b0001  # North
    if x < maze.width and _horiz_wall(maze, x, y):
        mask |= 0b0010  # East
    if y < maze.height and _vert_wall(maze, x, y):
        mask |= 0b0100  # South
    if x > 0 and _horiz_wall(maze, x - 1, y):
        mask |= 0b1000  # West
    return _JUNCTION_CHAR[mask]


def render(
    maze: Maze,
    entry: Coord,
    exit_: Coord,
    path: list[Coord] | None = None,
    color_index: int = 0,
) -> str:
    """Render the maze as Unicode box-drawing line art.

    Args:
        maze: The maze to render.
        entry: (x, y) entry coordinates.
        exit_: (x, y) exit coordinates.
        path: Optional ordered sequence of (x, y) coordinates from entry to
            exit (inclusive): the final shortest path, once known.
        color_index: Index into the wall colour palette (wraps around).

    Returns:
        A multi-line string representing the maze, ready to print.
    """
    wall_color = _COLOR_PALETTE[color_index % len(_COLOR_PALETTE)]

    def colored_wall(glyph: str) -> str:
        return f"{wall_color}{glyph}{_RESET}" if glyph != " " else " "

    path_cells: set[Coord] = set()
    path_edges: set[Edge] = set()
    if path:
        path_cells, path_edges = _build_corridor_overlay(path)

    lines: list[str] = []
    for cy in range(maze.height + 1):
        top_row: list[str] = []
        for cx in range(maze.width + 1):
            top_row.append(colored_wall(_junction_glyph(maze, cx, cy)))
            if cx < maze.width:
                if _horiz_wall(maze, cx, cy):
                    top_row.append(colored_wall("─"))
                elif ("h", cx, cy) in path_edges:
                    top_row.append(f"{_PATH_COLOR}·{_RESET}")
                else:
                    top_row.append(" ")
        lines.append("".join(top_row))

        if cy < maze.height:
            mid_row: list[str] = []
            for cx in range(maze.width + 1):
                if _vert_wall(maze, cx, cy):
                    mid_row.append(colored_wall("│"))
                elif ("v", cx, cy) in path_edges:
                    mid_row.append(f"{_PATH_COLOR}·{_RESET}")
                else:
                    mid_row.append(" ")
                if cx < maze.width:
                    cell = (cx, cy)
                    if cell == entry:
                        mid_row.append(f"{_ENTRY_COLOR}S{_RESET}")
                    elif cell == exit_:
                        mid_row.append(f"{_EXIT_COLOR}X{_RESET}")
                    elif cell in path_cells:
                        mid_row.append(f"{_PATH_COLOR}·{_RESET}")
                    else:
                        mid_row.append(" ")
            lines.append("".join(mid_row))

    return "\n".join(lines)
