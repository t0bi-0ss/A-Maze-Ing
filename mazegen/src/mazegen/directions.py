"""Direction handling and neighbor validation for maze generation."""

from enum import Enum

from .exceptions import InvalidDirection


class Directions(Enum):
    """Supported movement directions in the maze grid."""

    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


def get_neighbors_index(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
) -> int:
    """Return the neighbor index for a cell in the given direction.

    Args:
        c_cell_index: Current cell index in row-major order.
        dir: Direction to inspect.
        maze_width: Width of the maze, used to compute row boundaries.

    Returns:
        The neighbor cell index.
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
    """Validate whether moving in a direction stays within the maze.

    Args:
        c_cell_index: Current cell index in row-major order.
        dir: Direction to validate.
        maze_width: Width of the maze.
        maze_height: Height of the maze.

    Returns:
        The neighbor index if the direction is valid.

    Raises:
        InvalidDirection: If the direction would leave the maze bounds.
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
