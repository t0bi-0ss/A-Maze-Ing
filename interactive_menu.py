"""Interactive console menus for generating, viewing, and managing mazes."""

import maze_generator

import maze_visualizer

import path_finder

import helper_f

import sys

import transcripter

from time import sleep


def _visualizer_route_update(
        maze_generator: maze_generator.MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer
) -> None:
    """Update the visualizer route based on the current maze solution.

    Args:
        maze_generator: Maze generator instance with the current maze state.
        visualizer: Visualizer whose route should be refreshed.
    """

    solution = path_finder.path_finder(
        maze_generator.maze,
        maze_generator.ENTRY,
        maze_generator.EXIT,
        maze_generator.WIDTH
    )
    visualizer.start = helper_f.convert_pos(maze_generator.ENTRY)
    visualizer.end = helper_f.convert_pos(maze_generator.EXIT)
    route = helper_f.plot_route(visualizer.start, solution)
    visualizer.full_route = route


def interactive_menu(
        maze_generator: maze_generator.MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer,
) -> None:
    """Run the interactive menu loop for maze generation and navigation.

    Args:
        maze_generator: Generator controlling the current maze structure.
        visualizer: Renderer used to display the maze and route.
    """

    animation_toggle = 0
    original = 1
    original_seed = maze_generator.SEED

    while True:
        options = [
            f"Toggle Animation. {'ON' if animation_toggle else 'OFF'}",
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
            print()
            transcripter.transcripter(maze_generator)
            sys.exit()
        match choice:
            case "1":  # Toggle animation
                animation_toggle = not animation_toggle
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer
                )
            case "2":  # Re-generate and visualize
                helper_f.regenerate_maze(
                    maze=maze_generator,
                )
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
            case "3":  # New maze
                original = 0
                helper_f.regenerate_maze(
                    maze=maze_generator,
                    new_maze=True
                )
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
                _visualizer_route_update(maze_generator, visualizer)
            case "4":  # Solution path
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer,
                    show_path=not visualizer.show_path
                )
            case "5":  # Color
                helper_f.clear()
                visualizer.change_color_palette()
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer
                )
            case "6":  # Original
                if original:
                    print("Current maze is already the original one")
                    sleep(2)
                    helper_f.maze_rendering(
                        maze=maze_generator,
                        visualizer=visualizer
                    )
                else:
                    original = 1
                    maze_generator.SEED = original_seed
                    helper_f.regenerate_maze(
                        maze=maze_generator
                    )
                    helper_f.maze_rendering(
                        maze=maze_generator,
                        visualizer=visualizer,
                        animated=animation_toggle
                    )
                    _visualizer_route_update(maze_generator, visualizer)
            case "7":  # Output file
                transcripter.transcripter(maze_generator)
                # maze_generator.rng = random.Random(maze_generator.SEED)
                helper_f.maze_rendering(
                    maze=maze_generator,
                    visualizer=visualizer,
                )
            case "8":  # Re-load config
                maze_generator = helper_f.load_config(sys.argv[1])
                helper_f.maze_rendering(
                                    maze=maze_generator,
                                    visualizer=visualizer,
                                    animated=animation_toggle
                                )
                _visualizer_route_update(maze_generator, visualizer)
            case "9":  # Exit
                transcripter.transcripter(maze_generator)
                print("Exiting program.")
                break
            case _:
                print("Invalid option. Please try again.")
