"""Export maze state and solution data to a text file."""

import sys

from maze_generator import MazeGenerator, path_finder

from helper_f import to_hex

from time import sleep


def transcripter(maze: MazeGenerator) -> None:
    """Write the maze layout, entry and exit, and solution to an output file.

    Args:
        maze: Maze generator instance containing the maze to export.
    """

    # Pass maze values
    counter = 1
    res = ""

    for cell in maze.maze:
        res += to_hex(cell.walls)
        if counter == maze.WIDTH and cell != maze.maze[-1]:
            counter = 1
            res += "\n"
            continue
        counter += 1

    # Pass entry and exit
    res += "\n\n"
    res += f"{maze.ENTRY}\n"
    res += f"{maze.EXIT}\n"

    # Pass solution
    solution = path_finder(
        maze.maze,
        maze.ENTRY,
        maze.EXIT,
        maze.WIDTH
    )
    res += solution

    try:
        with open(maze.OUTPUT_FILE, 'w') as f:
            f.write(res)
    except (
            UnicodeDecodeError,
            ValueError,
            OSError,
            PermissionError,
            IsADirectoryError,
            FileNotFoundError,
    ) as msg:
        print(msg)
        sys.exit()
    else:
        print(f'Content saved to "{maze.OUTPUT_FILE}"')
        sleep(2)
