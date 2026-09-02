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
        entry: tuple[str, str],
        exit: tuple[str, str],
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
    converted_entry = int(entry[0]), int(entry[1])
    converted_exit = int(exit[0]), int(exit[1])

    if converted_entry in pattern_cells or converted_exit in pattern_cells:
        print(
            "ERROR: unsolvable maze. Either entry or exit coordinates"
            " coincide with one of the '42' pattern cells"
            "\nPattern cells coordinates =",
            pattern_cells,
            "\nEntry coordinates =", converted_entry,
            "\nExit coordinates =", converted_exit
        )
        sys.exit()
