from configparser import ConfigParser, ParsingError

import sys

from pydantic import ValidationError, BaseModel, Field, model_validator

from typing_extensions import Self

from typing import Literal

"""
Pending DocString
"""


class MazeConfiguration(BaseModel):
    """
    BaseModel for maze configuration
    """

    width: int = Field(gt=2, le=42)
    height: int = Field(gt=2, le=42)
    entry: str = Field(min_length=3)
    exit: str = Field(min_length=3)
    output_file: str = Field(
        min_length=5,
        max_length=260,
        pattern=r"^[a-zA-Z0-9._-]+$"
    )
    perfect: bool
    seed: str | int | float | bytes | None = None
    algorithm: Literal["prism", "backtracking", "gt"]
    perfect_centered: bool

    @model_validator(mode="after")
    def validate_configuration(self) -> Self:
        """
        Validates 'entry' and 'exit' before instatiation
        """

        try:
            assert self.exit.split(',') != self.entry.split(',')
        except AssertionError:
            raise AssertionError(
                "ERROR: 'ENTRY' and 'EXIT' coordinates must be different"
            )

        def validate_pos(pos: str, name: str) -> None:
            """
            validates both 'entry' and 'exit' formats
            """

            pos_list = pos.split(",")
            if len(pos_list) != 2:
                raise ValueError(
                    f"{name} must be two integers (ONLY)"
                    " separated by a SINGLE comma"
                )

            # Check if either of it's elements are not an int or negative
            for item in pos_list:
                try:
                    assert int(item) >= 0
                except ValueError as msg:
                    raise ValueError(
                        f"ERROR in '{name}'\n" + str(msg)
                    )
                except AssertionError:
                    raise AssertionError(
                        f"ERROR in '{name}'\n"
                        f"Negative value found:{item}"
                    )

            # Check if either of it's elements exceeds maze boundaries
            for item in pos_list:
                try:
                    assert self.height > int(item)
                    assert self.width > int(item)
                except AssertionError:
                    raise AssertionError(
                        f"ERROR in '{name}'\n"
                        f"Value exceeds maze boundaries: {item}"
                    )

        validate_pos(self.exit, "EXIT")
        validate_pos(self.entry, "ENTRY")

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
            f"Algorithm: {self.algorithm}"


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
        sys.exit()
    except ParsingError as msg:
        print("ERROR: invalid syntax for 'config' file")
        print(msg)
        sys.exit()

    config_vars = dict(parser['TOP'])

    if 'algorithm' not in config_vars:
        config_vars['algorithm'] = 'gt'

    if 'seed' not in config_vars:
        config_vars['seed'] = None

    for key in ['width', 'height']:
        try:
            int(config_vars[key])
        except ValueError as msg:
            print(f"ERROR in '{key}' parameter value:", msg)
            sys.exit()

    if 'perfect_centered' not in config_vars:
        config_vars['perfect_centered'] = True

    try:
        maze_config = MazeConfiguration(
            width=int(config_vars['width']),
            height=int(config_vars['height']),
            entry=config_vars['entry'].replace(" ", ""),
            exit=config_vars['exit'].replace(" ", ""),
            output_file=config_vars['output_file'],
            perfect=parser.getboolean('TOP', 'perfect'),
            algorithm=config_vars['algorithm'],
            seed=config_vars['seed'],
            perfect_centered=parser.getboolean['TOP', 'perfect_centered']
        )
    except KeyError as msg:
        print(f"KeyError: key {msg} is missing from config file")
        sys.exit()
    except ValidationError as msg:
        print(
            f"ERROR in '{str(msg.errors()[0]['loc'][0])}' config parameter: ",
            end=""
        )
        print(str(msg.errors()[0]['msg']))
        sys.exit()
    except ValueError as msg:
        print("ERROR: 'PERFECT' or 'PERFECT_CENTERED' parameter:", msg)
        sys.exit()

    return maze_config
