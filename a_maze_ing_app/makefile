MAIN_SCRIPT = a_maze_ing.py
MAZEGEN_PATH = ../mazegen
CONFIG_FILE = config.txt

.PHONY: install run debug clean lint lint-strict run-poetry

install:
	pip install -r requirements.txt
	pip install $(MAZEGEN_PATH)

run:
	@test -n "$(CONFIG_FILE)" || (echo "Error: Specify a file with 'CONFIG_FILE=path/to/file'" && exit 1)
	python3 $(MAIN_SCRIPT) $(CONFIG_FILE)

run-poetry:
	@test -n "$(CONFIG_FILE)" || (echo "Error: Specify a file with 'CONFIG_FILE=path/to/file'" && exit 1)
	poetry install
	poetry run python3 $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	python3 -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	find ../. -type d -name "__pycache__" -exec rm -rf {} +
	find ../. -type d -name ".mypy_cache" -exec rm -rf {} +
	find ../. -type f -name "poetry.lock" -exec rm -rf {} +

lint:
	flake8 --exclude=__pycache__,.venv,maze_analyzer.py ../.
	mypy ../. --exclude '(__pycache__|\.venv|maze_analyzer\.py)' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 --ignore=0,W503,W504 --exclude=__pycache__,.venv,maze_analyzer.py ../.
	mypy ../. --exclude '(__pycache__|\.venv|maze_analyzer\.py)' --strict