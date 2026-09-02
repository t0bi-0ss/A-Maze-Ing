"""
Pathfinding support functions used to compute shortest routes in the maze.
"""

from maze_generator import MazeCell, Maze

from .exceptions import UnreachableCellsError


def select_from_unvisited(unvisited: list[MazeCell]) -> MazeCell:
    """Choose the nearest reachable cell from the unvisited frontier.

    Args:
        unvisited: Cells not yet finalized during path search.

    Returns:
        The cell with the smallest distance to the entrance.

    Raises:
        UnreachableCellsError: If no reachable cells remain in the frontier.
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
    """Update adjacent cells with the distance from the maze entrance.

    Args:
        maze: Maze grid.
        maze_width: Maze width.
        current_cell: Cell whose neighbors should be evaluated.
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
    """Find the neighbor closest to the maze entrance.

    Args:
        maze: Maze grid.
        current_cell: Cell whose route back toward the entrance is being
        traced.
        maze_width: Maze width.

    Returns:
        A tuple of the neighboring cell and the direction used to reach it.
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
    """Trace the shortest path from the exit back to the entrance.

    Args:
        maze: Maze grid containing computed distances.
        exit_cell: Goal cell for the route.
        maze_width: Maze width.

    Returns:
        A sequence of direction characters from the exit to the entrance.
    """

    current_cell = exit_cell
    path = ""

    while current_cell.distance_to_entrance != 0:
        closest_neighbor = _closest_neighbor(maze, current_cell, maze_width)
        path = closest_neighbor[1] + path
        current_cell = closest_neighbor[0]
    return path
