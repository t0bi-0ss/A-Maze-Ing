# Maze Generator Module (`mazegen.py`)

## Overview
The `MazeGenerator` class generates and manages a maze instance with configurable generation rules. It supports the growing tree (`gt`), recursive backtracking, and Prim's algorithms. These algorithms maintain active visited cells, select a cell according to their strategy, and carve passages to unvisited neighbors. A fixed 42 center pattern is applied to the maze when it is large enough. A collision checker ensures the entry and exit coordinates do not overlap these fixed pattern cells.

By default, imperfect mazes are created by running `open_dead_end_passage()` after the initial generation. This function searches for dead ends (cells with 3 walls) and attempts to delete the middle wall; if impossible, it randomly deletes one of the remaining two side walls. Path solutions are computed using a Dijkstra implementation.

---

## 1. Instantiation and Basic Usage

Import `MazeGenerator`, create a validated configuration, and iterate through
`gen_maze()` to complete generation. The generator yields the current maze
state after each generation step, so it can also be used to visualize progress.

```python

from mazegen import MazeGenerator

# Instantiate with default settings
generator = MazeGenerator()

# gen_maze yields the maze state progressively; exhaust it to finish generation
for state in generator.gen_maze():
    pass
```

---

## 2. Configuration Parameters

Pass custom parameters during initialization. Pydantic validates the
configuration before the maze is created: `width` and `height` must be between
3 and 60, and `entry` and `exit` must be different coordinates inside the
maze. Coordinates use `(row, column)` order.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | `3` | Maze width in cells. |
| `height` | `int` | `3` | Maze height in cells. |
| `entry` | `tuple[int, int]` | `(0, 0)` | Entrance coordinate `(row, column)`. |
| `exit` | `tuple[int, int]` | `(2, 2)` | Exit coordinate `(row, column)`. |
| `output_file` | `str` | `maze.txt` | Output filename configuration, 5-260 characters. |
| `perfect` | `bool` | `False` | Keep the generated maze perfect when `True`; otherwise open dead ends. |
| `seed` | `str \| int \| float \| None` | random value | Seed used for reproducible generation. |
| `algorithm` | `str` | `gt` | Generation algorithm: `gt`, `backtracking`, or `prims`. |
| `pcentered` | `bool` | `True` | Keep the fixed center pattern centered when it is applied. |

Boolean options also accept the strings `true`, `false`, `yes`, `no`, `1`, and `0`.
Calling `str(generator)` returns a readable summary of the validated configuration.

```python

# Custom configuration

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42,
    algorithm="backtracking",
    pcentered=False
)
for state in generator.gen_maze():
    pass
```

---

## 3. Accessing Structure and Solution

### Access the Grid Structure
After generation, `generator.maze` contains a flat, row-major list of
`MazeCell` objects. Each cell starts with all four walls (`walls = 15`) and
uses a bitmask for its current walls: `1` north, `2` east, `4` south, and `8`
west. The `static` flag identifies cells belonging to the fixed center pattern.

```python

# Access the list of MazeCell objects

maze_data = generator.maze

for cell in maze_data:
    print(f"Index: {cell.INDEX} | Walls: {cell.walls} | Static: {cell.static}")
```

### Access the Solution
Use the exported Dijkstra pathfinder after generation. It returns a string of
direction characters describing a route from `entry` to `exit`.

```python

from mazegen import path_finder

# The pathfinder expects the generated cells, both coordinates, and maze width
path = path_finder(generator.maze, generator.entry, generator.exit, generator.width)
print("Path from entry to exit:")
print(path)
```