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


def get_neighbors_index(
        c_cell_index: int,
        dir: Directions,
        maze_width: int,
) -> int:
    """
    Returns neighbors index in specified direction
    """

    match dir.value:
        case 'N':
            return c_cell_index - maze_width
        case 'E':
            return c_cell_index + 1
        case 'S':
            return c_cell_index + maze_width
        case 'W':
            return c_cell_index - 1


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
        _move_forward(visited, maze, maze_width, maze_height, selector)
    except EmptyVisitedList:
        return


def _locate_center(maze_width: int, maze_height: int) -> int:
    """
    Locates maze's most approximate center
    """

    possible_indexes = []
    if maze_width % 2 != 0 and maze_height % 2 != 0:
        return (maze_height // 2) * maze_width + (maze_width // 2)
    if maze_width % 2 == 0 and maze_height % 2 != 0:
        left_center_index = (maze_height // 2) * \
            maze_width + (maze_width // 2 - 1)
        right_center_index = (maze_height // 2) * \
            maze_width + (maze_width // 2)
        possible_indexes.append(left_center_index)
        possible_indexes.append(right_center_index)
        return random.choice(possible_indexes)
    if maze_width % 2 != 0 and maze_height % 2 == 0:
        top_center_index = ((maze_height // 2) - 1) \
            * maze_width + (maze_width // 2)
        bottom_center_index = (maze_height // 2) \
            * maze_width + (maze_width // 2)
        possible_indexes.append(top_center_index)
        possible_indexes.append(bottom_center_index)
        return random.choice(possible_indexes)
    if maze_width % 2 == 0 and maze_height % 2 == 0:
        rows = [maze_height // 2 - 1, maze_height // 2]
        cols = [maze_width // 2 - 1, maze_width // 2]
        return random.choice(rows) * maze_width + random.choice(cols)


def _set_static_sequence(
        maze: Maze,
        maze_width: int,
        starting_index: int,
        dir: Directions,
        cells_number: int
) -> None:
    """
    Sets a number of cells to static in a specific direction and returns last
    index in the sequence
    """

    current_index = starting_index
    maze[current_index].is_now_static()
    for i in range(0, cells_number - 1):
        current_index = get_neighbors_index(current_index, dir, maze_width)
        maze[current_index].is_now_static()
    return current_index


def _set_four_pattern(
        maze: Maze, maze_width: int, starting_index: int
) -> None:
    """Sets the 'four' on the '42' pattern"""

    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )


def _set_two_pattern(maze: Maze, maze_width: int, starting_index: int) -> None:
    """
    Sets the 'two' on the '42' pattern
    """

    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the left
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.WEST, 3
        )
    # 3 cells down
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.SOUTH, 3
        )
    # 3 cells to the right
    starting_index = _set_static_sequence(
        maze, maze_width, starting_index, Directions.EAST, 3
        )


def _pattern(
        maze: Maze, maze_width: int, maze_height: int, perfect_centered: bool
        ) -> None:
    """Sets '42' pattern in the maze if possible"""

    if maze_width < 9 or maze_height < 8:
        print("ERROR: maze is not big enough to hold the '42' pattern")
        return
    if (maze_width % 2 == 0 or maze_height % 2 == 0) and perfect_centered:
        print(
            "ERROR: either width or center is not odd so '42' could not be"
            " perfectly centered"
        )
        return
    maze_center_index = _locate_center(maze_width, maze_height)
    two_starting_index = maze_center_index - maze_width * 2 + 1
    four_starting_index = maze_center_index - maze_width * 2 - 3
    _set_two_pattern(maze, maze_width, two_starting_index)
    _set_four_pattern(maze, maze_width, four_starting_index)


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
        _pattern(self.maze, self.WIDTH, self.HEIGHT, self.PCENTERED)
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

    maze = MazeGenerator(15, 15, (0, 0), (3, 3), 0.75, True)

    from collections import deque

    # counter = 1
    # for _ in maze.generator():
    #     for val in _:
    #         print(to_hex(val.walls), end="")
    #         if counter == 9:
    #             counter = 1
    #             print()
    #             continue
    #         counter += 1
    #     print()
    # Exhaust the generator instantly
    deque(maze.generator(), maxlen=0)
    counter = 1
    final = ""
    for _ in maze.maze:
        final += to_hex(_.walls)
        if counter == maze.WIDTH and _ != maze.maze[-1]:
            counter = 1
            final += "\n"
            continue
        counter += 1
    # print(final)

    with open('maze.txt', 'w') as f:
        f.write(final)
