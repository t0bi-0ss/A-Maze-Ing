# Maze Generator Module (`maze_generator.py`)

## Overview
The `MazeGenerator` class generates and manages a maze instance with configurable generation rules. Mazes are built using the growing tree algorithm. This algorithm maintains a set of active visited cells, selects one based on a strategy, and carves a passage to an unvisited neighbor. A fixed 42 center pattern is applied to the maze when it is large enough. A collision checker ensures the entry and exit coordinates do not overlap these fixed pattern cells. 

By default, imperfect mazes are created by running `open_dead_end_passage()` after the initial generation. This function searches for dead ends (cells with 3 walls) and attempts to delete the middle wall; if impossible, it randomly deletes one of the remaining two side walls. Path solutions are computed using a Dijkstra implementation.

---

## 1. Instantiation and Basic Usage

Import the `MazeGenerator` class, create an instance, and iterate through the `gen_maze()` generator to process the maze generation steps.

```
python

from maze_generator import MazeGenerator

# Instantiate with default settings
generator = MazeGenerator()

# gen_maze yields the maze state progressively; exhaust it to finish generation
for state in generator.gen_maze():
    pass
```

---

## 2. Custom Parameters

Pass custom parameters during initialization to control grid dimensions, start/end positions, and random seeding.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | `3` | Maze width in cells. |
| `height` | `int` | `3` | Maze width in cells. |
| `seed` | `int` / `None` | `None` | Seed for reproducible generation. |
| `start` | `tuple(int, int)` | `(0, 0)` | Starting coordinate `(row, col)`. |
| `end` | `tuple(int, int)` | `(2, 2)` | Ending coordinate `(row, col)`. |
| `selector` | `float` | `-1` | Growth strategy selector for the generator. |
| `perfect` | `bool` | `False` | Wether to keep the maze fully perfect. |
| `seed` | `any` | `None` | Random seed for reproducible generation. |
| `perfect_centered` | `bool` | `True` | Whether the fixed center pattern should stay centered. |
| `output_file` | `str` | `maze.txt` | File path used when exporting the maze. |


```
python

# Custom configuration

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42
)
for state in generator.gen_maze():
    pass
```

---

## 3. Accessing Structure and Solution

### Access the Grid Structure
The generated maze is accessible via the maze attribute as a flat, row-major list of MazeCell objects[cite: 1]. Each cell utilizes a bitmask (walls = 15) for its wall configuration. Walls are removed using bitwise XOR operations (1=North, 2=East, 4=South, 8=West).

```
python

# Access the list of MazeCell objects

maze_data = generator.maze

for cell in maze_data:
    print(f"Index: {cell.INDEX} | Walls: {cell.walls} | Static: {cell.static}")
```

### Access the Solution
Retrieve sequence of direction characters describing a valid route from `entry` to `exit` by applying the external Dijkstra pathfinder implementation to the generated maze structure.

```
python

from maze_generator import path_finder

# The Dijkstra pathfinder processes the generated maze data

path = path_finder(generator.maze, generator.ENTRY, generator.EXIT, generator.width)
print("Path from entry to exit:")
print(path)
```