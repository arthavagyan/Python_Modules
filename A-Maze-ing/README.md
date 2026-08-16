*This project has been created as part of the 42 curriculum by artavagy, grgrigor.*

# A-Maze-ing

## Description

A-Maze-ing is a Python application that generates, solves, displays, and
exports 2D mazes from a plain-text configuration file. It supports two
generation modes:

- **`PERFECT=True`** — a classic perfect maze: exactly one path between any
  two cells, no loops at all.
- **`PERFECT=False`** (default) — a Pac-Man-ready board: fully connected,
  the four corners and the centre are open corridors, at least two
  independent routes exist between any two points, and dead-ends are rare.

Both modes embed a visible **"42" pattern**, drawn by cells that stay fully
walled off, and both are solved with a shortest-path search (BFS or A*)
before being rendered in the terminal and exported to a hex-encoded file.

The project is split into two independent parts:

- **Application** (`a_maze_ing.py`) — a thin CLI: reads the config file,
  calls into `mazegen`, writes the output file, and runs the interactive
  terminal viewer.
- **Reusable package** (`mazegen/`) — all maze logic (config validation,
  generation, solving, rendering, exporting, utilities). It has no
  dependency on the CLI and can be installed and imported independently in
  other projects.

## Instructions

Install the project dependencies (uses [Poetry](https://python-poetry.org/)):

```bash
make install
# equivalent to: poetry install
```

Run the application:

```bash
make run
# equivalent to: poetry run python a_maze_ing.py config.txt
```

or directly:

```bash
python3 a_maze_ing.py config.txt
```

Run in the debugger:

```bash
make debug
```

Run the linters (flake8 + mypy, exact flags required by the subject):

```bash
make lint
make lint-strict   # optional, stricter mypy --strict pass
```

Run the test suite:

```bash
make test
```

Build the reusable `mazegen` package (`.whl` + `.tar.gz`, copied to the repo
root as required):

```bash
make build
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

## Configuration file format

The application reads one `KEY=VALUE` pair per line from a plain text file
(default: `config.txt`, committed at the repo root). Blank lines and lines
starting with `#` are ignored.

The following is the complete structure and format of your config file: a
full example first, then every supported key, its type, and its
validation rules.

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

Boolean values accept `True`/`False`, `1`/`0`, `yes`/`no` (case-insensitive).

### Validation

Before generating anything, the config is validated: all required keys are
present; `WIDTH`/`HEIGHT` are positive integers within the 40×25 subject
limit; `ENTRY`/`EXIT` are inside the maze and different from each other;
`OUTPUT_FILE` is non-empty; `ALGORITHM`, when given, is `BFS` or `ASTAR`.
Any problem — a missing file, a malformed line, or a failed check — is
reported as a clear message on stderr; the program never crashes with a raw
traceback.

## Maze generation algorithm

Mazes are carved with the **Recursive Backtracker** (an iterative DFS with
an explicit stack, so there's no Python recursion-depth limit). It was
chosen because it:

- generates a perfect spanning tree in linear time;
- is simple to reason about and to defend;
- produces long, visually interesting corridors rather than a maze full of
  short dead-ends (as Prim's tends to);
- composes cleanly with the post-processing step below, since walls can be
  opened on top of the tree independently of how it was built.

When `PERFECT=False` (the default), a second pass turns that tree into a
Pac-Man-ready board:

1. **Braiding** — every real dead-end (a cell with only one open wall) gets
   one extra wall opened, if that can be done without creating a forbidden
   open 3×3 block.
2. **Loop top-up** — random extra connections are added until the maze's
   cycle rank (`edges - nodes + 1` over the connectivity graph) reaches at
   least `MIN_LOOPS`, guaranteeing at least that many genuinely independent
   routes rather than just "some walls were opened."

Both steps only ever *open* walls on top of the already-connected tree, so
connectivity can never break, and every candidate wall is checked against
the "no 3×3 open area" rule before being opened.

The **"42" pattern** is reserved *before* generation starts: its cells are
pre-marked as visited, so the backtracker and the loop/braid steps never
touch a wall on any of their sides, and they stay fully closed by
construction — no extra bookkeeping needed to keep the shared walls
between a reserved and a normal cell coherent. Several candidate placements
are tried (closest-to-centre first) until one is found that doesn't overlap
the four corners, the centre, or the entry/exit; if the maze is too small
for any placement to fit, generation continues without the pattern and a
warning is printed.

## Maze solving

The solved path is always the true shortest path between entry and exit:

- **BFS** explores level by level and is the default.
- **A\*** (`ALGORITHM=ASTAR`) uses the Manhattan-distance heuristic; it
  returns a path of the same length but typically visits fewer cells.

Solving is entirely independent of generation — either algorithm works on
any maze produced by any generator.

## Reusable module (`mazegen`)

The reusable part of the project is the `mazegen` package: it has no
dependency on the CLI (`a_maze_ing.py`) or on config files, and can be
imported into any other Python project.

| Module | Responsibility |
|---|---|
| `cell.py` | A single maze cell and its four wall flags |
| `maze.py` | The cell grid, with neighbor/wall/bounds helpers |
| `generator.py` | `MazeGenerator` — perfect and playable (Pac-Man) generation |
| `solver.py` | BFS and A* shortest-path solving |
| `renderer.py` | Unicode box-drawing terminal rendering |
| `exporter.py` | Hex-format file export |
| `utils.py` | The "42" pattern and the corner/centre "must stay open" cells |
| `config.py` | `MazeConfig` (Pydantic) — config file parsing and validation |
| `app.py` | CLI orchestration (used by `a_maze_ing.py`, not required to reuse) |

Note the internal maze structure is *not* the same as the exported hex
format — the module exposes cell objects with `.north`/`.east`/`.south`/
`.west` booleans; hex-encoding only happens in `exporter.py`.

### Basic usage

```python
from mazegen import MazeGenerator, solve_bfs, export_maze

generator = MazeGenerator(width=20, height=15, seed=42)
generator.generate_perfect(start_x=0, start_y=0)

maze = generator.maze                       # the generated structure
path = solve_bfs(maze, entry=(0, 0), exit_=(19, 14))   # a solution

export_maze(maze, (0, 0), (19, 14), path, "maze.txt")  # optional
```

### Custom parameters

```python
# A non-perfect, Pac-Man-ready board with at least 3 independent routes:
generator = MazeGenerator(width=30, height=20, seed=123)
generator.generate_playable(start_x=0, start_y=0, min_loops=3)
```

### Building the package

```bash
make build
```

produces `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the
repo root (also committed there, per the subject's requirement), installable
in any other project with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

`mazegen` is distributed under the MIT license (see `LICENSE.md`), which
explicitly permits reuse and redistribution by later projects.

## Visual representation

The maze is rendered in the terminal as Unicode box-drawing line art (walls
as thin lines, not blocks), with the entry, exit, and — on request — the
shortest path highlighted in colour. After the initial render, an
interactive menu lets you:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

1. **Re-generate** — carve a brand-new maze (fresh random seed) and
   re-render it, re-exporting the output file.
2. **Show/Hide path** — toggle the BFS/A* solution overlay.
3. **Rotate wall colours** — cycle through an ANSI colour palette.
4. **Quit**.

## Advanced features

- **Two generation modes** (`PERFECT` flag): a true perfect maze, or a
  fully connected, multi-route, Pac-Man-ready board.
- **Two solving algorithms**: BFS and A* (`ALGORITHM` key).
- **Generation animation** (`ANIMATE=True`): the maze is redrawn after every
  wall removal, then the final shortest path is revealed one cell at a
  time. Off by default because it adds a real-time delay proportional to
  the maze's cell count.
- **Reproducible generation** via `SEED`; if omitted, one is generated and
  printed so the run can still be reproduced afterwards.

## Team & project management

### Roles

- **artavagy** — maze generation & solving core (`generator.py`,
  `solver.py`, the "42"-pattern placement algorithm), configuration
  validation.
- **grgrigor** — terminal rendering (`renderer.py`), CLI/application
  orchestration (`app.py`, `a_maze_ing.py`), packaging, and documentation.

Both reviewed and tested each other's modules throughout; the maze
requirements (Chapter IV.4 of the subject) were treated as the shared
contract between generation and rendering.

### Anticipated planning and how it evolved

The initial plan was: agree on the internal maze representation first (a
`Cell`/`Maze`/`MazeGenerator` layered design), then build generation →
solving → rendering → exporting → packaging → documentation in that order,
in parallel where possible once the shared data model was settled.

During development, the plan evolved as the team:

- reworked configuration validation from hand-written checks into a
  Pydantic schema, after realizing manual parsing made it easy to miss
  edge cases (out-of-bounds entry/exit, dimensions beyond the 40×25 limit);
- strengthened the non-perfect mode's loop guarantee from an ad-hoc "open
  a handful of extra walls" heuristic into a formally checkable cycle-rank
  count (`edges - nodes + 1 >= MIN_LOOPS`), after realizing the heuristic
  alone couldn't actually guarantee the subject's "at least two independent
  routes" requirement;
- reworked the "42" pattern placement from a fixed central position with
  overlapping cells subtracted out, to searching for a placement that
  fully avoids the corners/centre/entry/exit — the original approach could
  silently punch a hole in the digit shape when it overlapped a protected
  cell;
- added A* as a second solving algorithm alongside BFS;
- switched the terminal renderer from a blocky wall style to Unicode
  box-drawing line art for a clearer, more classic maze look.

### What worked well

- Reserving the "42" pattern *before* generation, by pre-marking its cells
  as visited, means the generator and the post-processing loop step never
  need special-case logic to avoid it — wall coherence with reserved cells
  falls out for free.
- Keeping the reusable `mazegen` package fully independent of the CLI made
  it straightforward to unit-test generation and solving without ever
  touching a config file or the terminal.
- Replacing the heuristic loop count with a formally checkable one (cycle
  rank) turned "looks fine on a few seeds" into an actual guarantee, and
  caught a real correctness gap early.

### What could be improved

- Add optional distinct colouring for the "42" pattern cells (mentioned as
  an optional interaction in the subject, not yet implemented).
- Support more generation algorithms (Prim's, Kruskal's) behind the
  `ALGORITHM`-style config pattern already used for solving.
- Add a MiniLibX graphical display as an alternative to the terminal.
- Animate the non-perfect post-processing (braiding/loop top-up) step, not
  just the initial tree carve.

### Tools used

- **Python 3.10+** — implementation language.
- **Poetry** — dependency management, packaging, and build.
- **Pydantic** — declarative configuration validation.
- **pytest** — unit testing.
- **flake8** / **mypy** — linting and static type checking.
- **Git** — version control.

## Resources

### Documentation

- [Python Standard Library documentation](https://docs.python.org/3/library/) —
  `random.Random` for seeded generation (`generator.py`), `heapq` for the
  A* priority queue and `collections.deque` for BFS (`solver.py`),
  `pathlib` for config file handling (`config.py`).
- [Pydantic documentation](https://docs.pydantic.dev/) — field/model
  validators, custom error messages, used throughout `mazegen/config.py`.
- [PEP 8](https://peps.python.org/pep-0008/) — style guide followed
  throughout, and the basis for the `flake8` configuration.
- [PEP 257](https://peps.python.org/pep-0257/) — docstring conventions
  used across all `mazegen` modules.
- [pytest documentation](https://docs.pytest.org/) — fixtures and
  assertion patterns used in `tests/`.
- Wikipedia — [Maze generation
  algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) and
  [Spanning tree](https://en.wikipedia.org/wiki/Spanning_tree) — background
  for why the recursive backtracker produces a perfect maze.

### AI usage

This section describes how AI was used in the project: an AI assistant
(Claude) was used during development, and the table below specifies for
which tasks and for which parts of the project it was used:

| Task | Part of the project |
|---|---|
| Reading the subject PDF in full and extracting every hard requirement (exact filenames, package naming, hex bit layout, the 40×25 size cap, the non-perfect-mode loop/dead-end rules) into a checklist used throughout development | Project-wide reference, not shipped code |
| Discussing maze generation and pathfinding algorithm trade-offs (Recursive Backtracker vs. Prim's/Kruskal's; BFS vs. A*) | `mazegen/generator.py`, `mazegen/solver.py` |
| Reviewing the configuration validation logic and catching missing edge cases (the 40×25 size cap, `ENTRY == EXIT`, out-of-bounds coordinates) | `mazegen/config.py` |
| Reviewing the "42" pattern placement logic and catching a case where a fixed placement with overlapping cells removed could produce a broken/incomplete digit shape, which led to the collision-search placement approach used instead | `mazegen/utils.py` |
| Helping design and write the pytest suite | `tests/test_maze.py` |
| Helping write and structure this documentation | `README.md` |

All AI-assisted code and documentation were reviewed, run against
`flake8`/`mypy`/`pytest`, and manually exercised (both `PERFECT` modes, both
solving algorithms, animation on/off) before being treated as final.

## License

This project is distributed under the MIT License. See `LICENSE.md` for
details.

## Authors

- artavagy
- grgrigor
