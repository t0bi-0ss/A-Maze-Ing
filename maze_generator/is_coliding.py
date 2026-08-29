import sys

from .mazecell import Maze


def _get_coordinates(index: int, width: int) -> tuple[int, int]:
    """
    Transforms index to a (x, y) format coordinates
    """

    return index % width, index // width


def colition_checker(
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int],
        maze_width: int
) -> None:
    """
    Checks if either entry or exit 'colides' with any of the pattern cells
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
