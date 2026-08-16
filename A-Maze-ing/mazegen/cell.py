"""Maze cell representation for the A-Maze-ing project."""


class Cell:
    """A single maze cell with coordinates and four wall flags."""

    def __init__(self, x_coord: int, y_coord: int) -> None:
        """Create a cell with all four walls closed.

        Args:
            x_coord: Column index of the cell.
            y_coord: Row index of the cell.
        """
        self.x: int = x_coord
        self.y: int = y_coord
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.is_visited: bool = False
        self.reserved: bool = False
