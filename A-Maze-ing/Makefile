.PHONY: install run debug lint lint-strict test build clean re

POETRY := poetry
PYTHON := $(POETRY) run python
MAIN   := a_maze_ing.py
CONFIG := config.txt

# Exact flags required by the subject (III.2/III.3) for the mandatory
# `lint` target - the grader's Moulinette runs the same commands, so
# loosening them locally only hides errors from us, not from evaluation.
MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
              --ignore-missing-imports --disallow-untyped-defs \
              --check-untyped-defs

install:
	$(POETRY) install

run:
	$(PYTHON) $(MAIN) $(CONFIG)

# Drops into pdb at the first line of the program, per the subject's
# requirement to run the main script in debug mode.
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . $(MYPY_FLAGS)

# Optional stricter check (III.2). Not required to pass, but worth
# running before submission to catch anything the relaxed flags miss.
lint-strict:
	$(POETRY) run flake8 .
	$(POETRY) run mypy mazegen $(MAIN) --strict

test:
	$(POETRY) run pytest tests/ -v

# Rebuilds the reusable mazegen-*.whl/.tar.gz and copies it to the repo
# root, since the subject requires the package file to live there (not
# just in dist/).
build:
	$(POETRY) build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info

re: clean install
