# A-Maze-ing — Pre-Submission Verification Guide

This is a manual verification checklist, mapped to the subject's chapters.
Every check below was actually run against this project and the real
output is shown, so you can either trust the evidence as-is or re-run each
command yourself before submitting. Nothing here is graded — it's purely
for your own peace of mind.

---

## Part 0 — How to run this project, step by step

The `Makefile` (and the README) document running everything through
[Poetry](https://python-poetry.org/), but Poetry isn't installed on this
machine right now. Two paths below: the quick one that works immediately
with a plain venv, and the canonical one via Poetry if you'd rather match
the README exactly.

### Option A — plain venv (works right now, no extra install)

1. Open a terminal and go to the project folder:
   ```bash
   cd /home/arth/Yop/Python_Modules/A-Maze-ing
   ```
2. Create a virtual environment (one-time step):
   ```bash
   python3 -m venv .venv
   ```
3. Install the dependencies into it:
   ```bash
   .venv/bin/pip install pydantic flake8 mypy pytest
   ```
4. Run the application on the default config:
   ```bash
   .venv/bin/python3 a_maze_ing.py config.txt
   ```
   You should see the maze printed, then:
   ```
   === A-Maze-ing ===
   1. Re-generate a new maze
   2. Show / Hide the shortest path
   3. Rotate the wall colours
   4. Quit
   Choice? (1-4):
   ```
   Type `1`, `2`, or `3` and press Enter to try each interaction; type `4`
   to quit.
5. (Optional) run it on a different config file the same way:
   ```bash
   .venv/bin/python3 a_maze_ing.py path/to/other_config.txt
   ```
6. (Optional) run the linters and tests the same way `make lint`/`make test`
   would:
   ```bash
   .venv/bin/flake8 .
   .venv/bin/mypy . --warn-return-any --warn-unused-ignores \
       --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
   PYTHONPATH=. .venv/bin/pytest tests/ -v
   ```
7. (Optional) build the reusable package the same way `make build` would:
   ```bash
   .venv/bin/pip install build
   .venv/bin/python3 -m build .
   cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
   ```

`.venv/` is already listed in `.gitignore`, so it's never committed —
delete it any time with `rm -rf .venv` and repeat steps 2-3 to rebuild it.

### Option B — Poetry (matches the README/Makefile exactly)

1. Install Poetry (one-time, only if you don't have it):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Then restart your terminal (or `source ~/.bashrc` / `source ~/.zshrc`) so
   the `poetry` command is on your `PATH`. Check it worked:
   ```bash
   poetry --version
   ```
2. From the project folder, install dependencies:
   ```bash
   cd /home/arth/Yop/Python_Modules/A-Maze-ing
   make install
   ```
3. Run it:
   ```bash
   make run
   ```
4. Everything else from here on matches the README 1:1:
   ```bash
   make lint
   make lint-strict
   make test
   make build
   make debug
   ```

If you only ever plan to run this project on this one machine, Option A is
simpler and does everything you need. Option B is worth doing once before
submission, since it proves the project works exactly the way the README
tells an evaluator to run it.

---

## Part 1 — One-shot automated check

```bash
make install
make lint          # flake8 + mypy with the subject's required flags
make lint-strict    # optional, stricter mypy --strict
make test           # pytest suite
make build           # builds mazegen-*.whl / .tar.gz into the repo root
```

Real output, captured against the current code:

```
$ flake8 .
OK: no issues

$ mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
        --disallow-untyped-defs --check-untyped-defs
Success: no issues found in 13 source files

$ mypy mazegen a_maze_ing.py --strict
Success: no issues found in 11 source files

$ pytest tests/ -q
....................
20 passed in 0.21s
```

If any of these fail after you make further changes, fix them before doing
anything else — a red `make lint`/`make test` is the fastest signal
something regressed.

---

## Part 2 — Manual walkthrough, by subject chapter

### Chapter III — General rules

- [ ] **Python 3.10+**: `python3 --version`
- [ ] **flake8 clean**: `make lint` (see Part 1 output above)
- [ ] **mypy clean**, exact required flags: `make lint` (see above)
- [ ] **mypy --strict clean** (optional bonus rigor): `make lint-strict` (see above)
- [ ] **Makefile has `install`/`run`/`debug`/`clean`/`lint`/`lint-strict`**: open `Makefile` and confirm all six targets exist
- [ ] **`.gitignore` excludes Python artifacts**: `cat .gitignore`

### Chapter IV.2 — Usage & error handling

The program must never crash with a raw traceback. Real transcripts:

```
$ python3 a_maze_ing.py
Usage: python3 a_maze_ing.py <config_file>
(exit code 1)

$ python3 a_maze_ing.py /tmp/does_not_exist.txt
Error: Configuration file not found: /tmp/does_not_exist.txt
(exit code 1)

$ printf "WIDTH 10\n" > bad.txt && python3 a_maze_ing.py bad.txt
Error: bad.txt:1: invalid line 'WIDTH 10' (expected KEY=VALUE)
(exit code 1)
```

- [ ] Reproduce these three yourself (or invent your own broken config) and
      confirm you always get a clean one-line error, never a Python
      traceback.

### Chapter IV.3 — Configuration validation

```
$ printf "WIDTH=41\nHEIGHT=10\nENTRY=0,0\nEXIT=1,1\nOUTPUT_FILE=x.txt\nPERFECT=True\n" > bad_width.txt
$ python3 a_maze_ing.py bad_width.txt
Error: invalid configuration in bad_width.txt:
1 validation error for MazeConfig
width
  Input should be less than or equal to 40 [type=less_than_equal, input_value='41', ...]
(exit code 1)

$ printf "WIDTH=10\nHEIGHT=10\nENTRY=2,2\nEXIT=2,2\nOUTPUT_FILE=x.txt\nPERFECT=True\n" > bad_entry.txt
$ python3 a_maze_ing.py bad_entry.txt
Error: invalid configuration in bad_entry.txt:
1 validation error for MazeConfig
  Value error, ENTRY and EXIT must be different cells [...]
(exit code 1)
```

- [ ] `WIDTH`/`HEIGHT` > 40×25 rejected (shown above)
- [ ] `ENTRY == EXIT` rejected (shown above)
- [ ] `ENTRY`/`EXIT` out of bounds rejected — try `ENTRY=99,0` on a 10-wide maze yourself
- [ ] A default `config.txt` exists at the repo root: `cat config.txt`

### Chapter IV.4 — Maze requirements (the core of the grading)

All checks below were run on the **same** 16×10 maze, seed 7, entry
`(0,0)`, exit `(15,9)` — once with `PERFECT=True`, once with
`PERFECT=False` — so you can compare the two modes directly.

#### PERFECT=True must be a true perfect maze (spanning tree)

```
non-reserved nodes: 127, edges: 126
tree property (edges == nodes - 1): True
```

A perfect maze on a connected grid is, by definition, a spanning tree:
exactly `nodes - 1` open connections, no more, no less. If `edges` were
ever `>= nodes`, there'd be a loop somewhere, and the maze would no longer
be perfect. See the "Reusable verification script" below to re-run this
check yourself on any output file.

- [ ] Re-run with a different seed/size and confirm `edges == nodes - 1`
      still holds.

#### PERFECT=False must be a Pac-Man-ready board

```
nodes=127 edges=141
independent loops (edges - nodes + 1) = 15   (required: >= MIN_LOOPS, here 2)
any fully-open 3x3 block: False               (required: False, always)
corners+centre reserved/degree: all "not reserved", all degree >= 2
dead-end cells (degree == 1), excluding "42": 0
```

- [ ] Loop count comfortably clears `MIN_LOOPS` (here 15 >> 2) — a real,
      *countable* number of independent routes, not just "some walls got
      opened."
- [ ] No 3×3 fully-open block anywhere (corridors never wider than 2 cells).
- [ ] All four corners and the centre are open corridors (not swallowed by
      the "42" pattern, not stuck at degree 0).
- [ ] Dead-ends are rare — 0 in this particular run, a couple is still
      acceptable per the subject; if you ever see dozens, something's off.

#### Wall coherence

```
coherence mismatches: 0   (must always be 0)
```

Every shared wall between two neighbouring cells must be encoded
identically from both sides. `0` mismatches confirms `east(x,y) ==
west(x+1,y)` and `south(x,y) == north(x,y+1)` everywhere in the grid.

#### "42" pattern

Dumping the fully-closed (`0xF`) cells from the `PERFECT=True` run above,
`#` = fully walled:

```
................
.#...#.#####....
.#...#.....#....
.#...#.....#....
.#####.#####....
.....#.#........
.....#.#........
.....#.#####....
................
................
```

- [ ] The shape reads as "4" and "2" — an intact digit, not a blob with a
      hole punched in it.
- [ ] Try a maze too small to fit the pattern (e.g. `WIDTH=10 HEIGHT=8`)
      and confirm you get a console warning, not a crash, and the maze
      still generates without the pattern.

### Chapter IV.5 — Output file format

Full `maze.txt` from the `PERFECT=True` run above:

```
bd15551555555393
afc53fafffffbaea
af97af85553fac3a
afc56fad556f87c2
afffffafffff8556
c3d53faf97956d53
96952fafc545393a
c56bafafffffc6aa
95386969539517aa
c7c456d47c47c546

0,0
15,9
SSSSSESWSEENEESSWSEENENNNNNNNNEEEEEEESSESESWWWSWWSEESENESSSE
```

- [ ] `WIDTH` (16) hex characters per row, `HEIGHT` (10) rows.
- [ ] One blank line separates the grid from the footer.
- [ ] Footer is exactly 3 lines: `entry_x,entry_y`, `exit_x,exit_y`, then
      the path as `N`/`E`/`S`/`W` letters.
- [ ] Every line, including the last, ends with `\n` — check with
      `tail -c 50 maze.txt | xxd | tail -3` and look for `0a` as the very
      last byte.
- [ ] Spot-check one hex digit by hand: top-left cell of the grid above is
      `b` = `1011` = bits 0,1,3 set = North+East+West closed, South open —
      matches it being the entry's row against the top border (North
      closed) and the left border (West closed).

### Chapter V — Visual representation

This part needs a real terminal (colours/box-drawing won't show in a
piped log), so run it yourself:

```bash
make run
```

- [ ] Walls, entry, exit are all visually distinct.
- [ ] Menu appears exactly as:
      ```
      === A-Maze-ing ===
      1. Re-generate a new maze
      2. Show / Hide the shortest path
      3. Rotate the wall colours
      4. Quit
      Choice? (1-4):
      ```
- [ ] Option `1` produces a visibly different maze and updates `maze.txt`.
- [ ] Option `2` toggles a coloured path overlay on/off.
- [ ] Option `3` visibly changes the wall colour.
- [ ] Option `4` exits cleanly (exit code 0).
- [ ] Try `ANIMATE=True` in `config.txt` and confirm generation redraws
      step by step, then the path is revealed cell by cell.

### Chapter VI — Reusable module

```
$ ls mazegen-1.0.0-py3-none-any.whl mazegen-1.0.0.tar.gz LICENSE.md config.txt
LICENSE.md  config.txt  mazegen-1.0.0-py3-none-any.whl  mazegen-1.0.0.tar.gz
```

Clean-venv install, run from *outside* the repo, proving the package has
no hidden dependency on the CLI or on being run from the project directory:

```
$ python3 -m venv /tmp/clean_venv
$ /tmp/clean_venv/bin/pip install ./mazegen-1.0.0-py3-none-any.whl
$ cd /tmp && /tmp/clean_venv/bin/python3 -c "
from mazegen import MazeGenerator, solve_bfs
g = MazeGenerator(width=10, height=8, seed=1)
g.generate_perfect(0, 0)
path = solve_bfs(g.maze, (0,0), (9,7))
print('import OK, path length:', len(path))
"
import OK, path length: 46
```

- [ ] Reproduce this yourself right before submitting — it's exactly what
      an evaluator is likely to try.
- [ ] `mazegen-*` is the package name (not `a-maze-ing` or anything else).
- [ ] `LICENSE.md` exists at the repo root and its text explicitly permits
      reuse/redistribution (MIT here).

### Chapter VII — README.md

- [ ] First line is exactly:
      `*This project has been created as part of the 42 curriculum by artavagy, grgrigor.*`
      — check with `head -1 README.md`.
- [ ] Contains a `## Description` section.
- [ ] Contains an `## Instructions` section.
- [ ] Contains a `## Resources` section with both classic references *and*
      an explicit description of how AI was used, and for which tasks.
- [ ] Explicitly covers the complete structure and format of the config
      file.
- [ ] States which maze generation algorithm was chosen, and why.
- [ ] States what part of the code is reusable, and how.
- [ ] Covers team & project management: roles, how the plan evolved, what
      worked well, what could be improved, tools used.
- [ ] English (or campus main language) throughout.

### Chapter VIII — Bonuses (optional, only after everything above is solid)

- [x] **Zero dead-ends** in non-perfect mode — the example above hit 0
      dead-ends on this seed; braiding aims for this but isn't a hard
      guarantee on every seed/size, so re-check on a few different seeds
      if you want to claim this bonus with confidence.
- [x] **Multiple algorithms** — two solving algorithms are supported
      (`ALGORITHM=BFS`/`ASTAR`). (Generation itself only has one algorithm,
      Recursive Backtracker — if you want the generation-side bonus too,
      that's still open.)
- [x] **Animation** — `ANIMATE=True` animates both generation and the
      final path reveal.

### Chapter IX — Submission

- [ ] Double-check every filename against the subject one more time
      (`a_maze_ing.py` exact name, `mazegen-*` package, `LICENSE.md`,
      `README.md`, `config.txt` all at the repo root).
- [ ] Be ready to make a small live code change during evaluation and
      explain any part of the codebase on the spot — the loop-rank check
      in `generator.py` and the "42" placement search in `utils.py` are
      the two most likely "why does this work" questions.

---

## Part 3 — Reusable verification script

Copy-paste this into a file (or a Python REPL) to re-run the coherence /
spanning-tree / loop-count / 3×3 checks against *any* `maze.txt` this
project produces:

```python
import sys

def load(path):
    with open(path) as f:
        content = f.read()
    rows_part, rest = content.split("\n\n", 1)
    rows = rows_part.split("\n")
    entry, exit_, path_str = rest.strip("\n").split("\n")
    return rows, entry, exit_, path_str

def bits(h):
    return int(h, 16)

def check(path, min_loops=2):
    rows, entry, exit_, path_str = load(path)
    W, H = len(rows[0]), len(rows)

    bad = 0
    for y in range(H):
        for x in range(W):
            v = bits(rows[y][x])
            east, south = (v >> 1) & 1, (v >> 2) & 1
            if x + 1 < W and east != (bits(rows[y][x + 1]) >> 3) & 1:
                bad += 1
            if y + 1 < H and south != bits(rows[y + 1][x]) & 1:
                bad += 1

    nodes = edges = 0
    for y in range(H):
        for x in range(W):
            v = bits(rows[y][x])
            if v == 0xF:
                continue
            nodes += 1
            east, south = (v >> 1) & 1, (v >> 2) & 1
            if not east and x + 1 < W and bits(rows[y][x + 1]) != 0xF:
                edges += 1
            if not south and y + 1 < H and bits(rows[y + 1][x]) != 0xF:
                edges += 1
    loops = edges - nodes + 1

    def open_e(x, y):
        return not (bits(rows[y][x]) >> 1) & 1

    def open_s(x, y):
        return not (bits(rows[y][x]) >> 2) & 1

    found_3x3 = False
    for top in range(H - 2):
        for left in range(W - 2):
            if any(bits(rows[yy][xx]) == 0xF
                   for yy in range(top, top + 3)
                   for xx in range(left, left + 3)):
                continue
            fully_open = all(
                (xx + 1 >= left + 3 or open_e(xx, yy))
                and (yy + 1 >= top + 3 or open_s(xx, yy))
                for yy in range(top, top + 3)
                for xx in range(left, left + 3)
            )
            if fully_open:
                found_3x3 = True

    print(f"grid: {W}x{H}")
    print(f"wall coherence mismatches: {bad} (must be 0)")
    print(f"nodes={nodes} edges={edges}")
    print(f"  -> if PERFECT=True, expect edges == nodes-1 "
          f"({edges == nodes - 1})")
    print(f"  -> if PERFECT=False, expect independent loops "
          f"(edges-nodes+1={loops}) >= MIN_LOOPS ({min_loops})")
    print(f"any fully-open 3x3 block: {found_3x3} (must be False)")
    print(f"entry={entry} exit={exit_} path_len={len(path_str)}")


if __name__ == "__main__":
    check(sys.argv[1], min_loops=int(sys.argv[2]) if len(sys.argv) > 2 else 2)
```

Usage: `python3 verify_output.py maze.txt 2`

---

*This file is a personal pre-submission aid and is not part of the graded
deliverable — feel free to delete it, or keep it in the repo, as you
prefer.*
