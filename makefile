MAIN_SCRIPT = main.py
WHL_FILE = maze_generator-1.0-py3-none-any.whl
CONFIG_FILE = config.txt

.PHONY: install run debug clean lint lint-strict run-poetry

install:
	pip install -r requirements.txt
	pip install $(WHL_FILE)

run:
	@test -n "$(CONFIG_FILE)" || (echo "Error: Specify a file with 'CONFIG_FILE=path/to/file'" && exit 1)
	python $(MAIN_SCRIPT) $(CONFIG_FILE)

run-poetry:
	@test -n "$(CONFIG_FILE)" || (echo "Error: Specify a file with 'CONFIG_FILE=path/to/file'" && exit 1)
	poetry install
	poetry run python $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	python -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 --ignore=0,W503,W504 .
	mypy . --strict