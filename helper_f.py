"""
Utility helpers for maze generation, configuration loading, and route display.
"""

import subprocess
import maze_visualizer
import maze_generator
import random
from time import sleep
import parser
import sys
import helper_f
from collections import deque


def to_hex(num: int) -> str:
    """Convert a numeric wall mask to its hexadecimal character representation.

    Args:
        num: Integer value from 0 to 15 representing maze wall bits.

    Returns:
        The hexadecimal digit as a string, or the original value as a string.
    """
    match num:
        case 10:
            return 'a'
        case 11:
            return 'b'
        case 12:
            return 'c'
        case 13:
            return 'd'
        case 14:
            return 'e'
        case 15:
            return 'f'
        case _:
            return str(num)


def plot_route(start: tuple[int, int], steps: str) -> list[tuple[int, int]]:
    """
    Build a coordinate path from a starting position following directional
    steps.

    Args:
        start: Initial maze position as ``(row, col)``.
        steps: A string containing movement directions such as ``N``, ``E``,
        ``S``, and ``W``.

    Returns:
        A list of visited coordinates including the starting cell.
    """
    route_coordinates = [start]
    f, c = start

    movements = {
        'E': (0, 1),
        'W': (0, -1),
        'S': (1, 0),
        'N': (-1, 0)
    }

    for step in steps.upper():
        if step in movements:
            df, dc = movements[step]
            f += df
            c += dc
            route_coordinates.append((f, c))

    return route_coordinates


def clear() -> None:
    """Clear the terminal screen."""
    subprocess.run(['clear'])


def matrix_converter(maze: maze_generator.Maze, width: int) -> list[list[int]]:
    """Convert a flat maze representation into a row-wise matrix.

    Args:
        maze: A sequence of maze cells preserving row-major order.
        width: Number of cells per row.

    Returns:
        A 2D matrix of cell wall values grouped by row.
    """

    matrix = []
    row = []
    counter = 0

    for cell in maze:
        row.append(cell.walls)
        counter += 1
        if counter == width:
            matrix.append(row)
            row = []
            counter = 0

    return matrix


def regenerate_maze(
        maze: maze_generator.MazeGenerator,
        new_maze: bool = False
) -> None:
    """
    Regenate a maze, optionally setting a new seed
    """

    # New maze?
    if new_maze:
        maze.SEED = random.random()

    # Restart maze
    maze.maze = [
        maze_generator.MazeCell(element_num) for element_num
        in range(0, maze.WIDTH * maze.HEIGHT)
    ]

    # Restart rng
    maze.rng = random.Random(maze.SEED)

    # Set pattern
    maze_generator.pattern(
        maze.maze,
        maze.WIDTH,
        maze.HEIGHT,
        maze.PCENTERED,
        maze.rng
    )

    # Check for colition
    maze_generator.colition_checker(
        maze.maze,
        maze.ENTRY,
        maze.EXIT,
        maze.WIDTH
    )

    # Restart generator
    maze.generator = maze.gen_maze


def maze_rendering(
        maze: maze_generator.MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer,
        show_path: bool = False,
        animated: bool = False,
) -> None:
    """Regenerate and render a maze, optionally with animation.

    Args:
        animated: Whether to animate the maze generation process.
        maze: Maze generator instance being rebuilt.
        visualizer: Visualizer used to render the generated maze.
    """

    # Show path?
    if show_path:
        visualizer.show_path = True
    else:
        visualizer.show_path = False

    if animated:
        try:
            for frame in maze.generator():
                clear()
                visualizer.render_ascii(
                    maze=maze.maze,
                    width=maze.WIDTH
                )
                sleep(.05)
        except KeyboardInterrupt:
            print("\nMaze generation interrupted")
            sys.exit()
    else:

        deque(maze.generator(), maxlen=0)
        clear()
        visualizer.render_ascii(
            maze=maze.maze,
            width=maze.WIDTH
        )


def define_selector(algorithm: str) -> int:
    """Map a maze-generation algorithm name to its selection integer.

    Args:
        algorithm: Algorithm identifier such as ``gt``, ``prism``, or
            ``backtracking``.

    Returns:
        The selector value used by the generation algorithm.
    """

    match algorithm:
        case "gt":
            res = -1
        case "prism":
            res = 1
        case "backtracking":
            res = 0
    return res


def load_config(
        file_name: str
) -> maze_generator.MazeGenerator:
    """Build a maze generator from a configuration file.

    Args:
        file_name: Path to the maze configuration file.

    Returns:
        A configured ``MazeGenerator`` instance.
    """

    try:
        configuration = parser.get_config(file_name)
    except SystemExit as msg:
        print(msg)
        sys.exit()
    else:
        maze = maze_generator.MazeGenerator(
            width=configuration.width,
            height=configuration.height,
            entry=configuration.entry,
            exit=configuration.exit,
            perfect=configuration.perfect,
            seed=configuration.seed,
            perfect_centered=configuration.perfect_centered,
            selector=helper_f.define_selector(configuration.algorithm),
            output_file=configuration.output_file
        )
    return maze
