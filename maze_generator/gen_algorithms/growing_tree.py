"""Growing-tree maze generation algorithm and related helpers."""

from ..directions import Directions, validate_direction

from ..mazecell import MazeCell, Maze

import random

from ..exceptions import EmptyVisitedList, \
    InvalidDirection, InvalidNeighbor, NoValidNeighbors


def _select_from_visited(
        visited: list[MazeCell], selector: float, rng: random.Random
) -> MazeCell:
    """Choose the next active cell from the visited list.

    Args:
        visited: Cells visited so far in the growth frontier.
        selector: Strategy selector controlling random or backtracking
        behavior.
        rng: Random number generator.

    Returns:
        A selected cell from the visited list.

    Raises:
        EmptyVisitedList: If the frontier has no cells remaining.
    """

    def stochastic_round(num: float, rng: random.Random) -> int:
        """Convert a probability to a random binary choice.

        Args:
            num: Probability threshold between 0 and 1.
            rng: Random generator.

        Returns:
            0 or 1 depending on the random draw.
        """
        return 0 if rng.random() < num else 1

    if len(visited) == 0:
        raise EmptyVisitedList
    if selector == -1:
        selector = rng.random()
    if 0 < selector < 1:
        selector = stochastic_round(selector, rng)
    # Prism
    if selector == 1:
        return rng.choice(visited)
    # Backtracking
    elif selector == 0:
        return visited[-1]


def _neighbor_validator(maze: Maze, neighbors_index: int) -> MazeCell:
    """Return a valid unvisited non-static neighbor cell.

    Args:
        maze: Maze grid.
        neighbors_index: Candidate neighbor index.

    Returns:
        The neighboring cell if it can be used for expansion.

    Raises:
        InvalidNeighbor: If the neighbor is static or already visited.
    """

    neighbor = maze[neighbors_index]

    if neighbor.static or neighbor.is_visited:
        raise InvalidNeighbor
    return neighbor


def _return_valid_dir_and_neighbor(
        current_cell: MazeCell,
        maze: Maze,
        maze_width: int,
        maze_height: int,
        rng: random.Random
) -> tuple[Directions, MazeCell]:
    """Find a valid neighbor direction and target cell for expansion.

    Args:
        current_cell: Cell currently being expanded.
        maze: Maze grid.
        maze_width: Maze width.
        maze_height: Maze height.
        rng: Random generator for choosing an available direction.

    Returns:
        The chosen direction and neighbor cell.

    Raises:
        NoValidNeighbors: If no legal neighbor exists for the current cell.
    """

    neighbor = None
    directions = [dir for dir in Directions]
    current_cell_index = current_cell.INDEX

    while len(directions):
        dir = rng.choice(directions)
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
    """Open a passage between a cell and one of its neighbors.

    Args:
        current_cell: Cell being expanded.
        neighbor_cell: Neighbor that will be connected.
        dir: Direction of the connection.
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
        visited_list: list[MazeCell],
        rng: random.Random
) -> int:
    """Connect a cell to one valid neighboring cell, if possible.

    Args:
        current_cell: Cell currently being grown from.
        maze: Maze grid.
        maze_width: Maze width.
        maze_height: Maze height.
        visited_list: Current frontier of visited cells.
        rng: Random generator controlling neighbor selection.

    Returns:
        1 if a neighbor was connected, otherwise 0.
    """

    try:
        dir_and_neighbor = _return_valid_dir_and_neighbor(
            current_cell, maze, maze_width, maze_height, rng
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
        selector: float,
        rng: random.Random
) -> None:
    """Advance the growing-tree algorithm by one expansion step.

    Args:
        visited: Frontier of visited cells.
        maze: Maze grid being generated.
        maze_width: Maze width.
        maze_height: Maze height.
        selector: Generation strategy selector.
        rng: Random generator for expansion choices.
    """

    could_connect = 0

    try:
        while not could_connect:
            current_cell = _select_from_visited(visited, selector, rng)
            could_connect = _connect_neighbor(
                current_cell, maze, maze_width, maze_height, visited, rng
            )
            if not could_connect:
                visited.remove(current_cell)
    except EmptyVisitedList:
        return
