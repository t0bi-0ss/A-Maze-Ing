from ..directions import Directions, validate_direction

from ..mazecell import MazeCell, Maze

import random

from ..exceptions import EmptyVisitedList, \
    InvalidDirection, InvalidNeighbor, NoValidNeighbors


def _select_from_visited(visited: list[MazeCell], selector: float) -> MazeCell:
    """
    Selects a cell from 'visited' list according to 'selector'
    """

    def stochastic_round(num: float) -> int:
        """
        Returns num rounded up or down being it's proper value the chance for
        either case
        """
        return 0 if random.random() < num else 1

    if len(visited) == 0:
        raise EmptyVisitedList
    if selector == 1:
        return random.choice(visited)
    elif selector == 0:
        return visited[-1]
    else:
        return _select_from_visited(visited, stochastic_round(selector))


def _neighbor_validator(maze: Maze, neighbors_index: int) -> MazeCell:
    """
    Returns cell's neighbor cell in 'dir' direction if it's valid
    """

    neighbor = maze[neighbors_index]

    if neighbor.static or neighbor.is_visited:
        raise InvalidNeighbor
    return neighbor


def _return_valid_dir_and_neighbor(
        current_cell: MazeCell,
        maze: Maze,
        maze_width: int,
        maze_height: int
) -> tuple[Directions, MazeCell]:
    """
    Returns a valid cell's neighbor if any
    """

    neighbor = None
    directions = [dir for dir in Directions]
    current_cell_index = current_cell.INDEX

    while len(directions):
        dir = random.choice(directions)
        try:
            neighbors_index = validate_direction(
                current_cell_index, dir, maze_width, maze_height
            )
            neighbor = _neighbor_validator(maze, neighbors_index)
        except (InvalidDirection, InvalidNeighbor):
            neighbor = None
            directions.remove(dir)
        else:
            break
    if not neighbor and not len(directions):
        raise NoValidNeighbors

    return dir, neighbor


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


def _connect_neighbor(
        current_cell: MazeCell,
        maze: Maze,
        maze_width: int,
        maze_height: int,
        visited_list: list[MazeCell]
) -> int:
    """
    Connects 'cell' with one of it's neighbors if possible
    """

    try:
        dir_and_neighbor = _return_valid_dir_and_neighbor(
            current_cell, maze, maze_width, maze_height
            )
    except NoValidNeighbors:
        return 0
    else:
        neighbor_cell = dir_and_neighbor[1]
        neighbor_cell.is_now_visited()
        visited_list.append(neighbor_cell)
        dir = dir_and_neighbor[0]
        _build_path(current_cell, neighbor_cell, dir)
        return 1


def growing_tree(
        visited: list[MazeCell],
        maze: Maze,
        maze_width: int,
        maze_height: int,
        selector: float
) -> None:
    """
    Builds next path bewteen cells if possible
    """

    could_connect = 0

    try:
        while not could_connect:
            current_cell = _select_from_visited(visited, selector)
            could_connect = _connect_neighbor(
                current_cell, maze, maze_width, maze_height, visited
            )
            if not could_connect:
                visited.remove(current_cell)
    except EmptyVisitedList:
        return
