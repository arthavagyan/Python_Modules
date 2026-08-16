# A-Maze-ing — project rules (extracted from the 42 subject, verbatim requirements)

This file is the ground truth for this project. It is a distilled, exhaustive
extraction of `/home/arth/Yop/Python_Modules/subjects/A-Maze-ing.pdf`
(20 pages, read in full). Every rule below is a hard requirement unless
explicitly marked optional/bonus. When in doubt, re-check the PDF page
referenced in brackets before deviating from this file.

Two prior draft implementations exist for reference/salvage at `/home/arth/Yop/M`
and `/home/arth/Yop/H`. `H` is architecturally closer to these rules; `M` has a
couple of good ideas (see "Known pitfalls" at the bottom). Neither prior draft
fully satisfies this file — do not assume either is a finished spec.

---

## 1. General rules [Ch. III.1]

- Python **3.10+**.
- Must pass **flake8** (default rules, no loosened config — the grader runs
  the same commands we do).
- Must pass **mypy** with:
  `--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
  (this is the `make lint` target; a `--strict` variant is optional as
  `make lint-strict`).
- Functions must handle exceptions gracefully (`try/except`), never crash on
  unhandled exceptions — **a crash during review = non-functional**.
- All resources (files, etc.) via context managers (`with`).
- Type hints everywhere applicable (`typing` module).
- Docstrings on functions/classes, PEP 257 style (Google or NumPy).

## 2. Makefile [Ch. III.2]

Required targets:
- `install` — install deps (pip/uv/pipx/poetry, any manager).
- `run` — run the main script.
- `debug` — run the main script under `pdb`.
- `clean` — remove `__pycache__`, `.mypy_cache`, build artifacts.
- `lint` — `flake8 .` and the exact mypy invocation above.
- `lint-strict` (optional) — `flake8 .` and `mypy . --strict`.

## 3. Additional guidelines [Ch. III.3]

- Test programs (pytest/unittest) are encouraged but **not graded/submitted**
  as a requirement — still worth having for our own confidence and for
  defending the project.
- `.gitignore` excluding Python artifacts (`__pycache__/`, `.mypy_cache/`,
  `venv/`, `dist/`, `*.egg-info/`, etc.).
- A virtualenv is recommended for dev isolation.

## 4. Entry point and usage [Ch. IV.1–IV.2]

- Main file **must be named exactly `a_maze_ing.py`** — non-negotiable.
- Run command: `python3 a_maze_ing.py config.txt` — config filename itself is
  free (config.txt is just an example / our default).
- Must handle **all** errors gracefully: invalid config, file not found, bad
  syntax, impossible maze parameters, etc. Never crash unexpectedly; always
  print a clear error message.

## 5. Configuration file format [Ch. IV.3]

One `KEY=VALUE` per line. Lines starting with `#` are comments, ignored.

### Mandatory keys

