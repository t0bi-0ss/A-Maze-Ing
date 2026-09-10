*This project has been created as part of the 42 curriculum by tsordo-o, jvera-cr.*

# Table of contents
- [ꡙ‍ A-Maze-ing](#-a-maze-ing)
  - [📝 Description](#-description)
    - [🎯 Project Goal \& Overview](#-project-goal--overview)
    - [✨ Key \& Interesting Features](#-key--interesting-features)
  - [🛠️ Instructions](#️-instructions)
    - [📥 Installation \&\& Compilation](#-installation--compilation)
      - [🛠️ Alternative with Poetry](#️-alternative-with-poetry)
    - [🖥️ Interactive menu](#️-interactive-menu)
  - [📝 Resources](#-resources)
    - [References](#references)
    - [AI Usage](#ai-usage)
  - [⚙️ Structure and format of our config file](#️-structure-and-format-of-our-config-file)
  - [🧠 Maze Generation: Selected Algorithms \& Rationale](#-maze-generation-selected-algorithms--rationale)
    - [⚙️ How the Algorithm Works](#️-how-the-algorithm-works)
    - [🎛️ Dual-Behavior Replication via Cell Selection](#️-dual-behavior-replication-via-cell-selection)
  - [📦 Code Reusability](#-code-reusability)
    - [Method 1: Standard Build (Manual)](#method-1-standard-build-manual)
    - [Method 2: Automated Build (Recommended)](#method-2-automated-build-recommended)
  - [🌀 Maze Generator Module (`maze_generator.py`)](#-maze-generator-module-maze_generatorpy)
    - [Overview](#overview)
    - [1. Instantiation and Basic Usage](#1-instantiation-and-basic-usage)
    - [2. Custom Parameters](#2-custom-parameters)
    - [3. Accessing Structure and Solution](#3-accessing-structure-and-solution)
      - [Access the Grid Structure](#access-the-grid-structure)
      - [Access the Solution](#access-the-solution)
  - [👥 Team \& Project Management](#-team--project-management)
    - [Member Roles](#member-roles)
    - [Project planning and evolution](#project-planning-and-evolution)
    - [Achievements and areas for improvement](#achievements-and-areas-for-improvement)
    - [Tools Used](#tools-used)

# $\color{red}{ꡙ‍}$ A-Maze-ing

## 📝 Description

**A-Maze-ing** is a random maze generator and viewer developed in Python.

### 🎯 Project Goal & Overview
The ultimate goal of this project is to take a set of constraints (dimensions, coordinates, generation mode) and build a structurally sound, fully interconnected maze without any isolated cells or broken logic. The generated output is securely encoded using **hexadecimal wall representations (4-bit masking)**, ensuring the file remains compact and readable by analysis scripts like the `maze_analyzer.py`.

### ✨ Key & Interesting Features
* **Dual Architecture Modes:** 
    * *Perfect Mazes:* Implements pure academic mazes with **exactly one unique path** between the entry and exit points (zero loops). 
    * *Playable Boards:* Shifts into a fully braided **Pac-Man-like gameplay board** featuring multiple independent loop routes, rare dead-ends, and explicitly open corners/centers for players and enemies.
* **The "42" Structural Signature:** As a clever nod to the 42 curriculum, the engine embeds a **hidden "42" pattern** built directly from fully enclosed walls rendering that only becomes visible during visual.
* **Interactive Control Center:** The viewer is not static. Users can dynamically **regenerate layouts on the fly, toggle the visual representation of the shortest path, and cycle through vibrant color palettes** for the walls.
* **Production-Ready Packaging:** Beyond a simple script, the generation logic is isolated into a standalone `mazegen-*` package architecture, ready to be built into standard `.whl` files and **distributed via pip** for future projects.

## 🛠️ Instructions

### 📥 Installation && Compilation
This project uses a `Makefile` to automate environment tasks:

_Note: We recommend running the commands in the order presented, to observe the flake8 and mypy validations in action._

* **To install project dependencies using pip:**

```bash
make install
```

* **To execute the commands flake8 . and mypy .:**

```bash
make lint
```

* **To execute the main script of our project:**
```bash
make run
```

* **To run the main script in debug mode using Python’s built-in debugger:**
```bash
make debug
```

* **To remove temporary files or caches (e.g., __pycache__, .mypy_cache) to
keep the project environment clean:**
```bash
make clean
```
 ⚠️ Important: It is highly recommended to keep the original file and folder structure intact. The project relies on relative paths to connect its components, so moving any element could break references and cause runtime errors.

#### 🛠️ Alternative with Poetry
Alternatively, the `make install` and `make run` workflows have been automated using **Python Poetry**, a modern tool for dependency management and Python project packaging:

* **To install dependencies and run the project using Poetry:**
```bash
make run-poetry
```

### 🖥️ Interactive menu

Once the dependencies are installed and the program is run, a maze with 9/10 options will be displayed, which are described below:

| Number | Name | Description |
|----|----|----|
| `1` | Toggle Animation. (Status OFF/ON) | It starts with the animation disabled; selecting this option will generate a maze animation the next time it is generated. |
| `2` | Re-generate maze | It generates the same maze again, useful if you want to see the animation, if you activated it previously. |
| `3` | Generate new maze | It generates a new maze, different from the previous one. |
| `4` | Show/Hide solution path | It starts with the solution path hidden; if this option is selected, it toggles between showing and not showing the solution path. |
| `5` | Next Color Combination | The colors of the maze are changed: Walls, blocks 42 and solution path. |
| `6` | Recover original maze | No matter how many times we have generated new mazes, with this option we will have the same maze that was generated when starting the program. |
| `7` | Generate output file | The current maze is saved in an output file with the name given in the `output_file` key within the `config.txt` file. |
| `8` | Re-load config | If you made changes to the `config.txt` file, you don't need to run the program again; just choose this option and the program will read the `config.txt` file again with the changes you made. |
| `9` | Switch Visualizer (Current: THICK/SLENDER) | Toggles between **THICK** (Minecraft-like solid blocks) and **SLENDER** (thin lines) maze display styles. |
| `10` | Select algorithm (Current: Growing Tree/ Prim's/ Backtracking) | Opens a submenu to choose the generation algorithm: **Prim's like**, **Backtracking like**, or **Growing Tree**. |
| `11` | Exit | The program closes by saving the current maze to a previously configured output file. |

ℹ️ Note: _If the generated maze exceeds the dimensions of your screen, you can reduce the zoom of the browser or terminal (usually with the key combination `Ctrl` + `-`) to view the complete structure correctly._

## 📝 Resources

### References
* **42 Peer-Learning** — Collaborated with colleagues.
* [Maze Generation Algorithms - An Exploration](https://professor-l.github.io/mazes/) — An excellent visual and theoretical guide on the behavior and implementation of 10 perfect maze generation algorithms (such as *Randomized Depth-First Search*, *Prim* and *Kruskal*).
* [Terminal ASCII rendering and codes ASCII](https://elcodigoascii.com.ar/) — Extended ASCII codes were used to form the mazes.
* [Choose an open source license](https://choosealicense.com/) — To choose and write the license that allows code reuse.

### AI Usage

In compliance with the project guidelines, Artificial Intelligence tools were utilized exclusively for the following tasks:
* **Documentation Standardization:** Automated generation and formatting of *docstrings* across all project modules, ensuring strict adherence to **PEP 257** style conventions.
* **Conceptual Research & Algorithm Analysis:** Assisted in researching mathematical concepts and clarifying the underlying logic of the implemented maze-generation algorithms.
* **README Structuring:** Helped organize, format, and refine the layout of the project's documentation for better readability.

## ⚙️ Structure and format of our config file

As previously described, there is a configuration file, `config.txt`, that allows customization of the maze generation. Its keys and possible configurations are described below:

```ini
WIDTH=20                # Maze width (number of cells, minimun 3 & maximum 60)
HEIGHT=15               # Maze height (Minimun 3 & maximum 60)
ENTRY=0,0               # Entry coordinates (x,y)
EXIT=19,14              # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt    # Output file name (hexadecimal format)
PERFECT=True            # True for perfect maze / False for Pac-Man mode
```

We also have 3 additional keys:

```ini
SEED=12345             # Seed for reproducible generation (optional)
ALGORITHM=gt           # Generation algorithm (prim, backtracking, gt)
PERFECT_CENTERED=True  # Forces exact centering of the "42" logo or raises a controlled error. For default this value is True.
```

ℹ️ **Note:** The configuration parser is highly flexible and includes the following features:

* **Separators:** It accepts both the equals sign (`=`) and the colon (`:`) as valid key-value separators.
* **Case Insensitivity:** Keys are **case-insensitive**, meaning `WIDTH`, `width`, and `Width` are all recognized as the exact same configuration key.
* **Comment Lines:** Comments can only be placed on standalone lines and must start with either a hash character (`#`) or a semicolon (`;`) as the **leading** character. Inline or trailing comments after a key-value pair are not allowed.
* **Whitespace Robustness:** It automatically strips any **leading** or **trailing** whitespace from both keys and values, preventing accidental parsing errors.
* **Maze Display Rule**: If the PERFECT_CENTERED flag is disabled, the maze will not be displayed by default unless specific parameters are provided to achieve a perfect center alignment.

Therefore, the following formats are completely valid:

```ini
; This is a valid comment line
# This is also a valid comment line
WIDTH=20
WIDTH   :   20   
```

The "42" pattern is not be to show if the width is minor of 9 and the height is minor of 8.

## 🧠 Maze Generation: Selected Algorithms & Rationale

The primary algorithm selected to power this project is the **Growing Tree** algorithm. 

The choice of this algorithm is highly justified as it serves as an excellent architectural case study: it demonstrates how altering internal cell-selection logic completely mutates a system's behavior and maze aesthetics **without altering the core logic of the program**. By leveraging **Growing Tree**, the program can dynamically replicate both **Prim's** and **Backtracking** algorithms at the user's command.

### ⚙️ How the Algorithm Works

The core process relies on iteratively managing an **active list of cells ($C$)** to carve out paths through the grid:

1. **Initialization:** An empty list $C$ is created. A starting cell is chosen at random from the grid, marked as visited, and added to $C$.
2. **Selection:** While the list $C$ is not empty, a cell is selected from it based on a specific, configurable rule.
3. **Expansion:** If the selected cell has unvisited neighbors:
   * One of those neighbors is chosen at random.
   * The wall between the current cell and the chosen neighbor is removed.
   * The neighbor is marked as visited and added to the list $C$.
4. **Removal:** If the selected cell has no unvisited neighbors, it is removed from the list $C$.
5. **Repetition:** Steps 2 through 4 repeat sequentially until the active list $C$ becomes completely empty.

### 🎛️ Dual-Behavior Replication via Cell Selection

The visual aesthetic and structural behavior of the generated maze change radically depending on the selection criteria used in **Step 2**:

* **Backtracking Mode (Always Newest):** By always selecting the most recently added cell (**LIFO** / Stack behavior), the algorithm acts exactly like a *Recursive Backtracker* (Randomized Depth-First Search). This yields long, winding, and snake-like corridors with very few branches.
* **Prim's Mode (Always Random):** By choosing a cell completely at **random** from the active set, the system mutates into *Prim's Algorithm*. This prioritizes radial expansion, resulting in a fractured layout with countless short branches and dead-ends.
* **Hybrid Mode (Native Growing Tree):** A parametric approach combining both strategies, allowing the generation of custom hybrid mazes.


## 📦 Code Reusability

The core generation logic is completely isolated within the distributable package **`mazegen`**, located at the repository root. This module generates `.whl` (Wheel) files that can be easily installed in any Python environment using `pip`.

There are two ways to build the module and generate the `.whl` file:

### Method 1: Standard Build (Manual)
Run the standard Python build command:
```bash
python3 -m build --wheel
```
* **Result:** This generates a set of temporary build directories. You will find the final `.whl` file inside the `dist/` folder.

### Method 2: Automated Build (Recommended)
We have automated the entire build lifecycle using `taskipy`. Simply run this:
```bash
task build
```
* **Result:** This command automatically cleans up any previous build artifacts, compiles the package, moves the resulting `.whl` file , and safely removes all temporary directories (`build/`, `dist/`, `.egg-info`).


## 🌀 Maze Generator Module (`maze_generator.py`)

### Overview
The `MazeGenerator` class generates and manages a maze instance with configurable generation rules. Mazes are built using the growing tree algorithm. This algorithm maintains a set of active visited cells, selects one based on a strategy, and carves a passage to an unvisited neighbor. A fixed 42 center pattern is applied to the maze when it is large enough. A collision checker ensures the entry and exit coordinates do not overlap these fixed pattern cells. 

By default, imperfect mazes are created by running `open_dead_end_passage()` after the initial generation. This function searches for dead ends (cells with 3 walls) and attempts to delete the middle wall; if impossible, it randomly deletes one of the remaining two side walls. Path solutions are computed using a Dijkstra implementation.

---

### 1. Instantiation and Basic Usage

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

### 2. Custom Parameters

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

### 3. Accessing Structure and Solution

#### Access the Grid Structure
The generated maze is accessible via the maze attribute as a flat, row-major list of MazeCell objects[cite: 1]. Each cell utilizes a bitmask (walls = 15) for its wall configuration. Walls are removed using bitwise XOR operations (1=North, 2=East, 4=South, 8=West).

```
python

# Access the list of MazeCell objects

maze_data = generator.maze

for cell in maze_data:
    print(f"Index: {cell.INDEX} | Walls: {cell.walls} | Static: {cell.static}")
```

#### Access the Solution
Retrieve sequence of direction characters describing a valid route from `entry` to `exit` by applying the external Dijkstra pathfinder implementation to the generated maze structure.

```
python

from maze_generator import path_finder

# The Dijkstra pathfinder processes the generated maze data

path = path_finder(generator.maze, generator.ENTRY, generator.EXIT, generator.width)
print("Path from entry to exit:")
print(path)
```

## 👥 Team & Project Management

### Member Roles
* **tsordo-o:** Lead developer of the maze generation algorithm and hexadecimal export logic.
* **jvera-cr:** Visual interface designer [ASCII Terminal], README and documentation.

### Project planning and evolution
Initially, the idea was to put an interactive menu with a tolerable number of options so as not to confuse the evaluator; however, as the project progressed, several more options were implemented with the aim of making it easier for the evaluator to test the project without closing the application.

### Achievements and areas for improvement
* **Achievements:** 
  * **Seamless Collaboration & Design:** The choice of a highly modular architecture allowed the team to integrate independent components smoothly.
  * **Advanced Type Safety:** Implementing type hints and robust data parsing libraries like `Pydantic` significantly reduced runtime errors and simplified configuration validation.
* **Areas for improvement:** 
  * **Time Management:** Allocating more dedicated, synchronous team sessions would enhance code-review efficiency.
  * **Python Mastery:** Further deepening our knowledge of advanced Python patterns and asynchronous workflows remains a key learning goal.
  * **Git & GitHub Collaboration:** Since one team member was solely responsible for managing the GitHub repository due to differing experience levels with version control, a key goal is to improve collaborative Git workflows in future projects.

### Tools Used
* **Dependency Management & Packaging:**
  * **Poetry:** Utilized as the modern packaging framework to securely bundle the core `mazegen` package into PEP-compliant `.whl` and `.tar.gz` distribution files.
* **Code Quality & Validation:**
  * **Configparser:** Utilized as the primary low-level parser to handle the initialization, reading, and extraction of the plain-text configuration files (`config.txt`).
  * **Pydantic:** Implemented for automated data parsing and strict type validation of the plain-text configuration files.
  * **Flake8 & Mypy:** Used to enforce maximum code compliance, static type safety (`--strict`), and adherence to 42's programming standards.
* **Debugging & Architecture:**
  * **Pdb (Python Debugger):** Integrated via the automation pipeline (`make debug`) for runtime inspection, state analysis, and step-by-step trace evaluation.
* **Version Control & Hosting:**
  * **Git & GitHub:** Maintained for single-manager repository deployment, release tracking, and codebase archiving.
