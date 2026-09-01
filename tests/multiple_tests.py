"""Regression tests covering parser validation and maze generation setup."""

import maze_generator
import transcripter
import parser
import sys

# to run test: python -m tests.multiple_tests

if __name__ == "__main__":

    file_names = [
            "bad_algorithm",
            "bad_entry_1",
            "bad_entry_2",
            "bad_entry_3",
            "bad_entry_and_exit",
            "bad_exit_1",
            "bad_exit_2",
            "bad_height_1",
            "bad_height_2",
            "bad_height_3",
            "bad_output_file_1",
            "bad_output_file_2",
            "bad_perfect",
            "bad_width_1",
            "bad_width_2",
            "bad_width_3",
            "no_file",
            "no_permission",
            "missing_perfect",
            "missing_key"
        ]
    for file in file_names:
        try:
            print(f"\nRunning '{file}' test:")
            configuration = parser.get_config("tests/" + file + ".txt")
        except SystemExit as msg:
            print(msg)
        else:
            print("No error")

    try:
        print("\nDirectory test:")
        configuration = parser.get_config("tests/some_dir")
    except SystemExit as msg:
        print(msg)
        sys.exit()
    else:
        print("No error")

    print(configuration)
    maze = maze_generator.MazeGenerator(
            width=configuration.width,
            height=configuration.height,
            entry=configuration.entry,
            exit=configuration.exit,
            perfect=configuration.perfect,
            seed=configuration.seed,
            perfect_centered=configuration.perfect_centered
        )

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
    transcripter.transcripter(maze, "maze.txt")
