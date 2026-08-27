import random

from .mazecell import Maze

from .directions import Directions, get_neighbors_index


def _locate_center(
        maze_width: int, maze_height: int, rng: random.Random
) -> int:
    """
    Locates maze's most approximate center
    """

    possible_indexes = []
    if maze_width % 2 != 0 and maze_height % 2 != 0:
        return (maze_height // 2) * maze_width + (maze_width // 2)
    if maze_width % 2 == 0 and maze_height % 2 != 0:
        left_center_index = (maze_height // 2) * \
            maze_width + (maze_width // 2 - 1)
        right_center_index = (maze_height // 2) * \
            maze_width + (maze_width // 2)
        possible_indexes.append(left_center_index)
        possible_indexes.append(right_center_index)
        return rng.choice(possible_indexes)
    if maze_width % 2 != 0 and maze_height % 2 == 0:
        top_center_index = ((maze_height // 2) - 1) \
            * maze_width + (maze_width // 2)
        bottom_center_index = (maze_height // 2) \
            * maze_width + (maze_width // 2)
        possible_indexes.append(top_center_index)
        possible_indexes.append(bottom_center_index)
        return rng.choice(possible_indexes)
    if maze_width % 2 == 0 and maze_height % 2 == 0:
        rows = [maze_height // 2 - 1, maze_height // 2]
        cols = [maze_width // 2 - 1, maze_width // 2]
        return rng.choice(rows) * maze_width + rng.choice(cols)


def _set_static_sequence(
        maze: Maze,
        maze_width: int,
        starting_index: int,
        dir: Directions,
        cells_number: int
) -> None:
    """
    Sets a number of cells to static in a specific direction and returns last
    index in the sequence
    """

    current_index = starting_index
    maze[current_index].is_now_static()
    for i in range(0, cells_number - 1):
        current_index = get_neighbors_index(current_index, dir, maze_width)
        maze[current_index].is_now_static()
    return current_index


def _set_four_pattern(
        maze: Maze, maze_width: int, starting_index: int
) -> None:
    """Sets the 'four' on the '42' pattern"""

    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )


def _set_two_pattern(maze: Maze, maze_width: int, starting_index: int) -> None:
    """
    Sets the 'two' on the '42' pattern
    """

    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the left
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.WEST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )


def pattern(
        maze: Maze,
        maze_width: int,
        maze_height: int,
        perfect_centered: bool,
        rng: random.Random
        ) -> None:
    """Sets '42' pattern in the maze if possible"""

    if maze_width < 9 or maze_height < 8:
        print("ERROR: maze is not big enough to hold the '42' pattern")
        return
    if (maze_width % 2 == 0 or maze_height % 2 == 0) and perfect_centered:
        print(
            "ERROR: either width or center is not odd so '42' could not be"
            " perfectly centered"
        )
        return
    maze_center_index = _locate_center(maze_width, maze_height, rng)
    two_starting_index = maze_center_index - maze_width * 2 + 1
    four_starting_index = maze_center_index - maze_width * 2 - 3
    _set_two_pattern(maze, maze_width, two_starting_index)
    _set_four_pattern(maze, maze_width, four_starting_index)
