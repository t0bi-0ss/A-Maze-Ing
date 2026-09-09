"""
Collision checks for entry and exit coordinates against static maze cells.
"""

import sys

from .mazecell import Maze


def _get_coordinates(index: int, width: int) -> tuple[int, int]:
    """Convert a row-major cell index to ``(row, col)`` coordinates.

    Args:
        index: Linear index of a maze cell.
        width: Maze width.

    Returns:
        The corresponding row and column pair.
    """
    return index // width, index % width


def colition_checker(
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int],
        maze_width: int
) -> None:
    """Ensure the entry and exit do not overlap fixed pattern cells.

    Args:
        maze: Maze grid containing static pattern cells.
        entry: Entry coordinates as ``(row, col)`` strings.
        exit: Exit coordinates as ``(row, col)`` strings.
        maze_width: Width of the maze.

    Raises:
        SystemExit: If either entry or exit overlaps a static cell.
    """

    pattern_cells = [_get_coordinates(cell.INDEX, maze_width) for
                     cell in maze if cell.static]

    if entry in pattern_cells or exit in pattern_cells:
        print(
            "ERROR: unsolvable maze. Either entry or exit coordinates"
            " coincide with one of the '42' pattern cells"
            "\nPattern cells coordinates =",
            pattern_cells,
            "\nEntry coordinates =", entry,
            "\nExit coordinates =", exit
        )
        sys.exit()
