"""Core maze-generation engine and generator state management."""
from pydantic import BaseModel, field_validator, model_validator, Field
import random
from .mazecell import MazeCell, Maze
from .center_pattern import pattern
from .gen_algorithms import growing_tree
from collections.abc import Generator
from .open_dead_end_passage import open_dead_end_passage
from .is_coliding import colition_checker
from typing_extensions import Self


def _starting_cell(maze: Maze, rng: random.Random) -> MazeCell:
    """Choose a non-static maze cell to begin generation.

    Args:
        maze: Maze grid being generated.
        rng: Random generator used to pick a starting cell.

    Returns:
        A valid starting cell with visited status enabled.
    """

    cell = rng.choice(maze)

    while cell.static:
        cell = rng.choice(maze)
    cell.is_now_visited()
    return cell


def _selector_choice(algorithm: str) -> int:

    selector = -1
    if algorithm:
        match algorithm:
            case "gt":
                selector = -1
            case "backtracking":
                selector = 0
            case "prims":
                selector = 1
    return selector


class MazeGenerator(BaseModel):
    """Validated configuration data for generating a maze."""

    width: int = Field(gt=2, le=60, default=3)
    height: int = Field(gt=2, le=60, default=3)
    entry: tuple[int, int] = (0, 0)
    exit: tuple[int, int] = (2, 2)
    output_file: str = Field(
        min_length=5,
        max_length=260,
        pattern=r"^[a-zA-Z0-9._-ñ]+$",
        default="maze.txt"
    )
    perfect: bool = False
    seed: str | int | float | None = random.random()
    algorithm: str = "gt"
    pcentered: bool = True
    rng: None = None
    selector: None = None
    maze: None = None
    generator: None = None

    @field_validator("width", "height", mode="before")
    @classmethod
    def validate_size(
        cls,
        input: str
    ) -> int:
        if isinstance(input, str):
            try:
                int(input)
            except ValueError as msg:
                raise ValueError(msg)
            else:
                return int(input)
        return int(input)

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def validate_end_points(
        cls, input: str
    ) -> tuple[int, int]:

        input_list = input.split(",")
        for element in input_list:
            if isinstance(element, str):
                if len(input_list) != 2:
                    raise ValueError(
                        "Input must have two elements only"
                    )
                try:
                    int(input_list[0])
                    int(input_list[1])
                except ValueError as msg:
                    raise ValueError(msg)
        return int(input_list[0]), int(input_list[1])

    @field_validator("algorithm", mode="before")
    @classmethod
    def validate_algorithm(cls, input: str) -> str:
        allowed_strings = ["prims", "backtracking", "gt"]
        try:
            assert input in allowed_strings
        except AssertionError:
            raise AssertionError(f"Allowed strings: {allowed_strings}")
        return input

    @field_validator("perfect", "pcentered", mode="before")
    @classmethod
    def validate_string_bool(cls, input: str | bool) -> bool:
        res = input
        if isinstance(input, str):
            valid_strings = {"true", "false", "yes", "no", "1", "0"}
            if input.strip().lower() not in valid_strings:
                raise ValueError(
                    f"String '{input}' is not a valid boolean representation"
                    f"\nValid strings: {valid_strings}"
                )
            if input in ["true", "yes", "1"]:
                res = True
            else:
                res = False
        return res

    @staticmethod
    def validate_pos(
        maze_width: int,
        maze_height: int,
        pos: tuple[int, int],
        name: str
    ) -> None:
        """Validate a coordinate pair against maze boundaries.

        Args:
            maze_width: Width of the maze in cells.
            maze_height: HEIGHT of the maze in cells.
            pos: Position tuple to validate.
            name: Field name used in error messages.

        Raises:
            ValueError: If the coordinate is not an integer or lies outside the
                maze bounds.
        """

        x = pos[0]
        y = pos[1]
        # Check if either of it's elements exceeds maze boundaries
        if x >= maze_height or x < 0:
            raise ValueError(
                f"{name} = {pos} x value is out of"
                " bounds"
            )

        if y >= maze_width or y < 0:
            raise ValueError(
                f"{name} = {pos} y value is out of"
                " bounds"
            )

    def gen_maze(self) -> Generator[Maze, None, None]:
        """Yield the maze state as it is progressively generated.

        Yields:
            The current maze state after each generation step.
        """

        visited_cells = [_starting_cell(self.maze, self.rng)]
        while visited_cells:
            yield self.maze
            growing_tree(
                visited_cells,
                self.maze,
                self.width,
                self.height,
                self.selector,
                self.rng
            )
        index = 0
        if not self.perfect:
            while index < len(self.maze):
                open_dead_end_passage(
                    self.maze,
                    self.maze[index],
                    self.width,
                    self.height,
                    self.rng
                )
                index += 1
                yield self.maze

    @model_validator(mode="after")
    def validate_configuration(self) -> Self:
        """Validate ENTRY and EXIT coordinates before model creation.

        Returns:
            The validated configuration instance.

        Raises:
            ValueError: If the ENTRY or EXIT cells are invalid or identical.
        """

        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT coordinates must differ")
        try:
            self.validate_pos(self.width, self.height, self.exit, "EXIT")
            self.validate_pos(self.width, self.height, self.entry, "ENTRY")
        except ValueError as msg:
            raise ValueError(msg)
        else:
            self.selector = _selector_choice(self.algorithm)
            self.maze = [MazeCell(element_num) for element_num
                         in range(0, self.width * self.height)]
            self.rng = random.Random(self.seed)
            self.generator = self.gen_maze
        return self

    @model_validator(mode="after")
    def check_for_colition(self) -> Self:
        try:
            pattern(
                self.maze, self.width, self.height, self.pcentered, self.rng
            )
            colition_checker(self.maze, self.entry, self.exit, self.width)
        except ValueError as msg:
            raise ValueError(msg)
        return self

    def __str__(self) -> str:
        """Return a readable summary of the maze configuration."""

        return f"HEIGHT: {self.height}\n" \
            f"Width: {self.width}\n" \
            f"ENTRY: {self.entry}\n" \
            f"Exit: {self.exit}\n" \
            f"Output file: {self.output_file}\n" \
            f"PERFECT: {self.perfect}\n" \
            f"Seed: {self.seed}\n" \
            f"Algorithm: {self.algorithm}\n" \
            f"PERFECT centered: {self.pcentered}"
