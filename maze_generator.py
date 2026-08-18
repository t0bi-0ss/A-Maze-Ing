"""
Holds MazeGenerator class
"""

from collections.abc import Callable

import random


class InvalidMovement(Exception):
    """
    Exception for an 'invalid' movement
    """

    def __init__(self, movement: str) -> None:
        self.message = f"Movement '{movement}' not recognized." \
            " Valid movements: ['N', 'E', 'S', 'W']"
        super.__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ImpossibleMovement(Exception):
    """
    Exception for an 'impossible' movement
    """

    def __init__(self, move: str) -> None:
        self.message = f"Impossible to move '{move}' from selected cell"
        super.__init__(self.message)

    def __str__(self) -> str:
        return self.message


class MazeCell():
    """
    pass
    """

    def __init__(self, index: int) -> None:
        self.INDEX = index
        self.walls = 15
        self.static = False

    def del_north(self) -> None:
        """
        Deletes 'North' wall
        """

        self.walls = self.walls ^ 1

    def del_east(self) -> None:
        """
        Deletes 'East' wall
        """

        self.walls = self.walls ^ 2

    def del_south(self) -> None:
        """
        Deletes 'South' wall
        """

        self.walls = self.walls ^ 4

    def del_west(self) -> None:
        """
        Deletes 'West' wall
        """

        self.walls = self.walls ^ 8


def random_neighbor(
        current_cell: MazeCell,
        maze: list[MazeCell],
        maze_width: int,
) -> MazeCell:
    """
    Returns random current_cell neighbor cell
    """

    move = random.choice(['N', 'E', 'S', 'W'])
    total_elements = len(maze)
    current_index = current_cell.INDEX

    match move:
        case 'N':
            if current_index < maze_width:
                current_index = -1
            else:
                current_index -= maze_width
        case 'E':
            if (current_index + 1) % maze_width == 0:
                current_index = -1
            else:
                current_index += 1
        case 'S':
            if current_index + maze_width > total_elements:
                current_index = -1
            else:
                current_index += maze_width
        case 'W':
            if current_index % maze_width == 0:
                current_index = -1
            else:
                current_index -= 1
    current_cell = maze[current_index]
    return current_cell


class MazeGenerator():
    """
    Generates a random maze
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            perfect: bool = False,
            seed: int | float |
            str | bytes |
            bytearray | None = None
    ) -> None:
        self.WIDTH = width
        self.HEIGHT = height
        self.ENTRY = entry
        self.EXIT = exit
        self.PERFECT = perfect
        self.SEED = seed
        self.maze = [[15 for col in range(0, self.WIDTH)]
                     for row in range(0, self.HEIGHT)]
        self.valid_coordinates = self.valid_list()

    # VALID coordinates list
    def valid_list(self) -> list[tuple[int, int]]:
        """
        Creates a list of 'valid' coordinates
        """

        valid_coordinates = []
        for row in range(0, self.HEIGHT):
            for col in range(0, self.WIDTH):
                if self.maze[row][col] == 15:
                    valid_coordinates.append((row, col))

        return valid_coordinates

    # Define pattern cells
    def pattern_setter(self) -> None:
        """
        Sets 'pattern' cells if possible
        """

        if self.WIDTH >= 9 and self.HEIGHT >= 7:
            center = (round(self.HEIGHT / 2), round(self.WIDTH / 2))
            four_top_left = tuple(map(sum, zip(center, (-2, -3))))
            two_top_left = tuple(map(sum, zip(center, (-2, 1))))

            def three_down(
                    starting_coordinates: tuple[int, int],
                    maze: list[list[int]]
            ) -> None:
                x = starting_coordinates[0]
                y = starting_coordinates[1]
                for i in range(0, 3):
                    maze[x + i][y] = 16
            three_down()
        else:
            print("ERROR: maze size is not big enough to hold '42' pattern")


def random_cell(
        cells: list[MazeCell],
) -> MazeCell:
    """
    Returns a non 'static' cell randomly selected from 'cells'
    """

    cell = cells[random.randint(0, len(cells) - 1)]

    if cell.static:
        return random_cell(cells)
    else:
        return cell
