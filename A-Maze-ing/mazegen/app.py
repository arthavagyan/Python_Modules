"""Top-level orchestration for the A-Maze-ing terminal application."""

import sys
import time
from typing import Callable

from mazegen.config import MazeConfig
from mazegen.exporter import export_maze
from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.renderer import clear_screen, path_to_cell_sequence, render
from mazegen.solver import solve_astar, solve_bfs
from mazegen.utils import apply_42_pattern

_ANIMATION_DELAY_SECONDS = 0.03

_SOLVERS: dict[str, Callable[..., list[str]]] = {
    "BFS": solve_bfs,
    "ASTAR": solve_astar,
}


def build_maze(
    cfg: MazeConfig, seed: int | None
) -> tuple[MazeGenerator, list[str]]:
    """Generate a maze, solve it, and return the generator plus the path.

    Args:
        cfg: Validated maze configuration.
        seed: Seed to use for this specific generation.

    Returns:
        A tuple of (generator holding the built maze, shortest path).
    """
    generator = MazeGenerator(cfg.width, cfg.height, seed=seed)

    if not apply_42_pattern(generator.maze, cfg.entry, cfg.exit):
        print(
            "Warning: maze is too small to draw the '42' pattern, "
            "skipping it.",
            file=sys.stderr,
        )

    gen_on_step = _make_generation_callback(cfg) if cfg.animate else None

    if cfg.perfect:
        generator.generate_perfect(
            cfg.entry[0], cfg.entry[1], on_step=gen_on_step
        )
    else:
        generator.generate_playable(
            cfg.entry[0], cfg.entry[1],
            min_loops=cfg.min_loops, on_step=gen_on_step,
        )

    solve = _SOLVERS[cfg.algorithm]
    path = solve(generator.maze, cfg.entry, cfg.exit)

    if cfg.animate:
        _animate_path_reveal(cfg, generator, path)

    if not path:
        print(
            "Warning: no path found between entry and exit.",
            file=sys.stderr,
        )

    return generator, path


def _make_generation_callback(cfg: MazeConfig) -> Callable[[Maze], None]:
    """Build an on_step callback that redraws the maze after each wall
    removal."""
    def on_step(maze: Maze) -> None:
        clear_screen()
        print(render(maze, cfg.entry, cfg.exit))
        time.sleep(_ANIMATION_DELAY_SECONDS)

    return on_step


def _animate_path_reveal(
    cfg: MazeConfig, generator: MazeGenerator, path: list[str]
) -> None:
    """Animate the shortest path being drawn one cell at a time."""
    if not path:
        return
    sequence = path_to_cell_sequence(cfg.entry, path)
    for i in range(2, len(sequence) + 1):
        clear_screen()
        print(
            render(
                generator.maze, cfg.entry, cfg.exit, path=sequence[:i]
            )
        )
        time.sleep(_ANIMATION_DELAY_SECONDS)


def write_output(
    generator: MazeGenerator, cfg: MazeConfig, path: list[str]
) -> None:
    """Export the maze to cfg's output file."""
    try:
        export_maze(
            generator.maze,
            cfg.entry,
            cfg.exit,
            path,
            cfg.output_file,
        )
    except OSError as exc:
        print(
            f"Error: could not write output file "
            f"'{cfg.output_file}': {exc}",
            file=sys.stderr,
        )


def run(cfg: MazeConfig) -> None:
    """Build the initial maze, write it out, then run the interactive
    menu loop."""
    generator, path = build_maze(cfg, cfg.seed)
    write_output(generator, cfg, path)

    show_path = cfg.animate
    color_index = 0

    while True:
        sequence = (
            path_to_cell_sequence(cfg.entry, path) if show_path else None
        )
        if cfg.animate:
            clear_screen()
        print(render(
            generator.maze,
            cfg.entry,
            cfg.exit,
            sequence,
            color_index=color_index,
        ))
        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        try:
            choice = input("Choice? (1-4): ").strip()
        except EOFError:
            break

        if choice == "1":
            generator, path = build_maze(cfg, seed=None)
            write_output(generator, cfg, path)
            show_path = cfg.animate
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index += 1
        elif choice == "4":
            break
        else:
            print("Invalid choice, please pick 1-4.")
