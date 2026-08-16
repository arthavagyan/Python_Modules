*This project has been created as part of the 42 curriculum by artavagy, grgrigor.*

# A-Maze-ing

## Description

A-Maze-ing generates, solves, displays, and exports a 2D maze from a
plain-text configuration file.

Two generation modes are available:

- **`PERFECT=True`** — a classic perfect maze: exactly one path between any
  two cells, no loops.
- **`PERFECT=False`** (default) — a Pac-Man-ready board instead: fully
  connected, corners and centre kept open, at least two independent
  routes between entry and exit, and dead-ends kept rare.

Both modes embed a visible **"42" pattern** made of cells that stay fully
walled off. Once a maze is built, it's solved with a shortest-path search,
rendered in the terminal, and exported to a hexadecimal text file.

The project has two parts:

- **`a_maze_ing.py`** — a thin CLI entry point: reads the config, calls into
  `mazegen`, writes the output file, runs the interactive viewer.
- **`mazegen/`** — the reusable package doing all the actual work
  (validation, generation, solving, rendering, exporting). It doesn't
  depend on the CLI at all and can be installed on its own in any other
  Python project.

## Instructions

Dependencies are managed with [Poetry](https://python-poetry.org/).

```bash
make install    # poetry install
make run         # poetry run python a_maze_ing.py config.txt
```

or directly, with any config file:

```bash
python3 a_maze_ing.py config.txt
```

Other useful targets:

```bash
make debug         # run under pdb
make lint           # flake8 + the exact mypy flags the subject requires
make lint-strict     # optional, mypy --strict
make test             # pytest suite
make build              # rebuild mazegen-*.whl / .tar.gz into the repo root
```

### Makefile targets

| Command | Description |
|---|---|
| `make install` | Install project dependencies via Poetry |
| `make run` | Run the application on `config.txt` |
| `make debug` | Run the application under `pdb` |
| `make lint` | `flake8 .` + `mypy .` with the required flags |
| `make lint-strict` | `flake8 .` + `mypy --strict` (optional) |
| `make test` | Run the pytest suite |
| `make build` | Build `mazegen-*.whl`/`.tar.gz` into the repo root |
| `make clean` | Remove caches and build artifacts |
| `make re` | `clean` then `install` |

## Resources

### Documentation

- [Python Standard Library docs](https://docs.python.org/3/library/) —
  `random.Random` for seeded generation, `heapq`/`collections.deque` for
  A*/BFS, `pathlib` for config handling.
- [Pydantic docs](https://docs.pydantic.dev/) — model/field validators,
  used throughout `mazegen/config.py`.
- [PEP 8](https://peps.python.org/pep-0008/) and
  [PEP 257](https://peps.python.org/pep-0257/) — style and docstring
  conventions followed across the codebase.
- [pytest docs](https://docs.pytest.org/) — fixtures and parametrization
  used in `tests/test_maze.py`.
- Wikipedia — [maze generation
  algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) and
  [spanning trees](https://en.wikipedia.org/wiki/Spanning_tree), for the
  background behind why a randomized DFS carve gives a perfect maze.

### AI usage

An AI assistant (Claude) was used during development: to discuss
generation/pathfinding algorithm trade-offs before settling on the
Recursive Backtracker and BFS/A*, to review `mazegen/config.py` for
validation edge cases we'd missed, to review the "42"-pattern placement
logic in `mazegen/utils.py`, and to help draft the pytest suite and this
README. Everything suggested was reviewed, tested, and understood before
being kept.

## Configuration file format

One `KEY=VALUE` pair per line, read from a plain text file (default:
`config.txt`, committed at the repo root). Blank lines and lines starting
with `#` are ignored.

Below is the complete structure and format of your config file: a full
example, then every key with its type and rules.

### Complete configuration example

```text
# Maze dimensions (WIDTH: 1-40, HEIGHT: 1-25)
WIDTH=25
HEIGHT=15

# Entry and exit coordinates (x,y), inside the maze, must differ
ENTRY=0,0
EXIT=24,14

# Output file for the exported maze
OUTPUT_FILE=maze.txt

# True = perfect maze (single path); False = Pac-Man-ready board (default)
PERFECT=False

# Optional keys
SEED=42
ALGORITHM=BFS
MIN_LOOPS=3
ANIMATE=False
```

### Required keys

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | int | Maze width in cells (1-40) | `WIDTH=25` |
| `HEIGHT` | int | Maze height in cells (1-25) | `HEIGHT=15` |
| `ENTRY` | `x,y` | Entry coordinates, inside the maze | `ENTRY=0,0` |
| `EXIT` | `x,y` | Exit coordinates, inside the maze, different from ENTRY | `EXIT=24,14` |
| `OUTPUT_FILE` | string | Destination file for the exported maze | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | `True` for a perfect (single-path) maze | `PERFECT=False` |

### Optional keys

| Key | Type | Default | Description |
|---|---|---|---|
| `SEED` | int | random, printed to the console | RNG seed, for reproducible generation |
| `ALGORITHM` | `BFS` \| `ASTAR` | `BFS` | Shortest-path solving algorithm |
| `MIN_LOOPS` | int (≥1) | `2` | Minimum independent routes in non-perfect mode |
| `ANIMATE` | bool | `False` | Animate generation and the final path reveal |

Booleans accept `True`/`False`, `1`/`0`, `yes`/`no`, case-insensitive.

### Validation

Required keys must all be present; `WIDTH`/`HEIGHT` are positive integers
within the subject's 40×25 cap; `ENTRY`/`EXIT` must be inside the maze and
different from each other; `OUTPUT_FILE` can't be empty; `ALGORITHM`, if
given, must be `BFS` or `ASTAR`. Anything wrong — a missing file, a
malformed line, a failed check — prints a clear message on stderr and
exits with status 1. It never crashes with a raw traceback.

## Maze generation algorithm

The generation algorithm is the **Recursive Backtracker**, run as an
iterative DFS with an explicit stack rather than actual recursion, so
there's no Python recursion-depth ceiling on large mazes.

### Why this algorithm

It builds a perfect spanning tree in linear time, it's easy to reason
about and defend (it's just a DFS carve with backtracking), and it tends
to produce long, winding corridors instead of the short dead-ends
algorithms like Prim's are prone to. It also composes cleanly with the
post-processing step below, since extra walls get opened on top of the
finished tree independently of how that tree was carved.

When `PERFECT=False` (the default), a second pass turns the tree into a
Pac-Man-ready board:

1. **Braiding** — every genuine dead-end gets one extra wall opened, as
   long as that doesn't create a forbidden fully-open 3×3 block.
2. **Loop top-up** — random extra connections are added until the maze's
   cycle rank (`edges - nodes + 1`) reaches `MIN_LOOPS`, so "at least N
   independent routes" is an actual guarantee, not a hope.

Both steps only ever open walls on top of an already-connected tree, so
connectivity can't break, and every candidate wall is checked against the
3×3 rule first.

The **"42" pattern** is reserved before generation starts — its cells are
pre-marked as visited, so nothing downstream ever touches a wall on any of
their sides, and they stay fully closed by construction. Several
placements are tried, closest to centre first, until one is found that
doesn't overlap the corners, the centre, or the entry/exit. If the maze is
too small for any placement to fit, generation carries on without the
pattern and prints a warning.

## Maze solving

Two algorithms are available via `ALGORITHM`, both returning the true
shortest path:

- **BFS** (default) — level-by-level search.
- **A\*** (`ALGORITHM=ASTAR`) — Manhattan-distance heuristic; same path
  length as BFS, usually visits fewer cells getting there.

Solving doesn't care how the maze was generated — either algorithm works
on any maze the generator produces.

## Reusable module (`mazegen`)

The reusable part is the entire `mazegen` package — no dependency on the
CLI or on config files, installable and importable on its own.

| Module | Responsibility |
|---|---|
| `cell.py` | A single maze cell and its four wall flags |
| `maze.py` | The cell grid, with neighbour/wall/bounds helpers |
| `generator.py` | `MazeGenerator` — perfect and playable generation |
| `solver.py` | BFS and A* shortest-path solving |
| `renderer.py` | Unicode box-drawing terminal rendering |
| `exporter.py` | Hex-format file export |
| `utils.py` | The "42" pattern and the "must stay open" cells |
| `config.py` | `MazeConfig` (Pydantic) — parsing and validation |
| `app.py` | CLI orchestration (not required to reuse) |

The internal structure is deliberately not the hex format: cells expose
plain `.north`/`.east`/`.south`/`.west` booleans, and hex-encoding only
happens inside `exporter.py`.

### Basic usage

```python
from mazegen import MazeGenerator, solve_bfs, export_maze

generator = MazeGenerator(width=20, height=15, seed=42)
generator.generate_perfect(start_x=0, start_y=0)

maze = generator.maze
path = solve_bfs(maze, entry=(0, 0), exit_=(19, 14))

export_maze(maze, (0, 0), (19, 14), path, "maze.txt")  # optional
```

### Custom parameters

```python
# Non-perfect, Pac-Man-ready, at least 3 independent routes:
generator = MazeGenerator(width=30, height=20, seed=123)
generator.generate_playable(start_x=0, start_y=0, min_loops=3)
```

### Accessing the structure and a solution

`generator.maze` is a `Maze` holding a grid of `Cell` objects
(`maze.get_cell(x, y)`). `solve_bfs`/`solve_astar` take that `Maze` plus
entry/exit and return the solution as `"N"`/`"E"`/`"S"`/`"W"` letters.

### Building the package

```bash
make build
```

produces `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the
repo root, installable anywhere with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Distributed under the MIT license (`LICENSE.md`), which explicitly permits
reuse and redistribution.

## Visual representation

The maze renders as Unicode box-drawing line art — thin walls, not solid
blocks — with entry, exit, and (on request) the shortest path picked out
in colour:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

1. **Re-generate** — new random maze, re-rendered, output file rewritten.
2. **Show/Hide path** — toggle the solution overlay.
3. **Rotate wall colours** — cycle an ANSI colour palette.
4. **Quit**.

## Advanced features

- Two generation modes (`PERFECT`): perfect maze, or Pac-Man board.
- Two solving algorithms: BFS and A* (`ALGORITHM`).
- Generation animation (`ANIMATE=True`) — redraws after every wall
  removal, then reveals the final path cell by cell. Off by default; it
  adds real-time delay proportional to maze size.
- Reproducible via `SEED` — if omitted, one is generated and printed so
  the run can still be reproduced afterwards.

## Team & project management

**Roles.** artavagy: generation and solving core (`generator.py`,
`solver.py`, the "42"-pattern placement), configuration validation.
grgrigor: terminal rendering (`renderer.py`), CLI orchestration
(`app.py`, `a_maze_ing.py`), packaging, documentation. Both reviewed and
tested each other's modules throughout, using Chapter IV.4 of the subject
as the shared contract between generation and rendering.

**Planning.** The plan was to fix the internal maze representation first
(`Cell`/`Maze`/`MazeGenerator`), then build generation → solving →
rendering → exporting → packaging → documentation, working in parallel
once that shared model was settled. It mostly held, with a few real
course corrections along the way: config validation moved from
hand-written checks to a Pydantic schema after we kept missing edge cases
by hand; the non-perfect mode's loop guarantee went from an "open a
handful of extra walls" heuristic to a cycle-rank count that's actually
checkable, after realizing the heuristic couldn't promise the subject's
"at least two independent routes"; the "42" placement changed from a
fixed spot with overlaps subtracted out (which could punch a hole in the
digit) to searching for a spot with no overlap at all; A* got added
alongside BFS; and the renderer moved from blocky walls to box-drawing
line art.

**What worked.** Reserving the "42" pattern before generation — marking
its cells visited up front — meant the generator and the loop step never
needed special-case logic to avoid it. Keeping `mazegen` fully independent
of the CLI made it trivial to unit-test generation and solving without
touching a config file or a terminal. And swapping the heuristic loop
count for a formally checkable one turned "looks fine on a few seeds" into
an actual guarantee, catching a real gap before it could reach evaluation.

**What's left.** Optional colouring for the "42" pattern cells. A second
generation algorithm (Prim's or Kruskal's) behind the same
`ALGORITHM`-style pattern already used for solving. A MiniLibX display as
an alternative to the terminal. Animating the braiding/loop-top-up pass,
not just the initial carve.

**Tools.** Python 3.10+, Poetry, Pydantic, pytest, flake8, mypy, Git.

## License

MIT — see `LICENSE.md`.

## Authors

- artavagy
- grgrigor
