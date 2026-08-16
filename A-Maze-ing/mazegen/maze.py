"""Maze grid data structure, with neighbor, wall, and bounds helpers."""

from mazegen.cell import Cell


class Maze:
    """Grid of cells, with helpers for neighbors, walls, and bounds."""

    def __init__(self, width: int, height: int) -> None:
        """Build a width x height grid, every cell fully walled.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        self.width: int = width
        self.height: int = height

        self.grid: list[list[Cell]] = []

        for h in range(self.height):
            grid_row: list[Cell] = []
            for w in range(self.width):
                grid_row.append(Cell(w, h))
            self.grid.append(grid_row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The cell at that position.

        Raises:
            ValueError: If (x, y) is outside the maze.
        """
        if not self.is_inside_the_maze(x, y):
            raise ValueError(f"Coordinates ({x}, {y}) are outside the maze.")
        return self.grid[y][x]

    def is_inside_the_maze(self, x: int, y: int) -> bool:
        """Whether (x, y) falls within the maze bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Return cell's in-bounds neighbors, regardless of walls."""
        neighbors: list[Cell] = []

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for delta_x, delta_y in directions:
            x_new = cell.x + delta_x
            y_new = cell.y + delta_y

            if self.is_inside_the_maze(x_new, y_new):
                neighbors.append(self.get_cell(x_new, y_new))

        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        """Return cell's in-bounds neighbors that aren't visited yet."""
        return [n for n in self.get_neighbors(cell) if not n.is_visited]

    def remove_wall(self, current: Cell, neighbor: Cell) -> None:
        """Open the shared wall between two adjacent cells.

        Args:
            current: The cell to open a wall from.
            neighbor: The adjacent cell to open a wall to.

        Raises:
            ValueError: If the cells aren't adjacent.
        """
        delta_x = neighbor.x - current.x
        delta_y = neighbor.y - current.y

        if (delta_x, delta_y) == (0, -1):
            current.north = neighbor.south = False
        elif (delta_x, delta_y) == (1, 0):
            current.east = neighbor.west = False
        elif (delta_x, delta_y) == (0, 1):
            current.south = neighbor.north = False
        elif (delta_x, delta_y) == (-1, 0):
            current.west = neighbor.east = False
        else:
            raise ValueError(
                    f"Cells ({current.x},{current.y}) and "
                    f"({neighbor.x},{neighbor.y}) aren't neighbors."
                )

    def has_wall_between(self, a: Cell, b: Cell) -> bool:
        """Whether the wall between two adjacent cells is closed.

        Raises:
            ValueError: If the cells aren't adjacent.
        """
        delta_x = b.x - a.x
        delta_y = b.y - a.y

        if (delta_x, delta_y) == (0, -1):
            return a.north
        if (delta_x, delta_y) == (1, 0):
            return a.east
        if (delta_x, delta_y) == (0, 1):
            return a.south
        if (delta_x, delta_y) == (-1, 0):
            return a.west
        raise ValueError(
            f"Cells ({a.x},{a.y}) and ({b.x},{b.y}) aren't neighbors."
        )
