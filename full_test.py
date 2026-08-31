import maze_generator

import maze_visualizer

import parser

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

    try:
        configuration = parser.get_config(sys.argv[1])
    except SystemExit as msg:
        print(msg)
        sys.exit()
    else:
        maze = maze_generator.MazeGenerator(
                width=configuration.width,
                height=configuration.height,
                entry=configuration.entry,
                exit=configuration.exit,
                perfect=configuration.perfect,
                seed=configuration.seed,
                perfect_centered=configuration.perfect_centered
            )

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
