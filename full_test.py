import maze_visualizer

import sys

import helper_f

from collections import deque

import path_finder

import interactive_menu

import random

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("len sys", len(sys.argv))
        print("ERROR: 2 files needed")
        sys.exit()

    # Config file name
    config_name = sys.argv[1]

    maze = helper_f.load_config(config_name)

    # Get generators final result
    deque(maze.generator(), maxlen=0)

    # Get maze solution
    solution = path_finder.path_finder(
        maze.maze, maze.ENTRY, maze.EXIT, maze.WIDTH
        )

    # Convert endpoints
    start = helper_f.convert_pos(maze.ENTRY)
    end = helper_f.convert_pos(maze.EXIT)

    # Get solution route
    route = helper_f.plot_route(start, solution)

    # Initiate visualizer
    visualizer = maze_visualizer.MazeVisualizer(route, start, end)
    visualizer.render_ascii(helper_f.matrix_converter(maze.maze, maze.WIDTH))
    # Restart rng
    maze.rng = random.Random(maze.SEED)

    # helper_f.visualize_generation(1, maze, visualizer)
    # Menu
    interactive_menu.interactive_menu(maze, visualizer)
