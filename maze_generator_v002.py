import random

from enum import Enum


class Directions(Enum):

    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


class EmptyVisitedList(Exception):
    """
    Exception in case of an empty 'visited' list
    """

    def __init__(self) -> None:
        self.message = "Visited List is empty"

    def __str__(self) -> str:
        return self.message


class InvalidNeighborIndex(Exception):
    """
    Exception in case of an invalid neighbor's index
    """


class MazeCell():
    """
    pass
    """

    def __init__(self, index: int) -> None:
        self.INDEX = index
        self.walls = 15
        self.static = False
        self.is_visited = False

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


Maze = list[MazeCell]


def _starting_cell(maze: Maze) -> MazeCell:
    """
    Selects a random cell from maze to use as a starting point
    """

    cell = random.choice(maze)

    if cell.static:
        cell = _starting_cell(maze)
    return cell


def _select_from_visited(visited: list[MazeCell], selector: float) -> MazeCell:
    """
    Selects a cell from 'visited' list according to 'selector'
    """

    def stochastic_round(num: float) -> int:
        """
        Returns num rounded up or down being it's proper value the chance for
        either case
        """
        return 0 if random.random() < num else 1

    if len(visited) == 0:
        raise EmptyVisitedList
    if selector == 1:
        return random.choice(visited)
    elif selector == 0:
        return visited[-1]
    else:
        return _select_from_visited(visited, stochastic_round(selector))


def move_index(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
        maze_height: int
) -> int:
    """
    Checks neighbor's index when moving in 'dir' direction from current cell's
    index and returns it if its valid
    """

    total_elements = maze_width * maze_height
    neighbors_index = -1

    match dir.value:
        case 'N':
            if not c_cell_index < maze_width:
                neighbors_index -= maze_width
        case 'E':
            if not (c_cell_index + 1) % maze_width == 0:
                neighbors_index += 1
        case 'S':
            if not c_cell_index + maze_width > total_elements:
                neighbors_index += maze_width
        case 'W':
            if not c_cell_index % maze_width == 0:
                neighbors_index -= 1

    if neighbors_index < 0:
        raise 


def neighbor_validator(cell: MazeCell, maze: Maze, dir: Directions) -> MazeCell:
    """
    Returns cell's neighbor cell in 'dir' direction if it's valid
    """

    cell_index = cell.INDEX



def _return_valid_neighbor(
        cell: MazeCell,
        maze_width: int,
        maze_height: int
) -> MazeCell:
    """
    Returns a valid cell's neighbor if any
    """

    neighbor = None
    directions = [dir for dir in Directions]

    while len(directions):
        dir = random.choice(directions)
    total_elements = maze_height * maze_width - 1

    match direction:
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




def _connect_neighbor(cell: MazeCell, maze: Maze) -> None:
    """
    Connects 'cell' with one of it's neighbors if possible
    """




def _move_forward(
        visited: list[MazeCell],
        maze: Maze,
        selector: float
) -> None:
    """
    Builds next path bewteen cells if possible
    """

    try:
        cell = _select_from_visited(visited, selector)
        connect_neighbor
    except EmptyVisitedList:
        return None


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
            selector: float,
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
        self.SELECTOR = selector
        self.SEED = seed
        self.maze = [MazeCell(element_num) for element_num
                     in range(0, self.WIDTH * self.HEIGHT)]
        self.visited = [_starting_cell()]
    
    def gen_maze(self) -> Maze:
        """
        Returns a Maze generator
        """


            

        visited_cells = [self.starting_cell()]
        while len(visited_cells):
            yield self.maze

