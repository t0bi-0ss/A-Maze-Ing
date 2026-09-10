"""CLI entry point for launching the interactive maze application."""

import maze_visualizer

import sys

import helper_f

from collections import deque

from mazegen import path_finder

import interactive_menu

import random

import transcripter

import parser

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("ERROR: Usage: python3 a_maze_ing.py <configfile>")
        sys.exit()

    # Config file name
    config_name = sys.argv[1]

    maze = parser.get_configurated_maze_generator(config_name)

    # Get generators final result
    deque(maze.generator(), maxlen=0)

    # Get maze solution
    solution = path_finder(
        maze.maze, maze.entry, maze.exit, maze.width
    )

    # Get solution route
    route = helper_f.plot_route(maze.entry, solution)

    # Generate first maze.txt
    transcripter.transcripter(maze)

    # Initiate visualizer
    visualizer = maze_visualizer.MazeVisualizer(route, maze.entry, maze.exit)

    # First rendering
    helper_f.maze_rendering(
        maze=maze,
        visualizer=visualizer
    )

    # Restart rng
    maze.rng = random.Random(maze.seed)

    # Menu
    interactive_menu.interactive_menu(maze, visualizer)
