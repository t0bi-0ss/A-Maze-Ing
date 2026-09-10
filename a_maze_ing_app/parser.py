"""Configuration parsing and validation utilities for the maze project."""
from mazegen import MazeGenerator
from configparser import ConfigParser, ParsingError, \
    InterpolationSyntaxError, DuplicateOptionError, DuplicateSectionError
from pydantic import ValidationError


def get_configurated_maze_generator(config_file: str) -> MazeGenerator:
    """Read and validate a maze configuration from a file.

    Args:
        config_file: Path to the configuration file.

    Returns:
        A parsed and validated ``MazeConfiguration`` object.
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
    except (DuplicateOptionError, DuplicateSectionError) as msg:
        raise SystemExit(msg)

    # Get dict of configparser options
    config_vars = {
        key.lower(): value for key, value in dict(parser['TOP']).items()
    }

    try:
        maze_generator = MazeGenerator.model_validate(config_vars)
    except KeyError as msg:
        raise SystemExit(
            f"KeyError: key {str(msg).upper()} is missing from config file"
        )
    except ValidationError as msg:
        msg_d = msg.errors()[0]
        loc = msg_d.get('loc')
        input = msg_d['input']
        if loc:
            message = f"{str(loc[0]).upper()} = {input}: {msg_d['msg']}"
        else:
            message = f"{msg_d['msg'].removeprefix('Value error, ')}"
        raise SystemExit(
            "ERROR: invalid option " + message
        )

    return maze_generator
