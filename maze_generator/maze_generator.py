import random

from .mazecell import MazeCell, Maze

from .center_pattern import pattern

from .gen_algorithms import growing_tree

from collections.abc import Generator

from .dead_end_deleter import dead_end_deleter

from .is_coliding import colition_checker


def _starting_cell(maze: Maze, rng: random.Random) -> MazeCell:
    """
    Selects a random cell from maze to use as a starting point
    """

    cell = rng.choice(maze)

    if cell.static:
        cell = _starting_cell(maze, rng)
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
            selector: float = -1,
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
        self.rng = random.Random(seed)
        self.PCENTERED = perfect_centered
        self.maze = [MazeCell(element_num) for element_num
                     in range(0, self.WIDTH * self.HEIGHT)]
        pattern(self.maze, self.WIDTH, self.HEIGHT, self.PCENTERED, self.rng)
        colition_checker(self.maze, self.ENTRY, self.EXIT, self.WIDTH)
        self.generator = self.gen_maze

    def gen_maze(self) -> Generator[Maze, None, None]:
        """
        Returns a Maze generator
        """

        visited_cells = [_starting_cell(self.maze, self.rng)]
        while len(visited_cells):
            yield self.maze
            growing_tree(
                visited_cells,
                self.maze,
                self.WIDTH,
                self.HEIGHT,
                self.SELECTOR,
                self.rng
            )
        if not self.PERFECT:
            dead_end_deleter(self.maze, self.WIDTH, self.HEIGHT, self.rng)
            yield self.maze
