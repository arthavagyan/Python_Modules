"""Tests for maze generation, solving, and configuration validation."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from mazegen.cell import Cell
from mazegen.config import ConfigError, load_config
from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.solver import solve_astar, solve_bfs
from mazegen.utils import get_42_pattern_cells, get_key_cells


def _count_edges_and_nodes(maze: Maze) -> tuple[int, int]:
    """Count open connections and non-reserved cells."""
    nodes = sum(1 for row in maze.grid for c in row if not c.reserved)
    edges = 0
    for row in maze.grid:
        for cell in row:
            if cell.reserved:
                continue
            if not cell.east and maze.is_inside_the_maze(cell.x + 1, cell.y):
                neighbor = maze.get_cell(cell.x + 1, cell.y)
                if not neighbor.reserved:
                    edges += 1
            if not cell.south and maze.is_inside_the_maze(cell.x, cell.y + 1):
                neighbor = maze.get_cell(cell.x, cell.y + 1)
                if not neighbor.reserved:
                    edges += 1
    return edges, nodes


def _has_fully_open_3x3(maze: Maze) -> bool:
    """Whether any 3x3 block of cells has every internal wall open."""
    for top in range(maze.height - 2):
        for left in range(maze.width - 2):
            block = [
                maze.get_cell(x, y)
                for y in range(top, top + 3)
                for x in range(left, left + 3)
            ]
            if any(c.reserved for c in block):
                continue
            fully_open = True
            for y in range(top, top + 3):
                for x in range(left, left + 3):
                    cell = maze.get_cell(x, y)
                    if x + 1 < left + 3 and cell.east:
                        fully_open = False
                    if y + 1 < top + 3 and cell.south:
                        fully_open = False
            if fully_open:
                return True
    return False


def test_perfect_maze_is_a_spanning_tree() -> None:
    generator = MazeGenerator(width=12, height=10, seed=1)
    generator.generate_perfect(0, 0)

    edges, nodes = _count_edges_and_nodes(generator.maze)
    assert edges == nodes - 1


@pytest.mark.parametrize("seed", [1, 2, 3, 42])
def test_playable_maze_has_no_3x3_open_area(seed: int) -> None:
    generator = MazeGenerator(width=15, height=12, seed=seed)
    generator.generate_playable(0, 0, min_loops=2)

    assert not _has_fully_open_3x3(generator.maze)


def test_playable_maze_reaches_min_loops() -> None:
    generator = MazeGenerator(width=15, height=12, seed=7)
    generator.generate_playable(0, 0, min_loops=3)

    edges, nodes = _count_edges_and_nodes(generator.maze)
    loop_count = edges - nodes + 1
    assert loop_count >= 3


def test_playable_maze_key_cells_never_reserved() -> None:
    generator = MazeGenerator(width=15, height=12, seed=5)
    generator.generate_playable(0, 0, min_loops=2)

    for x, y in get_key_cells(15, 12):
        assert not generator.maze.get_cell(x, y).reserved


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_wall_coherence_between_neighbours(seed: int) -> None:
    generator = MazeGenerator(width=10, height=8, seed=seed)
    generator.generate_playable(0, 0, min_loops=2)
    maze = generator.maze

    for row in maze.grid:
        for cell in row:
            if maze.is_inside_the_maze(cell.x + 1, cell.y):
                neighbor = maze.get_cell(cell.x + 1, cell.y)
                assert cell.east == neighbor.west
            if maze.is_inside_the_maze(cell.x, cell.y + 1):
                neighbor = maze.get_cell(cell.x, cell.y + 1)
                assert cell.south == neighbor.north


@pytest.mark.parametrize("solve", [solve_bfs, solve_astar])
def test_solver_always_finds_a_path(solve: object) -> None:
    generator = MazeGenerator(width=12, height=10, seed=9)
    generator.generate_perfect(0, 0)

    path = solve(generator.maze, (0, 0), (11, 9))  # type: ignore[operator]
    assert path
    x, y = 0, 0
    deltas = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    for letter in path:
        dx, dy = deltas[letter]
        x, y = x + dx, y + dy
    assert (x, y) == (11, 9)


def test_42_pattern_never_overlaps_key_cells() -> None:
    width, height = 25, 15
    avoid = get_key_cells(width, height)
    cells = get_42_pattern_cells(width, height, avoid)

    assert cells is not None
    assert not (set(cells) & avoid)


def test_42_pattern_none_when_maze_too_small() -> None:
    assert get_42_pattern_cells(5, 5) is None


def test_load_config_missing_file() -> None:
    with pytest.raises(ConfigError):
        load_config("/nonexistent/path/config.txt")


def test_load_config_missing_required_key(tmp_path: Path) -> None:
    path = tmp_path / "config.txt"
    path.write_text("WIDTH=10\nHEIGHT=10\n")
    with pytest.raises(ConfigError):
        load_config(str(path))


def test_load_config_entry_out_of_bounds(tmp_path: Path) -> None:
    path = tmp_path / "config.txt"
    path.write_text(
        "WIDTH=10\nHEIGHT=10\nENTRY=99,0\nEXIT=1,1\n"
        "OUTPUT_FILE=maze.txt\nPERFECT=True\n"
    )
    with pytest.raises(ValidationError):
        load_config(str(path))


def test_load_config_width_over_subject_limit(tmp_path: Path) -> None:
    path = tmp_path / "config.txt"
    path.write_text(
        "WIDTH=41\nHEIGHT=10\nENTRY=0,0\nEXIT=1,1\n"
        "OUTPUT_FILE=maze.txt\nPERFECT=True\n"
    )
    with pytest.raises(ValidationError):
        load_config(str(path))


def test_load_config_valid_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "config.txt"
    path.write_text(
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=maze.txt\nPERFECT=True\nSEED=42\n"
    )
    cfg = load_config(str(path))
    assert cfg.width == 10
    assert cfg.entry == (0, 0)
    assert cfg.exit == (9, 9)
    assert cfg.perfect is True
    assert cfg.seed == 42


def test_cell_starts_fully_walled() -> None:
    cell = Cell(0, 0)
    assert cell.north and cell.east and cell.south and cell.west
