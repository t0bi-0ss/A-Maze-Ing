from configparser import ConfigParser, ParsingError, InterpolationSyntaxError

from pydantic import ValidationError, BaseModel, Field, model_validator

from typing_extensions import Self

from typing import Literal

import random

"""
Pending DocString
"""


class InvalidTerminalNodesError(Exception):
    """
    Exception raised when either of the terminal nodes is invalid
    """


class MazeConfiguration(BaseModel):
    """
    BaseModel for maze configuration
    """

    width: int = Field(gt=2, le=25)
    height: int = Field(gt=2, le=25)
    entry: tuple[str, str]
    exit: tuple[str, str]
    output_file: str = Field(
        min_length=5,
        max_length=260,
        pattern=r"^[a-zA-Z0-9._-]+$"
    )
    perfect: bool
    seed: str | int | float | bytes | None = None
    algorithm: Literal["prism", "backtracking", "gt"] = Field(default="gt")
    perfect_centered: bool

    @staticmethod
    def validate_pos(
        maze_width: int,
        maze_height: int,
        pos: tuple[str, str],
        name: str
    ) -> None:
        """
        Validates position ('pos') values also considering max_value
        """

        # Check if either of it's elements are not an int or negative
        try:
            x = int(pos[0])
            y = int(pos[1])
        except ValueError as msg:
            raise ValueError(
                f"'{name}'\n" + str(msg)
            )

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

    @model_validator(mode="after")
    def validate_configuration(self) -> Self:
        """
        Validates 'entry' and 'exit' before instatiation
        """

        entry_copy = [coord.replace(" ", "") for coord in self.entry]
        exit_copy = [coord.replace(" ", "") for coord in self.exit]
        if entry_copy == exit_copy:
            raise ValueError("Entry and exit coordinates must differ")
        try:
            self.validate_pos(self.width, self.height, self.exit, "EXIT")
            self.validate_pos(self.width, self.height, self.entry, "ENTRY")
        except ValueError as msg:
            raise ValueError(msg)
        return self

    def __str__(self) -> str:
        """
        String representation
        """

        return f"Height: {self.height}\n" \
            f"Width: {self.width}\n" \
            f"Entry: {self.entry}\n" \
            f"Exit: {self.exit}\n" \
            f"Output file: {self.output_file}\n" \
            f"Perfect: {self.perfect}\n" \
            f"Seed: {self.seed}\n" \
            f"Algorithm: {self.algorithm}\n" \
            f"Perfect centered: {self.perfect_centered}"


def get_config(config_file: str) -> MazeConfiguration:
    """
    Get configuration from config file
    """

    parser = ConfigParser()

    try:
        with open(config_file) as stream:
            parser.read_string("[TOP]\n" + stream.read())
    except (
            UnicodeDecodeError,
            ValueError,
            OSError,
            PermissionError,
            IsADirectoryError,
            FileNotFoundError,
    ) as msg:
        print(msg)
        raise SystemExit
    except ParsingError as msg:
        print("ERROR: invalid syntax for 'config' file")
        print(msg)
        raise SystemExit
    except InterpolationSyntaxError as msg:
        raise SystemExit(msg)

    # Get dict of configparser options
    config_vars = dict(parser['TOP'])

    try:
        maze_config = MazeConfiguration(
            width=config_vars['width'],
            height=config_vars['height'],
            entry=config_vars['entry'].split(','),
            exit=config_vars['exit'].split(','),
            output_file=config_vars['output_file'],
            perfect=config_vars.get('perfect', True),
            algorithm=config_vars.get('algorithm', 'gt'),
            seed=config_vars.get('seed', random.random()),
            perfect_centered=config_vars.get('perfect_centered', True)
        )
    except KeyError as msg:
        raise SystemExit(
            f"KeyError: key {str(msg).upper()} is missing from config file"
        )
    except ValidationError as msg:
        msg_d = msg.errors()[0]
        loc = msg_d.get('loc')
        input = msg_d['input']
        if loc:
            message = f"{loc[0].upper()} = {input}: {msg_d['msg']}"
        else:
            message = f"{msg_d['msg'].removeprefix('Value error, ')}"
        raise SystemExit(
            "ERROR: invalid option " + message
        )

    return maze_config
