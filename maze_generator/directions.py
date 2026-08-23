from enum import Enum

from .exceptions import InvalidDirection


class Directions(Enum):

    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


def get_neighbors_index(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
) -> int:
    """
    Returns neighbors index in specified direction
    """

    match dir.value:
        case 'N':
            return c_cell_index - maze_width
        case 'E':
            return c_cell_index + 1
        case 'S':
            return c_cell_index + maze_width
        case 'W':
            return c_cell_index - 1


def validate_direction(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
        maze_height: int
) -> int:
    """
    Checks if direction is valid considering current cell. Returns neighbors
    index if True
    """

    total_elements = maze_width * maze_height
    neighbors_index = -1

    match dir.value:
        case 'N':
            if not c_cell_index < maze_width:
                neighbors_index = c_cell_index - maze_width
        case 'E':
            if not (c_cell_index + 1) % maze_width == 0:
                neighbors_index = c_cell_index + 1
        case 'S':
            if not c_cell_index + maze_width >= total_elements:
                neighbors_index = c_cell_index + maze_width
        case 'W':
            if not c_cell_index % maze_width == 0:
                neighbors_index = c_cell_index - 1

    if neighbors_index < 0:
        raise InvalidDirection
    return neighbors_index
