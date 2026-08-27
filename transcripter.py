import sys

from maze_generator import Maze


def transcripter(maze: Maze, output_file_name: str, solution: str = None):
    """
    Transcripts all MazeCell's walls value in maze into a text file
    while converting said values to hexadecimal
    """

    def to_hex(num):
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
    res += f"{maze.ENTRY[0]},{maze.ENTRY[1]}\t\t# entry\t(x,y)\n"
    res += f"{maze.EXIT[0]},{maze.EXIT[1]}\t\t# exit\t(x,y)\n"

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
