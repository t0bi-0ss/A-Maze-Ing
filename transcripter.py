import sys

from maze_generator import Maze

from helper_f import get_pos, to_hex


def transcripter(maze: Maze, output_file_name: str, solution: str = None):
    """
    Transcripts all MazeCell's walls value in maze into a text file
    while converting said values to hexadecimal
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
    entry = get_pos(maze.ENTRY)
    exit = get_pos(maze.EXIT)
    res += f"{entry}\t\t# entry\t(x,y)\n"
    res += f"{exit}\t\t# exit\t(x,y)\n"

    # Pass solution
    if solution:
        res += solution

    try:
        with open(output_file_name, 'w') as f:
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
