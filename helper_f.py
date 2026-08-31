import subprocess
import maze_visualizer
import maze_generator
import random


def get_pos(dir: tuple[str, str]) -> str:

    res = str(dir[0]).replace(' ', '') + ',' + str(dir[1]).replace(' ', '')
    return res


def convert_pos(dir: tuple[str, str]) -> tuple[int, int]:
    """
    Converts terminal points to a tuple of ints
    """

    return int(dir[0]), int(dir[1])


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


def plot_route(start: tuple[int, int], steps: str) -> list[tuple[int, int]]:
    """Take the start and go for the end with the route"""
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
    subprocess.run(['clear'])


def matrix_converter(maze: list[int], width: int) -> list[list[int]]:
    """
    Converts generator's one dimensional matrix to a two dimensional one, while
    converting each cells value to hexadecimal
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


def visualize_generation(
        animated: int,
        maze: maze_generator.MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer
) -> None:
    """
    In charge of generating a maze and it's visualization
    """

    # Restart maze
    maze.maze = [maze_generator.MazeCell(element_num) for element_num
                 in range(0, maze.WIDTH * maze.HEIGHT)]

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

    # Restart generator
    maze.generator = maze.gen_maze

    if animated:
        for frame in maze.generator():
            clear()
            converted_matrix = matrix_converter(frame, maze.WIDTH)
            visualizer.render_ascii(converted_matrix)
    else:
        from collections import deque

        deque(maze.generator(), maxlen=0)
        converted_matrix = matrix_converter(
            maze.maze, maze.WIDTH
            )
        clear()
        visualizer.render_ascii(converted_matrix)
