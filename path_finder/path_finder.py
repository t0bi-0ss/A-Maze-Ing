"""Public pathfinding entry point for the maze solver."""

from maze_generator import Maze
from .helper_f import select_from_unvisited, set_neighbors_distance, \
    path_to_entrance

from .exceptions import UnreachableCellsError


def path_finder(
        maze: Maze,
        entrance: tuple[str, str],
        exit: tuple[str, str],
        maze_width: int
) -> str:
    """Find a route from the maze entrance to the exit.

    Args:
        maze: Maze represented as a list of maze cells.
        entrance: Entry coordinates as ``(row, col)``.
        exit: Exit coordinates as ``(row, col)``.
        maze_width: Width of the maze.

    Returns:
        A sequence of direction characters describing a valid route.
    """

    unvisited = [cell for cell in maze if not cell.static]

    entrance_index = int(entrance[0]) * maze_width + int(entrance[1])
    entrance_cell = maze[entrance_index]
    entrance_cell.distance_to_entrance = 0

    exit_index = int(exit[0]) * maze_width + int(exit[1])
    exit_cell = maze[exit_index]

    while unvisited:
        try:
            current_cell = select_from_unvisited(unvisited)
        except UnreachableCellsError:
            break
        else:
            set_neighbors_distance(maze, maze_width, current_cell)
            unvisited.remove(current_cell)

    path = path_to_entrance(maze, exit_cell, maze_width)

    return path
