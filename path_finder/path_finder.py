from maze_generator import Maze

from .helper_f import select_from_unvisited, set_neighbors_distance, \
    path_to_entrance

from .exceptions import UnreachableCellsError


def path_finder(
        maze: Maze,
        entrance: tuple[int, int],
        exit: tuple[int, int],
        maze_width: int
) -> str:
    """
    Finds a path from entrance to exit in the maze using Dijkstra's algorithm.

    Args:
        maze (Maze): The maze represented as a list of MazeCell objects.
        entrance (tuple[int, int]): The coordinates of the entrance cell.
        exit (tuple[int, int]): The coordinates of the exit cell.
        maze_width (int): The width of the maze.

    Returns:
        list[str]: A list of directions representing the path from entrance to
        exit.
    """

    unvisited = [cell for cell in maze if not cell.static]

    entrance_index = entrance[0] * maze_width + entrance[1]
    entrance_cell = maze[entrance_index]
    entrance_cell.distance_to_entrance = 0

    exit_index = exit[0] * maze_width + exit[1]
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
