from maze_generator import MazeGenerator


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
    maze.transcript("maze.txt")
