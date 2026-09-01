import sys

from maze_generator import MazeGenerator

from helper_f import get_pos, to_hex

from time import sleep

import path_finder


def transcripter(maze_generator: MazeGenerator):
    """
    Transcripts all MazeCell's walls value in maze into a text file
    while converting said values to hexadecimal
    """

    # Pass maze values
    counter = 1
    res = ""

    for cell in maze_generator.maze:
        res += to_hex(cell.walls)
        if counter == maze_generator.WIDTH and cell != maze_generator.maze[-1]:
            counter = 1
            res += "\n"
            continue
        counter += 1

    # Pass entry and exit
    res += "\n\n"
    entry = get_pos(maze_generator.ENTRY)
    exit = get_pos(maze_generator.EXIT)
    res += f"{entry}\n"
    res += f"{exit}\n"

    # Pass solution
    solution = path_finder.path_finder(
                                    maze_generator.maze,
                                    maze_generator.ENTRY,
                                    maze_generator.EXIT,
                                    maze_generator.WIDTH
                                )
    res += solution

    try:
        with open(maze_generator.OUTPUT_FILE, 'w') as f:
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
        print(f'Content saved to "{maze_generator.OUTPUT_FILE}"')
        sleep(2)
