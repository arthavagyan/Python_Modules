"""Writes a Maze to the hexadecimal output file format."""

from mazegen.cell import Cell
from mazegen.maze import Maze


def _cell_hex_digit(cell: Cell) -> str:
    """Return the hexadecimal representation of a maze cell."""
    cell_hex_value = 0
    if cell.north:
        cell_hex_value |= 1
    if cell.east:
        cell_hex_value |= 2
    if cell.south:
        cell_hex_value |= 4
    if cell.west:
        cell_hex_value |= 8
    return format(cell_hex_value, "x")


def export_maze(
    maze: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[str],
    output_file: str,
) -> None:
    """Export a maze, its entry, exit, and solution path to a file.

    Args:
        maze: The generated maze.
        entry: Entry coordinates.
        exit_: Exit coordinates.
        path: Shortest path as direction letters.
        output_file: Destination file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for y in range(maze.height):
            maze_row = "".join(
                _cell_hex_digit(maze.get_cell(x, y)) for x in range(maze.width)
            )
            f.write(maze_row + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write("".join(path) + "\n")
