.PHONY: install run debug lint lint-strict test build clean re

POETRY := poetry
PYTHON := $(POETRY) run python
MAIN   := a_maze_ing.py
CONFIG := config.txt

MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
              --ignore-missing-imports --disallow-untyped-defs \
              --check-untyped-defs

install:
	$(POETRY) install

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . $(MYPY_FLAGS)

lint-strict:
	$(POETRY) run flake8 .
	$(POETRY) run mypy mazegen $(MAIN) --strict

test:
	$(POETRY) run pytest tests/ -v

build:
	$(POETRY) build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info

re: clean install
