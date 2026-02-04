# Makefile for A-Maze-Ing Python project

# Default config file for run/debug
CONFIG ?= config.txt

# Install project dependencies
install:
	pip install -r requirements.txt

# Run the main script
run:
	python3 a_maze_ing.py $(CONFIG)

# Run in debug mode with pdb
debug:
	python3 -m pdb a_maze_ing.py $(CONFIG)

# Clean temporary files and caches
clean:
	rm -rf __pycache__
	rm -rf mazegen/__pycache__
	rm -rf helpers/__pycache__
	rm -rf pathfinding/__pycache__
	rm -rf testing/__pycache__
	rm -rf .mypy_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf mazegen.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Lint with flake8 and mypy (required flags)
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Lint with strict mypy (optional but recommended)
lint-strict:
	flake8 .
	mypy . --strict

# Build the pip package
build:
	python3 -m build

# Install the package locally
install-package:
	pip install dist/mazegen-1.0.0-py3-none-any.whl

.PHONY: install run debug clean lint lint-strict build install-package
