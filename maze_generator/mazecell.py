class MazeCell():
    """
    pass
    """

    def __init__(self, index: int) -> None:
        self.INDEX = index
        self.walls = 15
        self.static = False
        self.is_visited = False

    def is_now_static(self) -> None:
        """
        Switches static attribute to True
        """
        self.static = True

    def is_now_visited(self) -> None:
        """
        Switches is_visited attribute to True
        """
        self.is_visited = True

    def del_north(self) -> None:
        """
        Deletes 'North' wall
        """

        if self.walls & 1:
            self.walls = self.walls ^ 1

    def del_east(self) -> None:
        """
        Deletes 'East' wall
        """

        if self.walls & 2:
            self.walls = self.walls ^ 2

    def del_south(self) -> None:
        """
        Deletes 'South' wall
        """

        if self.walls & 4:
            self.walls = self.walls ^ 4

    def del_west(self) -> None:
        """
        Deletes 'West' wall
        """

        if self.walls & 8:
            self.walls = self.walls ^ 8


Maze = list[MazeCell]
