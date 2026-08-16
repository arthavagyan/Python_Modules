"""Maze generation algorithms for the A-Maze-ing project."""

import random
from typing import Callable

from mazegen.cell import Cell
from mazegen.maze import Maze

_LOOP_TOPUP_FACTOR = 2
_BRAID_PASSES = 3


class MazeGenerator:
    """Carves perfect and Pac-Man-style mazes into a Maze grid."""

    def __init__(
                self, width: int, height: int, seed: int | None = None
            ) -> None:
        """Create a generator with its own maze and seeded RNG.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            seed: Optional seed for reproducible generation.
        """
        self.maze: Maze = Maze(width, height)
        self.rng: random.Random = random.Random(seed)

    def generate_perfect(
        self,
        start_x: int,
        start_y: int,
        on_step: Callable[[Maze], None] | None = None,
    ) -> Maze:
        """Generate a perfect maze using an iterative DFS backtracker.

        Args:
            start_x: X coordinate to start carving from.
            start_y: Y coordinate to start carving from.
            on_step: Optional callback invoked after each wall removal.

        Returns:
            The generated maze.
        """
        start: Cell = self.maze.get_cell(start_x, start_y)
        stack: list[Cell] = [start]
        start.is_visited = True

        while stack:
            curr = stack[-1]
            curr_unvisited_neighbors = self.maze.get_unvisited_neighbors(curr)

            if curr_unvisited_neighbors:
                random_neighbor = self.rng.choice(curr_unvisited_neighbors)
                self.maze.remove_wall(curr, random_neighbor)
                random_neighbor.is_visited = True
                stack.append(random_neighbor)
                if on_step is not None:
                    on_step(self.maze)
            else:
                stack.pop()

        return self.maze

    def generate_playable(
        self,
        start_x: int,
        start_y: int,
        min_loops: int = 2,
        on_step: Callable[[Maze], None] | None = None,
    ) -> Maze:
        """Build a fully-connected, multi-route board with few dead-ends.

        Args:
            start_x: X coordinate to start carving from.
            start_y: Y coordinate to start carving from.
            min_loops: Minimum number of independent routes to guarantee.
            on_step: Optional callback for animating the initial carve.

        Returns:
            The generated maze.
        """
        self.generate_perfect(start_x, start_y, on_step=on_step)
        self._braid_dead_ends()
        self._ensure_min_loops(min_loops)
        return self.maze

    def _braid_dead_ends(self) -> None:
        """Open one extra wall for every real (non-reserved) dead-end."""
        for _ in range(_BRAID_PASSES):
            cells = [
                c for row in self.maze.grid for c in row
                if not c.reserved
            ]
            self.rng.shuffle(cells)
            for cell in cells:
                if self._open_passage_count(cell) != 1:
                    continue
                self._try_open_one_wall(cell)

    def _try_open_one_wall(self, cell: Cell) -> bool:
        """Try to open one more wall from cell, respecting all rules."""
        candidates = [
            n for n in self.maze.get_neighbors(cell)
            if not n.reserved and self.maze.has_wall_between(cell, n)
        ]
        self.rng.shuffle(candidates)
        for neighbor in candidates:
            if not self._would_create_3x3_opening(cell, neighbor):
                self.maze.remove_wall(cell, neighbor)
                return True
        return False

    def _ensure_min_loops(self, min_loops: int) -> None:
        """Add random connections until at least min_loops independent
        routes exist."""
        max_attempts = (
            max(self.maze.width, self.maze.height) * _LOOP_TOPUP_FACTOR * 20
        )
        attempts = 0
        while self._loop_count() < min_loops and attempts < max_attempts:
            attempts += 1
            x = self.rng.randrange(self.maze.width)
            y = self.rng.randrange(self.maze.height)
            current = self.maze.get_cell(x, y)
            if current.reserved:
                continue

            candidates = [
                n for n in self.maze.get_neighbors(current)
                if not n.reserved and self.maze.has_wall_between(current, n)
            ]
            if not candidates:
                continue

            neighbor = self.rng.choice(candidates)
            if not self._would_create_3x3_opening(current, neighbor):
                self.maze.remove_wall(current, neighbor)

    def _open_passage_count(self, cell: Cell) -> int:
        """Number of open walls (0-4) a cell currently has."""
        return sum(
            (not cell.north, not cell.east, not cell.south, not cell.west)
        )

    def _loop_count(self) -> int:
        """Independent cycles (edges - nodes + 1) over non-reserved
        cells."""
        nodes = sum(
            1 for row in self.maze.grid for c in row if not c.reserved
        )
        edges = 0
        for row in self.maze.grid:
            for cell in row:
                if cell.reserved:
                    continue
                if not cell.east:
                    east = self.maze.get_cell(cell.x + 1, cell.y) \
                        if self.maze.is_inside_the_maze(cell.x + 1, cell.y) \
                        else None
                    if east is not None and not east.reserved:
                        edges += 1
                if not cell.south:
                    south = self.maze.get_cell(cell.x, cell.y + 1) \
                        if self.maze.is_inside_the_maze(cell.x, cell.y + 1) \
                        else None
                    if south is not None and not south.reserved:
                        edges += 1
        return edges - nodes + 1 if nodes else 0

    def _is_2x2_open(self, top_left_x: int, top_left_y: int) -> bool:
        """Whether the 2x2 block with this top-left corner has every
        internal wall open."""
        if top_left_x < 0 or top_left_y < 0:
            return False
        if not self.maze.is_inside_the_maze(top_left_x + 1, top_left_y + 1):
            return False

        tl = self.maze.get_cell(top_left_x, top_left_y)
        tr = self.maze.get_cell(top_left_x + 1, top_left_y)
        bl = self.maze.get_cell(top_left_x, top_left_y + 1)
        br = self.maze.get_cell(top_left_x + 1, top_left_y + 1)

        return (not tl.east and not tl.south
                and not tr.south and not tr.west
                and not bl.east and not bl.north
                and not br.north and not br.west)

    def _is_3x3_open(self, top_left_x: int, top_left_y: int) -> bool:
        """Whether the 3x3 block with this top-left corner is fully
        open."""
        if top_left_x < 0 or top_left_y < 0:
            return False
        if not self.maze.is_inside_the_maze(top_left_x + 2, top_left_y + 2):
            return False
        return all(
            self._is_2x2_open(top_left_x + ox, top_left_y + oy)
            for ox in (0, 1) for oy in (0, 1)
        )

    def _would_create_3x3_opening(self, a: Cell, b: Cell) -> bool:
        """Tentatively open the wall between a and b and check whether any
        3x3 window touching either cell would become fully open."""
        dx, dy = b.x - a.x, b.y - a.y
        self.maze.remove_wall(a, b)

        creates_large = any(
            self._is_3x3_open(a.x + wx, a.y + wy)
            for wx in (-2, -1, 0) for wy in (-2, -1, 0)
        )

        self._restore_wall(a, b, dx, dy)
        return creates_large

    def _restore_wall(self, a: Cell, b: Cell, dx: int, dy: int) -> None:
        """Put the wall between a and b back up."""
        if (dx, dy) == (0, -1):
            a.north, b.south = True, True
        elif (dx, dy) == (1, 0):
            a.east, b.west = True, True
        elif (dx, dy) == (0, 1):
            a.south, b.north = True, True
        elif (dx, dy) == (-1, 0):
            a.west, b.east = True, True

    def add_loops(self, extra_connections: int) -> None:
        """Add up to extra_connections random loop connections.

        Args:
            extra_connections: Number of extra connections to add.
        """
        added = 0
        attempts = 0
        max_attempts = extra_connections * 20

        while added < extra_connections and attempts < max_attempts:
            attempts += 1

            x = self.rng.randrange(self.maze.width)
            y = self.rng.randrange(self.maze.height)
            current = self.maze.get_cell(x, y)
            if current.reserved:
                continue

            candidates = [
                n for n in self.maze.get_neighbors(current)
                if not n.reserved
                and self.maze.has_wall_between(current, n)
            ]
            if not candidates:
                continue

            neighbor = self.rng.choice(candidates)

            if self._would_create_3x3_opening(current, neighbor):
                continue

            self.maze.remove_wall(current, neighbor)
            added += 1
