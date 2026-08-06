"""
Holds MazeGenerator class
"""


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


# Maze center