| Key | Type | Example |
|---|---|---|
| `WIDTH` | int, number of cells | `WIDTH=20` |
| `HEIGHT` | int, number of cells | `HEIGHT=15` |
| `ENTRY` | `x,y` | `ENTRY=0,0` |
| `EXIT` | `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | string | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | `PERFECT=True` |

### Optional keys we define ourselves (must be documented in README)

- `SEED` — int. If omitted, auto-generate one (and it's good practice to
  print/log it so the run is still reproducible after the fact).
- `ALGORITHM` — solving algorithm, e.g. `BFS` / `ASTAR`.
- `MIN_LOOPS` — minimum extra loops for non-perfect mode.
- `ANIMATE` — bool, animate generation.

A **default `config.txt` must exist in the repo root** and be committed.

### Validation (before generation) — must raise a clear, catchable error, never a raw traceback

- `WIDTH`, `HEIGHT` are positive integers.
- **`WIDTH` ≤ 40 and `HEIGHT` ≤ 25** — maze dimensions must not exceed 40×25.
  *(Both M and H prior drafts are missing this check — do not repeat that.)*
- `ENTRY` and `EXIT` exist, are different cells, and are inside maze bounds.
- Boolean values accepted: `True`, `False`, `1`, `0`, `yes`, `no` (any case).
- Integer values are valid integers.
- `OUTPUT_FILE` is not empty.
- Optional parameters, if present, contain valid values.

## 6. Maze requirements [Ch. IV.4]

- Randomly generated, but **reproducible via a seed**.
- Each cell has 0–4 walls (N/E/S/W).
- Validity:
  - Entry and exit exist, differ, are inside bounds.
  - Full connectivity, no isolated cells (except the "42" pattern cells).
  - Entry/exit sit at the maze's external border walls as required.
  - **Wall data must be coherent**: a shared wall must be encoded identically
    from both neighboring cells' perspective (open one side ⇒ open the
    other side too, always in the same operation).
- **No open area wider than 2 cells in any direction** — i.e. never a fully
  open 3×3 block of cells. (A 2×3 or 3×2 open area is fine.)
- The maze must visibly contain a **"42" pattern** drawn by several
  **fully-closed** (all 4 walls up) cells, when rendered.
  - If the maze is too small to fit it: **do not crash** — print a warning to
    the console and continue without the pattern.
  - The "42" cells must form a coherent, unbroken shape — don't just subtract
    overlapping cells from a fixed placement (that can punch holes in the
    digits); search for a placement that avoids protected cells entirely.
- **`PERFECT=True`**: exactly one path between entry and exit — a true perfect
  maze, zero loops.
- **`PERFECT=False` (default)**: must be a board directly usable by a
  Pac-Man-like game:
  - Full connectivity (whole board fillable with pac-gums, winnable).
  - The **four corners and the centre are open corridors** (ghosts/super-gums
    in corners, player starts centre) — never inside the "42" pattern, never
    unreachable dead single-wall pockets.
  - **At least two independent routes** (loops) — a perfect maze, or a
    perfect maze with just one wall removed (single loop), is **not**
    acceptable in this mode. Verify this formally, e.g. via cycle rank
    (`edges − nodes + 1 ≥ 2` over the connectivity graph), not just "opened N
    extra walls and hoped."
  - Dead-ends should be rare (a couple tolerated); **zero dead-ends is a
    bonus**, not the mandatory bar.

## 7. Output file format [Ch. IV.5]

One hex digit per cell, bit = wall **closed**:

| Bit (LSB→) | Direction |
|---|---|
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

- Closed wall → bit `1`; open → bit `0`. Example: `3` (`0011`) = south+west
  open. `A` (`1010`) = east+west closed.
- Cells stored row by row, one row per line (`WIDTH` hex chars per line).
- Then **one empty line**, then exactly 3 more lines:
  1. entry coordinates `x,y`
  2. exit coordinates `x,y`
  3. shortest path from entry to exit as a string of `N`/`E`/`S`/`W`
- **Every line ends with `\n`**, including the last one.
- An analysis script `maze_analyzer.py` (provided separately by the subject,
  not something we write) checks wall coherence and perfect/playable status —
  use it against our own output once we have it, including the bonus
  `--max-dead-ends 0` flag.

## 8. Visual representation [Ch. V]

- Either **terminal ASCII rendering** or a **MiniLibX (MLX) graphical
  display**. We are going with terminal ASCII (both prior drafts did too —
  MLX needs an external C-library binding, disproportionate effort here).
- Must clearly show walls, entry, exit, and the solution path.
- Mandatory user interactions, at minimum:
  1. Re-generate a new maze and display it.
  2. Show/hide the valid shortest path.
  3. Change maze wall colours.
  4. (Optional) set specific colours for the "42" pattern.
- Extra interactions are allowed beyond these.

## 9. Code reusability requirements [Ch. VI]

- Maze **generation logic must be a standalone, importable class** (subject's
  own example name: `MazeGenerator`) in a module separate from the CLI.
- Must document (in the reusable module *and* in the main README):
  1. How to instantiate/use the generator, with a basic example.
  2. How to pass custom parameters (size, seed, etc.).
  3. How to access the generated structure and at least one solution.
  - Note: the module's internal structure **does not have to match** the
    output file's hex format — it can expose its own richer representation.
- The **entire reusable module (code + docs) must build into a single
  pip-installable package file at the repo root**.
  - **Package must be named `mazegen-*`** (e.g.
    `mazegen-1.0.0-py3-none-any.whl`). Not `a-maze-ing`, not anything else.
  - `.tar.gz` or `.whl` both acceptable, as produced by a standard Python
    build.
  - All build inputs must be in the repo so the package can be rebuilt from
    source in a clean venv during evaluation.
- A **`LICENSE.md` at the repo root**, explicitly permitting reuse and
  redistribution of the generator by later projects (MIT/Apache-2.0/BSD-3 all
  fine; MIT is simplest).

## 10. README.md requirements [Ch. VII]

Required at repo root. Must include, **at minimum**:

- **First line, italicized, exact format**:
  `*This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].*`
  — list **every** team member's login here, matching LICENSE.md/pyproject
  authorship. (H's prior draft only listed one of two authors on this line —
  don't repeat that.)
- **Description** section — goal + brief overview.
- **Instructions** section — build/install/run.
- **Resources** section — classic references (docs, articles, tutorials) +
  an honest account of how AI was used, for which specific tasks/parts.
- Project-specific additions explicitly required by this subject:
  - Complete structure/format of the config file.
  - Which maze generation algorithm was chosen, and **why**.
  - What part of the code is reusable, and how.
  - Team & project management: roles of each member; how the anticipated
    plan evolved to the final result; what worked well / what could be
    improved; which specific tools were used.
  - Description of any advanced features implemented (multiple algorithms,
    display options, etc.).
- English recommended; campus main language acceptable alternative.
- **Do not describe files/structure that don't actually exist in the repo**
  (H's prior draft listed `tests/`, `maze_analyzer.py`, `requirements.txt` in
  its README's project tree while none of them existed on disk — this is
  exactly the kind of mismatch a "double-check your file names" evaluator
  will catch).

## 11. Bonuses [Ch. VIII] — only after mandatory part is airtight

- Non-perfect maze with **zero dead-ends at all** (fully braided), verifiable
  via `maze_analyzer.py --max-dead-ends 0`.
- Support for **multiple maze generation algorithms**.
- **Animation** during maze generation.

## 12. Submission & evaluation [Ch. IX]

- Only what's inside the Git repo is evaluated — double check filenames.
- During evaluation, a **brief live modification** of the project may be
  requested (a small behavior change / feature, expected to be feasible in a
  few minutes) to verify real understanding — be ready to navigate the
  codebase quickly and explain any part of it.

---

## Known pitfalls to avoid (from the M/H prior-draft review)

- Missing the **40×25 max dimension** validation — both drafts missed it.
- Wrong pip package name (`a-maze-ing` instead of `mazegen-*`).
- "42" pattern built by subtracting protected cells from a fixed placement
  instead of searching for a placement that avoids them — can silently punch
  a hole in the "4" or "2".
- Non-perfect mode "loop count" done by heuristically opening
  `width*height // 8` walls with no formal check that ≥2 independent routes
  actually exist — prefer the cycle-rank check (`edges − nodes + 1`).
- README claiming files/sections that don't exist in the actual repo.
- README's mandatory first line missing a team member.
- Trailing-newline flake8 warnings (`W292`) — trivial but free points, make
  sure every source file ends with `\n`.
