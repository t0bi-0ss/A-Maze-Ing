import random

from .mazecell import MazeCell, Maze

from .center_pattern import pattern

from .gen_algorithms import growing_tree

from collections.abc import Generator

from .dead_end_deleter import dead_end_deleter

import sys


def _starting_cell(maze: Maze) -> MazeCell:
    """
    Selects a random cell from maze to use as a starting point
    """

    cell = random.choice(maze)

    if cell.static:
        cell = _starting_cell(maze)
    cell.is_now_visited()
    return cell


class MazeGenerator:
    """
    Generates a random maze
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            selector: float,
            perfect: bool = False,
            seed: int | float |
            str | bytes |
            bytearray | None = None,
            perfect_centered: bool = True
    ) -> None:
        self.WIDTH = width
        self.HEIGHT = height
        self.ENTRY = entry
        self.EXIT = exit
        self.PERFECT = perfect
        self.SELECTOR = selector
        self.SEED = seed
        self.PCENTERED = perfect_centered
        self.maze = [MazeCell(element_num) for element_num
                     in range(0, self.WIDTH * self.HEIGHT)]
        pattern(self.maze, self.WIDTH, self.HEIGHT, self.PCENTERED)
        self.generator = self.gen_maze

    def gen_maze(self) -> Generator[Maze, None, None]:
        """
        Returns a Maze generator
        """

        visited_cells = [_starting_cell(self.maze)]
        while len(visited_cells):
            yield self.maze
            growing_tree(
                visited_cells,
                self.maze,
                self.WIDTH,
                self.HEIGHT,
                self.SELECTOR
            )
        if not self.PERFECT:
            dead_end_deleter(self.maze, self.WIDTH, self.HEIGHT)
            yield self.maze

    def transcript(self, output_file_name: str):
        """
        Transcripts all MazeCell's walls value in self.maze into a text file
        while converting said values to hexadecimal
        """

        def to_hex(num):
            match num:
                case 10:
                    return 'a'
                case 11:
                    return 'b'
                case 12:
                    return 'c'
                case 13:
                    return 'd'
                case 14:
                    return 'e'
                case 15:
                    return 'f'
                case _:
                    return str(num)

        counter = 1
        res = ""

        for cell in self.maze:
            res += to_hex(cell.walls)
            if counter == self.WIDTH and cell != self.maze[-1]:
                counter = 1
                res += "\n"
                continue
            counter += 1

        try:
            with open(output_file_name, 'w') as f:
                f.write(res)
        except (
                    UnicodeDecodeError,
                    ValueError,
                    OSError,
                    PermissionError,
                    IsADirectoryError,
                    FileNotFoundError,
        ) as msg:
            print(msg)
            sys.exit()
