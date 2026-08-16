"""BFS and A* pathfinding for the A-Maze-ing project."""

import heapq
import itertools
from collections import deque
from typing import Callable

from mazegen.cell import Cell
from mazegen.maze import Maze

_DIRS: list[tuple[str, int, int, str]] = [
    ("N", 0, -1, "north"),
    ("E", 1, 0, "east"),
    ("S", 0, 1, "south"),
    ("W", -1, 0, "west"),
]


def _open_neighbors(maze: Maze, current: Cell) -> list[tuple[str, Cell]]:
    """(direction letter, neighbor) pairs reachable through open walls."""
    result: list[tuple[str, Cell]] = []
    for letter, dx, dy, wall_attr in _DIRS:
        if getattr(current, wall_attr):
            continue
        nx, ny = current.x + dx, current.y + dy
        if not maze.is_inside_the_maze(nx, ny):
            continue
        result.append((letter, maze.get_cell(nx, ny)))
    return result


def _rebuild_path(
    came_from: dict[Cell, tuple[Cell, str]], goal: Cell, start: Cell
) -> list[str]:
    """Walk came_from backward from goal to start, returning the
    direction letters in forward order."""
    if goal not in came_from and goal is not start:
        return []
    path: list[str] = []
    cell = goal
    while cell in came_from:
        prev, letter = came_from[cell]
        path.append(letter)
        cell = prev
    path.reverse()
    return path


def solve_bfs(
    maze: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    on_step: Callable[[Cell], None] | None = None,
) -> list[str]:
    """Shortest path via breadth-first search.

    Args:
        maze: The maze to solve.
        entry: Entry coordinates.
        exit_: Exit coordinates.
        on_step: Optional callback invoked for each visited cell.

    Returns:
        Shortest path as a list of direction letters.
    """
    start = maze.get_cell(*entry)
    goal = maze.get_cell(*exit_)

    queue: deque[Cell] = deque([start])
    visited: set[Cell] = {start}
    came_from: dict[Cell, tuple[Cell, str]] = {}

    while queue:
        current = queue.popleft()
        if current is goal:
            break

        for letter, neighbor in _open_neighbors(maze, current):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            came_from[neighbor] = (current, letter)
            queue.append(neighbor)
            if on_step is not None:
                on_step(neighbor)

    return _rebuild_path(came_from, goal, start)


def solve_astar(
    maze: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    on_step: Callable[[Cell], None] | None = None,
) -> list[str]:
    """Shortest path via A* with the Manhattan-distance heuristic.

    Args:
        maze: The maze to solve.
        entry: Entry coordinates.
        exit_: Exit coordinates.
        on_step: Optional callback invoked for each visited cell.

    Returns:
        Shortest path as a list of direction letters.
    """
    start = maze.get_cell(*entry)
    goal = maze.get_cell(*exit_)

    def heuristic(cell: Cell) -> int:
        return abs(cell.x - goal.x) + abs(cell.y - goal.y)

    counter = itertools.count()
    frontier: list[tuple[int, int, Cell]] = [
        (heuristic(start), next(counter), start)
    ]
    cost_so_far: dict[Cell, int] = {start: 0}
    came_from: dict[Cell, tuple[Cell, str]] = {}
    visited: set[Cell] = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        if on_step is not None:
            on_step(current)
        if current is goal:
            break

        for letter, neighbor in _open_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = (current, letter)
                priority = new_cost + heuristic(neighbor)
                heapq.heappush(frontier, (priority, next(counter), neighbor))

    return _rebuild_path(came_from, goal, start)
