from maze_generator import MazeCell, Maze

from .exceptions import UnreachableCellsError


def select_from_unvisited(unvisited: list[MazeCell]) -> MazeCell:
    """
    Selects closest cell to entrance found in the unvisited list.

    Args:
        unvisited (list[MazeCell]): A list of unvisited cells.

    Returns:
        MazeCell: The selected cell from the unvisited list.
    """

    current_cell = None
    for cell in unvisited:
        # Check if cell has been reached
        if not cell.distance_to_entrance == -1:
            if (
                not current_cell
                or (current_cell.distance_to_entrance >
                    cell.distance_to_entrance)
            ):
                current_cell = cell

    if not current_cell:
        raise UnreachableCellsError

    return current_cell


def set_neighbors_distance(
    maze: Maze,
    maze_width: int,
    current_cell: MazeCell
) -> None:
    """
    Sets current cell's neighbors distance to entrance
    """

    new_distance = current_cell.distance_to_entrance + 1

    # Check if North wall is present
    if not current_cell.walls & 1:
        north_neighbor = maze[current_cell.INDEX - maze_width]
        if (
            north_neighbor.distance_to_entrance == -1
            or new_distance < north_neighbor.distance_to_entrance
        ):
            north_neighbor.distance_to_entrance = new_distance

    # Check if East wall is present
    if not current_cell.walls & 2:
        east_neighbor = maze[current_cell.INDEX + 1]
        if (
            east_neighbor.distance_to_entrance == -1
            or new_distance < east_neighbor.distance_to_entrance
        ):
            east_neighbor.distance_to_entrance = new_distance

    # Check if South wall is present
    if not current_cell.walls & 4:
        south_neighbor = maze[current_cell.INDEX + maze_width]
        if (
            south_neighbor.distance_to_entrance == -1
            or new_distance < south_neighbor.distance_to_entrance
        ):
            south_neighbor.distance_to_entrance = new_distance

    # Check if West wall is present
    if not current_cell.walls & 8:
        west_neighbor = maze[current_cell.INDEX - 1]
        if (
            west_neighbor.distance_to_entrance == -1
            or new_distance < west_neighbor.distance_to_entrance
        ):
            west_neighbor.distance_to_entrance = new_distance


def _closest_neighbor(
    maze: Maze, current_cell: MazeCell, maze_width: int
) -> tuple[MazeCell, str]:
    """
    Looks for current_cell's valid neighbor closest to entrance
    """

    all_neighbors = []

    # Check if North wall is present
    if not current_cell.walls & 1:
        north_neighbor = maze[current_cell.INDEX - maze_width]
        all_neighbors.append((north_neighbor, "S"))

    # Check if East wall is present
    if not current_cell.walls & 2:
        east_neighbor = maze[current_cell.INDEX + 1]
        all_neighbors.append((east_neighbor, "W"))

    # Check if South wall is present
    if not current_cell.walls & 4:
        south_neighbor = maze[current_cell.INDEX + maze_width]
        all_neighbors.append((south_neighbor, "N"))

    # Check if West wall is present
    if not current_cell.walls & 8:
        west_neighbor = maze[current_cell.INDEX - 1]
        all_neighbors.append((west_neighbor, "E"))

    closest_neighbor = None

    for neighbor in all_neighbors:
        if (
            not closest_neighbor
            or neighbor[0].distance_to_entrance
            < closest_neighbor[0].distance_to_entrance
        ):
            closest_neighbor = neighbor

    return closest_neighbor


def path_to_entrance(
        maze: Maze,
        exit_cell: MazeCell,
        maze_width: int
) -> list[str]:
    """
    Looks for path from exit to entrance
    """

    current_cell = exit_cell
    path = ""

    while current_cell.distance_to_entrance != 0:
        closest_neighbor = _closest_neighbor(maze, current_cell, maze_width)
        path = closest_neighbor[1] + path
        current_cell = closest_neighbor[0]

    return path
