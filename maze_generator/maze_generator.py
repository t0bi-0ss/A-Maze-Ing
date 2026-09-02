"""Core maze-generation engine and generator state management."""

import random

from .mazecell import MazeCell, Maze

from .center_pattern import pattern

from .gen_algorithms import growing_tree

from collections.abc import Generator

from .dead_end_deleter import dead_end_deleter

from .is_coliding import colition_checker


def _starting_cell(maze: Maze, rng: random.Random) -> MazeCell:
    """Choose a non-static maze cell to begin generation.

    Args:
        maze: Maze grid being generated.
        rng: Random generator used to pick a starting cell.

    Returns:
        A valid starting cell with visited status enabled.
    """

    cell = rng.choice(maze)

    if cell.static:
        cell = _starting_cell(maze, rng)
    cell.is_now_visited()
    return cell


class MazeGenerator:
    """
    Generate and manage a maze instance with configurable generation rules.
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            selector: float = -1,
            perfect: bool = True,
            seed: int | float |
            str | bytes |
            bytearray | None = None,
            perfect_centered: bool = True,
            output_file: str = "maze.txt"
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            entry: Entry coordinates as ``(row, col)``.
            exit: Exit coordinates as ``(row, col)``.
            selector: Growth strategy selector for the generator.
            perfect: Whether to keep the maze fully perfect.
            seed: Random seed for reproducible generation.
            perfect_centered: Whether the fixed center pattern should stay
            centered.
            output_file: File path used when exporting the maze.
        """
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
        self.OUTPUT_FILE = output_file

    def gen_maze(self) -> Generator[Maze, None, None]:
        """Yield the maze state as it is progressively generated.

        Yields:
            The current maze state after each generation step.
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

        index = 0
        if not self.PERFECT:
            while index < len(self.maze):
                dead_end_deleter(
                    self.maze,
                    self.maze[index],
                    self.WIDTH,
                    self.HEIGHT,
                    self.rng
                )
                index += 1
                yield self.maze
