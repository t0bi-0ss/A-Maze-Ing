"""Cell-level maze data model and wall management helpers."""


class MazeCell():
    """Represent a single maze cell and its wall configuration."""

    def __init__(self, index: int) -> None:
        """Initialize a maze cell.

        Args:
            index: The cell's position in the row-major maze list.
        """
        self.INDEX = index
        self.walls = 15
        self.static = False
        self.is_visited = False
        self.distance_to_entrance = -1

    def is_now_static(self) -> None:
        """Mark the cell as part of the fixed structural pattern."""
        self.static = True

    def is_now_visited(self) -> None:
        """Mark the cell as visited during maze generation."""
        self.is_visited = True

    def del_north(self) -> None:
        """Remove the north wall from the cell when present."""

        if self.walls & 1:
            self.walls = self.walls ^ 1

    def del_east(self) -> None:
        """Remove the east wall from the cell when present."""

        if self.walls & 2:
            self.walls = self.walls ^ 2

    def del_south(self) -> None:
        """Remove the south wall from the cell when present."""

        if self.walls & 4:
            self.walls = self.walls ^ 4

    def del_west(self) -> None:
        """Remove the west wall from the cell when present."""

        if self.walls & 8:
            self.walls = self.walls ^ 8


Maze = list[MazeCell]
