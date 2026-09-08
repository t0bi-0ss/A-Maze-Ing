"""Interactive console menus for generating, viewing, and managing mazes."""

from maze_generator import path_finder, MazeGenerator

import maze_visualizer

import helper_f

import sys

import transcripter

from time import sleep

from collections import deque


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
        visualizer: maze_visualizer.MazeVisualizer
) -> None:
    """Run the interactive menu loop for maze generation and navigation.

    Args:
        maze: Generator controlling the current maze structure.
        visualizer: Renderer used to display the maze and route.
    """

    animation_toggle = False
    original = 1
    original_seed = maze.seed
    original_selector = maze.SELECTOR

    match maze.SELECTOR:
        case 0:
            current_algorithm = "Backtracking"
        case 1:
            current_algorithm = "Prim's"
        case -1:
            current_algorithm = "Growing Tree"

    while True:
        options = [
            "Toggle Animation. (Status: " +
            ('ON)' if animation_toggle else 'OFF)'),
            "Re-generate maze",
            "Generate new maze",
            "Show/Hide solution path",
            "Next Color Combination",
            "Recover original maze",
            "Generate output file",
            "Re-load config",
            "Switch Visualizer (Current: " +
            (visualizer.renderizator_selector).upper() + ")",
            f"Select algorithm (Current: {current_algorithm})",
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
                _visualizer_route_update(maze, visualizer)
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
                    visualizer=visualizer,
                    show_path=visualizer.show_path
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
                    maze.seed = original_seed
                    maze.SELECTOR = original_selector
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
                # maze.rng = random.Random(maze.seed)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                )
            case "8":  # Re-load config
                maze = helper_f.load_config(sys.argv[1])
                deque(maze.generator(), maxlen=0)
                # helper_f.maze_rendering(
                #     maze=maze,
                #     visualizer=visualizer,
                # )
                _visualizer_route_update(maze, visualizer)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer,
                    animated=animation_toggle
                )
            case "9":  # Render selector
                visualizer.change_renderizator()
                print("Switched visualizer style!")
                sleep(1)
                helper_f.maze_rendering(
                    maze=maze,
                    visualizer=visualizer
                )
            case "10":  # Algorithm
                try:
                    while True:
                        helper_f.maze_rendering(
                            maze=maze,
                            visualizer=visualizer
                        )
                        print(
                            "1.Prim's like\n2.Backtracking like"
                            "\n3.Growing Tree"
                        )
                        try:
                            algo_choice = input("Choice: ")
                        except KeyboardInterrupt:
                            raise KeyboardInterrupt
                        else:
                            match algo_choice:
                                case "1":
                                    maze.SELECTOR = 1
                                case "2":
                                    maze.SELECTOR = 0
                                case "3":
                                    maze.SELECTOR = -1
                                case _:
                                    print(
                                        "Error: unrecognized selection. "
                                        "Try again"
                                    )
                                    sleep(1)
                                    continue
                            match maze.SELECTOR:
                                case 0:
                                    current_algorithm = "Backtracking"
                                case 1:
                                    current_algorithm = "Prim's"
                                case -1:
                                    current_algorithm = "Growing Tree"
                            break
                except KeyboardInterrupt:
                    print("\nKeyboardInterruptError")
                    transcripter.transcripter(maze)
                    print("Exiting program...")
                    sleep(1)
                    helper_f.clear()
                    break
                else:
                    helper_f.maze_rendering(
                        maze=maze,
                        visualizer=visualizer
                    )
            case "11":  # Exit
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
