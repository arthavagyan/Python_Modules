"""mazegen: reusable maze generation and solving library."""

from mazegen.cell import Cell
from mazegen.config import ConfigError, MazeConfig, load_config
from mazegen.exporter import export_maze
from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.solver import solve_astar, solve_bfs
from mazegen.utils import apply_42_pattern, get_42_pattern_cells

__all__ = [
    "Cell",
    "Maze",
    "MazeGenerator",
    "MazeConfig",
    "ConfigError",
    "load_config",
    "export_maze",
    "solve_bfs",
    "solve_astar",
    "apply_42_pattern",
    "get_42_pattern_cells",
]

__version__ = "1.0.0"
