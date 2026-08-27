from maze_generator import MazeGenerator
from transcripter import transcripter
from parser import get_config

if __name__ == "__main__":

    configuration = get_config("config.txt")
    print(configuration)
    maze = MazeGenerator(
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
    transcripter(maze, "maze.txt")
