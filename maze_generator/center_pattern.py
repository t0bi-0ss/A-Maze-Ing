"""Utilities for placing the fixed center pattern in the maze."""

import random

from .mazecell import Maze

from .directions import Directions, get_neighbors_index

from time import sleep


def _locate_center(
        maze_width: int, maze_height: int, rng: random.Random
) -> int:
    """Choose the central cell index for the fixed pattern.

    Args:
        maze_width: Width of the maze.
        maze_height: Height of the maze.
        rng: Random generator used to break ties for even-sized dimensions.

    Returns:
        The center cell index closest to the intended maze midpoint.
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
    """Mark a contiguous sequence of cells as static.

    Args:
        maze: Maze grid being updated.
        maze_width: Width of the maze.
        starting_index: First cell index for the sequence.
        dir: Direction of traversal for the sequence.
        cells_number: Number of cells to mark.

    Returns:
        The index of the last marked cell.
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
    """Place the "four" segment of the center pattern in the maze."""

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
    """Place the "two" segment of the center pattern in the maze."""

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
    """Set the fixed 42 center pattern when the maze is large enough.

    Args:
        maze: Maze grid to decorate.
        maze_width: Width of the maze.
        maze_height: Height of the maze.
        perfect_centered: Whether to enforce a centered layout.
        rng: Random generator used for center placement.
    """

    if maze_width < 9 or maze_height < 8:
        print("ERROR: maze is not big enough to hold the '42' pattern")
        sleep(1)
        return
    if (maze_width % 2 == 0 or maze_height % 2 == 0) and perfect_centered:
        print(
            "ERROR: either width or center is not odd so '42' could not be"
            " perfectly centered"
        )
        sleep(1)
        return
    maze_center_index = _locate_center(maze_width, maze_height, rng)
    two_starting_index = maze_center_index - maze_width * 2 + 1
    four_starting_index = maze_center_index - maze_width * 2 - 3
    _set_two_pattern(maze, maze_width, two_starting_index)
    _set_four_pattern(maze, maze_width, four_starting_index)
