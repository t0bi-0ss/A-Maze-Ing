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


class InvalidDirection(Exception):
    """
    Exception for an invalid Direction
    """


class InvalidNeighbor(Exception):
    """
    Exception in case of an invalid neighbor's index
    """


class NoValidNeighbors(Exception):
    """
    Exception in case no valid neighbors are found
    """


class DeadEnd(Exception):
    """
    Exception when a 'dead end' has been reached
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

    def is_now_visited(self) -> None:
        """
        Switches is_visited attribute to True
        """
        self.is_visited = True

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
    cell.is_now_visited()
    print("Starting cell index = ", maze.index(cell))
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

    # if len(visited) == 0:
    #     raise EmptyVisitedList
    if selector == 1:
        return random.choice(visited)
    elif selector == 0:
        return visited[-1]
    else:
        return _select_from_visited(visited, stochastic_round(selector))


def _validate_direction(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
        maze_height: int
) -> int:
    """
    Checks if direction is valid considering current cell. Returns neighbors
    index if True
    """

    total_elements = maze_width * maze_height
    neighbors_index = -1

    match dir.value:
        case 'N':
            if not c_cell_index < maze_width:
                neighbors_index = c_cell_index - maze_width
        case 'E':
            if not (c_cell_index + 1) % maze_width == 0:
                neighbors_index = c_cell_index + 1
        case 'S':
            if not c_cell_index + maze_width >= total_elements:
                neighbors_index = c_cell_index + maze_width
        case 'W':
            if not c_cell_index % maze_width == 0:
                neighbors_index = c_cell_index - 1

    if neighbors_index < 0:
        raise InvalidDirection
    return neighbors_index


def _neighbor_validator(maze: Maze, neighbors_index: int) -> MazeCell:
    """
    Returns cell's neighbor cell in 'dir' direction if it's valid
    """

    neighbor = maze[neighbors_index]

    if neighbor.static or neighbor.is_visited:
        raise InvalidNeighbor
    return neighbor


def _return_valid_dir_and_neighbor(
        current_cell: MazeCell,
        maze: Maze,
        maze_width: int,
        maze_height: int
) -> tuple[Directions, MazeCell]:
    """
    Returns a valid cell's neighbor if any
    """

    neighbor = None
    directions = [dir for dir in Directions]
    current_cell_index = current_cell.INDEX

    while len(directions):
        dir = random.choice(directions)
        try:
            neighbors_index = _validate_direction(
                current_cell_index, dir, maze_width, maze_height
            )
            neighbor = _neighbor_validator(maze, neighbors_index)
        except (InvalidDirection, InvalidNeighbor):
            neighbor = None
            directions.remove(dir)
        else:
            break
    if not neighbor and not len(directions):
        raise NoValidNeighbors

    return dir, neighbor


def _build_path(
        current_cell: MazeCell,
        neighbor_cell: MazeCell,
        dir: Directions
) -> None:
    """
    Builds path between current_cell and neighbor_cell according to dir
    """

    match dir.value:
        case 'N':
            current_cell.del_north()
            neighbor_cell.del_south()
        case 'E':
            current_cell.del_east()
            neighbor_cell.del_west()
        case 'S':
            current_cell.del_south()
            neighbor_cell.del_north()
        case 'W':
            current_cell.del_west()
            neighbor_cell.del_east()


def _connect_neighbor(
        current_cell: MazeCell,
        maze: Maze,
        maze_width: int,
        maze_height: int,
        visited_list: list[MazeCell]
) -> None:
    """
    Connects 'cell' with one of it's neighbors if possible
    """

    try:
        dir_and_neighbor = _return_valid_dir_and_neighbor(
            current_cell, maze, maze_width, maze_height
            )
    except NoValidNeighbors:
        raise DeadEnd
    else:
        neighbor_cell = dir_and_neighbor[1]
        neighbor_cell.is_now_visited()
        visited_list.append(neighbor_cell)
        dir = dir_and_neighbor[0]
        # print(f"Current_cell index = {current_cell.INDEX}")
        # print(f"Neighbor_cell index = {neighbor_cell.INDEX}")
        # print(f"Direction = {dir}")
        _build_path(current_cell, neighbor_cell, dir)


def _move_forward(
        visited: list[MazeCell],
        maze: Maze,
        maze_width: int,
        maze_height: int,
        selector: float
) -> None:
    """
    Builds next path bewteen cells if possible
    """

    try:
        current_cell = _select_from_visited(visited, selector)
        _connect_neighbor(current_cell, maze, maze_width, maze_height, visited)
    except DeadEnd:
        visited.remove(current_cell)


def _print_maze(maze: Maze, width: int):
    print()
    counter = 1
    for cel in maze:
        print(cel.walls, end="")
        if counter != width:
            print(", ", end="")
            counter += 1
        else:
            print()
            counter = 1


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
        self.generator = self.gen_maze

    def gen_maze(self) -> Maze:
        """
        Returns a Maze generator
        """

        visited_cells = [_starting_cell(self.maze)]
        while len(visited_cells):
            yield self.maze
            _move_forward(
                visited_cells,
                self.maze,
                self.WIDTH,
                self.HEIGHT,
                self.SELECTOR
            )


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

if __name__ == "__main__":

    maze = MazeGenerator(9, 9, (0, 0), (3, 3), 0, True)

    from collections import deque

    # Exhaust the generator instantly
    deque(maze.generator(), maxlen=0)
    counter = 1
    final = ""
    for _ in maze.maze:
        final += to_hex(_.walls)
        if counter == 9 and _ != maze.maze[-1]:
            counter = 1
            final += "\n"
            continue
        counter += 1
    print(final)
    print(maze.maze[-1].INDEX)

    with open('maze.txt', 'w') as f:
        f.write(final)
