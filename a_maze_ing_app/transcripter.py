"""Export maze state and solution data to a text file."""

import sys

from mazegen import MazeGenerator, path_finder

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
        if counter == maze.width and cell != maze.maze[-1]:
            counter = 1
            res += "\n"
            continue
        counter += 1

    # Pass entry and exit
    res += "\n\n"
    res += f"{maze.entry}\n"
    res += f"{maze.exit}\n"

    # Pass solution
    solution = path_finder(
        maze.maze,
        maze.entry,
        maze.exit,
        maze.width
    )
    res += solution

    try:
        with open(maze.output_file, 'w') as f:
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
        print(f'Content saved to "{maze.output_file}"')
        sleep(2)
