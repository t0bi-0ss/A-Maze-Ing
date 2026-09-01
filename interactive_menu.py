import maze_generator

import maze_visualizer

import path_finder

import helper_f

import random

import sys

import transcripter

from time import sleep


def interactive_menu(
        maze_generator: maze_generator.MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer,
) -> None:

    animation_toggle = 1
    original = 1
    original_seed = maze_generator.SEED

    # converted_matrix = helper_f.matrix_converter(
    #                     maze_generator.maze,
    #                     maze_generator.WIDTH
    #                     )

    while True:
        options = [
            f"Toggle Animation. {'OFF' if animation_toggle else 'ON'}",
            "Re-generate maze",
            "Generate new maze",
            "Show/Hide solution path",
            "Next Color Combination",
            "Recover original maze",
            "Generate output file",
            "Re-load config",
            "Exit"
        ]
        print("\n=== A-Maze-ing Interactive Menu ===")
        for num, option in enumerate(options):
            print(f"{num + 1}. {option}")

        try:
            choice = input(
                f"Select an option (1-{len(options)}): "
                ).strip()
            print()
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        match choice:
            case "1":  # Toggle animation
                animation_toggle = 0 if animation_toggle else 1
                helper_f.clear()
                helper_f.visualize_generation(
                    animation_toggle, maze_generator, visualizer
                )
            case "2":  # Re-generate
                helper_f.visualize_generation(
                    animation_toggle, maze_generator, visualizer
                )
            case "3":  # New maze
                visualizer.show_path = 0
                original = 0
                maze_generator.SEED = random.random()
                helper_f.visualize_generation(
                    animation_toggle, maze_generator, visualizer
                )
                solution = path_finder.path_finder(
                    maze_generator.maze,
                    maze_generator.ENTRY,
                    maze_generator.EXIT,
                    maze_generator.WIDTH
                )
                route = helper_f.plot_route(visualizer.start, solution)
                visualizer.full_route = route
            case "4":  # Solution path
                helper_f.clear()
                visualizer.show_path = not visualizer.show_path
                visualizer.render_ascii(
                    matrix=helper_f.matrix_converter(
                        maze_generator.maze,
                        maze_generator.WIDTH
                        )
                )
            case "5":  # Color
                helper_f.clear()
                visualizer.change_color_palette()
                visualizer.render_ascii(
                    matrix=helper_f.matrix_converter(
                        maze_generator.maze,
                        maze_generator.WIDTH
                        )
                )
            case "6":  # Original
                if original:
                    print("Current maze is already the original one")
                    sleep(2)
                    helper_f.visualize_generation(
                        0, maze_generator, visualizer
                    )
                else:
                    original = 1
                    maze_generator.SEED = original_seed
                    helper_f.visualize_generation(
                        animation_toggle, maze_generator, visualizer
                    )
                    solution = path_finder.path_finder(
                        maze_generator.maze,
                        maze_generator.ENTRY,
                        maze_generator.EXIT,
                        maze_generator.WIDTH
                    )
                    route = helper_f.plot_route(visualizer.start, solution)
                    visualizer.full_route = route
            case "7":  # Output file
                solution = path_finder.path_finder(
                    maze_generator.maze,
                    maze_generator.ENTRY,
                    maze_generator.EXIT,
                    maze_generator.WIDTH
                )
                transcripter.transcripter(maze_generator, "maze.txt", solution)
                maze_generator.rng = random.Random(maze_generator.SEED)
                helper_f.visualize_generation(
                    0, maze_generator, visualizer
                )
            case "8":
                maze_generator = helper_f.load_config(sys.argv[1])
                helper_f.clear()
                visualizer.start = helper_f.convert_pos(maze_generator.ENTRY)
                visualizer.end = helper_f.convert_pos(maze_generator.EXIT)
                helper_f.visualize_generation(
                                        0, maze_generator, visualizer
                                    )
            case "9":  # Exit
                print("Exiting program.")
                break
            case _:
                print("Invalid option. Please try again.")
