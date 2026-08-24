from .mazecell import Maze, MazeCell

from .directions import Directions, validate_direction

import random

from .exceptions import InvalidDirection


def _count_walls(cell: MazeCell) -> int:
    """
    Counts number of walls present in cell
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
    """
    Builds path between current_cell and neighbor_cell according to dir
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
    """
    Checks if index corresponds to a cell located on either of the four corners
    of the maze, and deletes corresponding walls if it's true
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


def _delete_walls(
        maze: Maze, cell: MazeCell, width: int, height: int
) -> None:
    """
    Deletes a 'dead end'
    """

    directions = [direction for direction in Directions]

    while len(directions):
        dir = random.choice(directions)
        try:
            neighbors_index = validate_direction(
                cell.INDEX, dir, width, height
                )
        except InvalidDirection:
            directions.remove(dir)
            continue
        else:
            if maze[neighbors_index].static:
                directions.remove(dir)
                continue
            else:
                _build_path(cell, maze[neighbors_index], dir)
                directions.remove(dir)


def dead_end_deleter(maze: Maze, width: int, height: int) -> None:
    """
    Searches maze for 'dead ends' and deletes them all
    """

    for cell in maze:
        if _is_a_corner(maze, cell, width, height) or cell.static:
            continue
        else:
            walls = _count_walls(cell)
            if walls == 3:
                _delete_walls(maze, cell, width, height)
