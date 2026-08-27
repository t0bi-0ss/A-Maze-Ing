from maze_generator import MazeGenerator
from path_finder import path_finder

if __name__ == "__main__":

    maze = MazeGenerator(
        15, 15, (0, 0), (3, 3), 0.75, perfect=False, perfect_centered=True
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
    maze.transcript("maze.txt")
    path = path_finder(maze.maze, maze.ENTRY, maze.EXIT, maze.WIDTH)
    print(path)
