"""Interactive console menus for generating, viewing, and managing mazes."""

from maze_generator import path_finder, MazeGenerator

import maze_visualizer

import helper_f

import sys

import transcripter

from time import sleep


def _visualizer_route_update(
        maze: MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer
) -> None:
    """Update the visualizer route based on the current maze solution.

    Args:
        maze_generator: Maze generator instance with the current maze state.
        visualizer: Visualizer whose route should be refreshed.
    """

    solution = path_finder(
        maze.maze,
        maze.ENTRY,
        maze.EXIT,
        maze.WIDTH
    )
    visualizer.start = maze.ENTRY
    visualizer.end = maze.EXIT
    route = helper_f.plot_route(visualizer.start, solution)
    visualizer.full_route = route


def interactive_menu(
        maze: MazeGenerator,
        visualizer: maze_visualizer.MazeVisualizer,
) -> None:
    """Run the interactive menu loop for maze generation and navigation.

    Args:
        maze: Generator controlling the current maze structure.
        visualizer: Renderer used to display the maze and route.
    """

    animation_toggle = False
    original = 1
    original_seed = maze.SEED

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
            print("\nKeyboardInterruptError")
            sleep(1)
            transcripter.transcripter(maze)
            print("Exiting program...")
            sleep(1)
            helper_f.clear()
            break
        match choice:
            case "1":  # Toggle animation
                animation_toggle = not animation_toggle
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer
                )
            case "2":  # Re-generate and visualize
                helper_f.regenerate_maze(
                    maze=maze,
                )
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
            case "3":  # New maze
                original = 0
                helper_f.regenerate_maze(
                    maze=maze,
                    new_maze=True
                )
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
                _visualizer_route_update(maze, visualizer)
            case "4":  # Solution path
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                    show_path=not visualizer.show_path
                )
            case "5":  # Color
                helper_f.clear()
                visualizer.change_color_palette()
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer
                )
            case "6":  # Original
                if original:
                    print("Current maze is already the original one")
                    sleep(2)
                    helper_f.maze_rendering(
                        maze=maze,
                        visualizer=visualizer
                    )
                else:
                    original = 1
                    maze.SEED = original_seed
                    helper_f.regenerate_maze(
                        maze=maze
                    )
                    helper_f.maze_rendering(
                        maze=maze,
                        visualizer=visualizer,
                        animated=animation_toggle
                    )
                    _visualizer_route_update(maze, visualizer)
            case "7":  # Output file
                transcripter.transcripter(maze)
                # maze.rng = random.Random(maze.SEED)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                )
            case "8":  # Re-load config
                maze = helper_f.load_config(sys.argv[1])
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                )
                _visualizer_route_update(maze, visualizer)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
            case "9":  # Exit
                transcripter.transcripter(maze)
                print("Exiting program.")
                sleep(1)
                helper_f.clear()
                break
            case _:
                print("Invalid option. Please try again.")
                sleep(2)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                )
