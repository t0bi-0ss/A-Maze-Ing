"""CLI entry point for launching the interactive maze application."""

import maze_visualizer

import sys

import helper_f

from collections import deque

from mazegen import path_finder

import interactive_menu

import random

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("ERROR: Usage: python3 a_maze_ing.py <configfile>")
        sys.exit()

    # Config file name
    config_name = sys.argv[1]

    maze = helper_f.load_config(config_name)

    # Get generators final result
    deque(maze.generator(), maxlen=0)

    # Get maze solution
    solution = path_finder(
        maze.maze, maze.ENTRY, maze.EXIT, maze.WIDTH
    )

    # Get solution route
    route = helper_f.plot_route(maze.ENTRY, solution)

    # Initiate visualizer
    visualizer = maze_visualizer.MazeVisualizer(route, maze.ENTRY, maze.EXIT)

    # First rendering
    helper_f.maze_rendering(
        maze=maze,
        visualizer=visualizer
    )

    # Restart rng
    maze.rng = random.Random(maze.seed)

    # Menu
    interactive_menu.interactive_menu(maze, visualizer)
