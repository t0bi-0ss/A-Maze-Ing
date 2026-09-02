"""
Helpers to trim dead ends from the generated maze while preserving boundaries.
"""

from .mazecell import Maze, MazeCell

from .directions import Directions, validate_direction

import random

from .exceptions import InvalidDirection


def _count_walls(cell: MazeCell) -> int:
    """Count how many walls are still present in a cell.

    Args:
        cell: Maze cell to inspect.

    Returns:
        Number of active walls on the cell.
    """

    counter = 0
    walls = [1, 2, 4, 8]

    for wall in walls:
        if cell.walls & wall:
            counter += 1

    return counter


def _build_path(
        current_cell: MazeCell,
        neighbor_cell: MazeCell,
        dir: Directions
) -> None:
    """Open a passage between two adjacent cells in a chosen direction.

    Args:
        current_cell: The cell being modified.
        neighbor_cell: The adjacent cell to connect to.
        dir: Direction from the current cell to the neighbor.
    """

    match dir.value:
        case 'N':
            current_cell.del_north()
            neighbor_cell.del_south()
        case 'E':
            current_cell.del_east()
            neighbor_cell.del_west()
        case 'S':
            current_cell.del_south()
            neighbor_cell.del_north()
        case 'W':
            current_cell.del_west()
            neighbor_cell.del_east()
        case _:
            print("invalid direction")
            return


def _is_a_corner(maze: Maze, cell: MazeCell, width: int, height: int) -> int:
    """Check whether a cell is one of the maze's corners.

    Args:
        maze: Maze grid.
        cell: Cell to inspect.
        width: Maze width.
        height: Maze height.

    Returns:
        1 if the cell is a corner, otherwise 0.
    """

    # Top left corner
    if cell.INDEX == 0:
        _build_path(cell, maze[cell.INDEX + 1], Directions.EAST)
        _build_path(cell, maze[cell.INDEX + width], Directions.SOUTH)
        return 1
    # Top right corner
    elif cell.INDEX == width - 1:
        _build_path(cell, maze[cell.INDEX + width], Directions.SOUTH)
        _build_path(cell, maze[cell.INDEX - 1], Directions.WEST)
        return 1
    # Bottom left corner
    elif cell.INDEX == (height - 1) * width:
        _build_path(cell, maze[cell.INDEX + 1], Directions.EAST)
        _build_path(cell, maze[cell.INDEX - width], Directions.NORTH)
        return 1
    # Bottom right corner
    elif cell.INDEX == height * width - 1:
        _build_path(cell, maze[cell.INDEX - width], Directions.NORTH)
        _build_path(cell, maze[cell.INDEX - 1], Directions.WEST)
        return 1
    else:
        return 0


def _get_middle_direction(
        valid_directions_dict: dict[Directions, int]
) -> None:

    valid_directions_set = set(valid_directions_dict.keys())

    if not {Directions.NORTH, Directions.EAST, Directions.SOUTH}.difference(
        valid_directions_set
    ):
        del valid_directions_dict[Directions.NORTH]
        del valid_directions_dict[Directions.SOUTH]
    elif not {Directions.EAST, Directions.SOUTH, Directions.WEST}.difference(
            valid_directions_set
    ):
        del valid_directions_dict[Directions.EAST]
        del valid_directions_dict[Directions.WEST]
    elif not {Directions.SOUTH, Directions.WEST, Directions.NORTH}.difference(
            valid_directions_set
    ):
        del valid_directions_dict[Directions.SOUTH]
        del valid_directions_dict[Directions.NORTH]
    elif not {Directions.SOUTH, Directions.WEST, Directions.NORTH}.difference(
            valid_directions_set
    ):
        del valid_directions_dict[Directions.SOUTH]
        del valid_directions_dict[Directions.NORTH]


def _delete_walls(
        maze: Maze, cell: MazeCell, width: int, height: int, rng: random.Random
) -> None:
    """Remove a dead-end connection from a cell in random valid directions.

    Args:
        maze: Maze grid.
        cell: Current dead-end cell.
        width: Maze width.
        height: Maze height.
        rng: Random generator used to choose directions.
    """

    directions = [direction for direction in Directions]
    valid_directions_and_neighbor_index = {}

    for dir in directions:
        try:
            valid_index = validate_direction(
                cell.INDEX, dir, width, height
            )
        except InvalidDirection:
            continue
        else:
            valid_directions_and_neighbor_index[dir] = valid_index

    if not cell.walls & 1 \
            and Directions.NORTH in valid_directions_and_neighbor_index:
        del valid_directions_and_neighbor_index[Directions.NORTH]
    if not cell.walls & 2 \
            and Directions.EAST in valid_directions_and_neighbor_index:
        del valid_directions_and_neighbor_index[Directions.EAST]
    if not cell.walls & 4 \
            and Directions.SOUTH in valid_directions_and_neighbor_index:
        del valid_directions_and_neighbor_index[Directions.SOUTH]
    if not cell.walls & 8 \
            and Directions.WEST in valid_directions_and_neighbor_index:
        del valid_directions_and_neighbor_index[Directions.WEST]

    are_static = []
    for key, value in valid_directions_and_neighbor_index.items():
        if maze[value].static:
            are_static.append(key)

    if are_static:
        for key in are_static:
            del valid_directions_and_neighbor_index[key]

    if len(valid_directions_and_neighbor_index) == 3:
        _get_middle_direction(valid_directions_and_neighbor_index)

    if valid_directions_and_neighbor_index:
        selected_dir = rng.choice(list(
            valid_directions_and_neighbor_index.items()
            ))

        _build_path(cell, maze[selected_dir[1]], selected_dir[0])

    # while len(directions):
    #     dir = rng.choice(directions)
    #     try:
    #         neighbors_index = validate_direction(
    #             cell.INDEX, dir, width, height
    #             )
    #     except InvalidDirection:
    #         directions.remove(dir)
    #         continue
    #     else:
    #         if maze[neighbors_index].static:
    #             directions.remove(dir)
    #             continue
    #         else:
    #             _build_path(cell, maze[neighbors_index], dir)
    #             directions.remove(dir)


def dead_end_deleter(
        maze: Maze,
        cell: MazeCell,
        width: int,
        height: int,
        rng: random.Random
) -> None:
    """Remove dead ends from a maze cell when it becomes a three-wall junction.

    Args:
        maze: Maze grid.
        cell: Cell currently being evaluated.
        width: Maze width.
        height: Maze height.
        rng: Random generator used for random wall deletion.
    """

    if _is_a_corner(maze, cell, width, height) or cell.static:
        return
    else:
        walls = _count_walls(cell)
        if walls == 3:
            _delete_walls(maze, cell, width, height, rng)
