import sys
import itertools
from maze_generator import MazeGenerator
from parser import get_config, MazeConfiguration
from path_finder import path_finder
from transcripter import transcripter
from time import sleep
import os

# Bitmask
WALL_NORTH = 1 << 0  # 0001
WALL_EAST = 1 << 1  # 0010
WALL_SOUTH = 1 << 2  # 0100
WALL_WEST = 1 << 3  # 1000
LOCKED_CELL = WALL_NORTH | WALL_EAST | WALL_SOUTH | WALL_WEST

# Color combination palette (Walls, Blocks 42, Solution)
COLOR_PALETTES: tuple[tuple[str, str, str], ...] = (
    ("\033[34m", "\033[38;5;18m", "\033[1;31m"),
    ("\033[37m", "\033[38;5;250m", "\033[1;32m"),
    ("\033[35m", "\033[38;5;93m", "\033[1;33m"),
    ("\033[33m", "\033[38;5;130m", "\033[1;36m"),
)


def plot_route(start: tuple[int, int], steps: str) -> list[tuple[int, int]]:
    """Take the start and go for the end with the route"""
    route_coordinates = [start]
    f, c = start

    movements = {
        'E': (0, 1),
        'W': (0, -1),
        'S': (1, 0),
        'N': (-1, 0)
    }

    for step in steps.upper():
        if step in movements:
            df, dc = movements[step]
            f += df
            c += dc
            route_coordinates.append((f, c))

    return route_coordinates


class MazeVisualizer:
    """Class responsible for visual representation and interactivity"""

    def __init__(self, matrix: list[list[int]], route: list[tuple[int, int]],
                 start: tuple[int, int], end: tuple[int, int]) -> None:
        valid_rows = []
        for row in matrix:
            if (isinstance(row, list) and len(row) > 0 and
                    all(isinstance(x, int) for x in row)):
                valid_rows.append(row)

        if valid_rows:
            common_width = len(valid_rows[0])
            self.matrix = [f for f in valid_rows if len(f) == common_width]
        else:
            self.matrix = []

        self.full_route = route
        self.start = start
        self.end = end
        self.show_path = False

        self._palette_iterator = itertools.cycle(COLOR_PALETTES)
        (self.current_wall, self.current_42,
         self.current_route) = next(self._palette_iterator)

    def render_ascii(self) -> None:
        """Generate a visual representation of the maze"""
        rows = len(self.matrix)
        if rows == 0:
            print("Error: The maze matrix is empty or invalid.")
            return

        columns = len(self.matrix[0])
        RESET_COLOR = "\033[0m"

        # Start and end blocks
        START_COLOR = "\033[38;5;208m"
        STARTER_BLOCK = "████"
        END_COLOR = "\033[38;5;118m"
        END_BLOCK = "████"

        # Standard blocks
        BLOCK = "████"
        EMPTY = "    "

        set_ruta = set(self.full_route) if self.show_path else set()

        # Top of the maze
        for _ in range(2):
            print(self.current_wall + (BLOCK * (columns * 2 + 1)) +
                  RESET_COLOR)

        # Body path
        for f in range(rows):
            body_line_top = self.current_wall + BLOCK + RESET_COLOR
            body_line_bottom = self.current_wall + BLOCK + RESET_COLOR

            for c in range(columns):
                v = self.matrix[f][c]
                c1_42 = (v & LOCKED_CELL) == LOCKED_CELL

                if (f, c) == self.start:
                    body_line_top += START_COLOR + STARTER_BLOCK + RESET_COLOR
                    body_line_bottom += (START_COLOR + STARTER_BLOCK +
                                         RESET_COLOR)
                elif (f, c) == self.end:
                    body_line_top += END_COLOR + END_BLOCK + RESET_COLOR
                    body_line_bottom += END_COLOR + END_BLOCK + RESET_COLOR
                elif (f, c) in set_ruta:
                    # Dynamic mapping of route connections for the current cell
                    has_north = False
                    has_south = False
                    has_east = False
                    has_west = False

                    for i in range(len(self.full_route) - 1):
                        curr = self.full_route[i]
                        nxt = self.full_route[i + 1]
                        if curr == (f, c):
                            if nxt == (f - 1, c):
                                has_north = True
                            elif nxt == (f + 1, c):
                                has_south = True
                            elif nxt == (f, c + 1):
                                has_east = True
                            elif nxt == (f, c - 1):
                                has_west = True
                        elif nxt == (f, c):
                            if curr == (f - 1, c):
                                has_north = True
                            elif curr == (f + 1, c):
                                has_south = True
                            elif curr == (f, c + 1):
                                has_east = True
                            elif curr == (f, c - 1):
                                has_west = True

                    # 4 top chars
                    t_chars = [" ", " ", " ", " "]
                    t_chars[0] = "▄" if has_west else " "
                    t_chars[3] = "▄" if has_east else " "
                    # The central cells (indices 1 and 2) adapt
                    # to vertical or horizontal flow.
                    has_e_w_s = has_east or has_west or has_south
                    t_chars[1] = (
                        "█" if has_north else ("▄" if has_e_w_s else " "))
                    t_chars[2] = (
                        "█" if has_north else ("▄" if has_e_w_s else " "))

                    # 4 bottom chars
                    b_chars = [" ", " ", " ", " "]
                    b_chars[0] = "▀" if has_west else " "
                    b_chars[3] = "▀" if has_east else " "
                    has_e_w_n = has_east or has_west or has_north
                    b_chars[1] = (
                        "█" if has_south else ("▀" if has_e_w_n else " "))
                    b_chars[2] = (
                        "█" if has_south else ("▀" if has_e_w_n else " "))

                    body_line_top += (self.current_route +
                                      "".join(t_chars) + RESET_COLOR)
                    body_line_bottom += (self.current_route +
                                         "".join(b_chars) + RESET_COLOR)
                elif c1_42:
                    body_line_top += self.current_42 + BLOCK + RESET_COLOR
                    body_line_bottom += self.current_42 + BLOCK + RESET_COLOR
                else:
                    body_line_top += RESET_COLOR + EMPTY + RESET_COLOR
                    body_line_bottom += RESET_COLOR + EMPTY + RESET_COLOR

                # East Wall (Intermediate side walls)
                if c < columns - 1:
                    v_next = self.matrix[f][c + 1]
                    c2_42 = (v_next & LOCKED_CELL) == LOCKED_CELL

                    next_horizontal = False
                    if self.show_path:
                        for i in range(len(self.full_route) - 1):
                            current = self.full_route[i]
                            next_pt = self.full_route[i + 1]
                            if (current == (f, c) and
                                next_pt == (f, c + 1)) or (
                                 current == (f, c + 1) and next_pt == (f, c)):
                                next_horizontal = True
                                break

                    if next_horizontal:
                        body_line_top += (self.current_route +
                                          "▄▄▄▄" + RESET_COLOR)
                        body_line_bottom += (self.current_route +
                                             "▀▀▀▀" + RESET_COLOR)
                    elif c1_42 and c2_42:
                        body_line_top += (self.current_wall +
                                          BLOCK + RESET_COLOR)
                        body_line_bottom += (self.current_wall +
                                             BLOCK + RESET_COLOR)
                    elif (v & WALL_EAST) or (v_next & WALL_WEST):
                        body_line_top += (self.current_wall +
                                          BLOCK + RESET_COLOR)
                        body_line_bottom += (self.current_wall +
                                             BLOCK + RESET_COLOR)
                    else:
                        body_line_top += RESET_COLOR + EMPTY + RESET_COLOR
                        body_line_bottom += RESET_COLOR + EMPTY + RESET_COLOR

            body_line_top += self.current_wall + BLOCK + RESET_COLOR
            body_line_bottom += self.current_wall + BLOCK + RESET_COLOR

            print(body_line_top)
            print(body_line_bottom)

            # --- Vertical Connections and Intersections ---
            if f < rows - 1:
                connector_line = self.current_wall + BLOCK + RESET_COLOR

                for c in range(columns):
                    v = self.matrix[f][c]
                    v_bottom = self.matrix[f + 1][c]

                    c1_42 = (v & LOCKED_CELL) == LOCKED_CELL
                    c3_42 = (v_bottom & LOCKED_CELL) == LOCKED_CELL

                    next_vertical = False
                    if self.show_path:
                        for i in range(len(self.full_route) - 1):
                            current = self.full_route[i]
                            next_pt = self.full_route[i + 1]
                            if (current == (f, c) and
                                next_pt == (f + 1, c)) or (
                                 current == (f + 1, c) and next_pt == (f, c)):
                                next_vertical = True
                                break

                    if next_vertical:
                        connector_line += (self.current_route +
                                           " ██ " + RESET_COLOR)
                    elif c1_42 and c3_42:
                        connector_line += (self.current_wall +
                                           BLOCK + RESET_COLOR)
                    elif (v & WALL_SOUTH) or (v_bottom & WALL_NORTH):
                        connector_line += (self.current_wall +
                                           BLOCK + RESET_COLOR)
                    else:
                        connector_line += RESET_COLOR + EMPTY + RESET_COLOR

                    # Diagonal intersection
                    if c < columns - 1:
                        v_right = self.matrix[f][c + 1]
                        v_bot_right = self.matrix[f + 1][c + 1]

                        c2_42 = (v_right & LOCKED_CELL) == LOCKED_CELL
                        c4_42 = (v_bot_right & LOCKED_CELL) == LOCKED_CELL

                        if c1_42 or c2_42 or c3_42 or c4_42:
                            connector_line += (self.current_wall +
                                               BLOCK + RESET_COLOR)
                        else:
                            connector_line += (self.current_wall +
                                               BLOCK + RESET_COLOR)

                connector_line += self.current_wall + BLOCK + RESET_COLOR

                for _ in range(2):
                    print(connector_line)

        # 3. Bottom of the maze
        for _ in range(2):
            print(self.current_wall + (BLOCK * (columns * 2 + 1))
                  + RESET_COLOR)

    def change_color_palette(self) -> None:
        (self.current_wall, self.current_42,
         self.current_route) = next(self._palette_iterator)

    @staticmethod
    def generate_maze(
        configuration: MazeConfiguration,
        visualizer: MazeVisualizer,
        route_coordinates: list[tuple[int, int]],
        start: tuple[int, int],
        end: tuple[int, int],
        seed: float
    ) -> None:
        from time import sleep
        import os
        import parser_output

        generator = MazeGenerator(
                width=configuration.width,
                height=configuration.height,
                entry=configuration.entry,
                exit=configuration.exit,
                perfect=configuration.perfect,
                seed=seed,
                perfect_centered=configuration.perfect_centered
            )

        for _ in generator.generator():
            os.system('cls' if os.name == 'nt' else 'clear')
            transcripter(generator, "maze.txt")
            matrix = parser_output.load_configuration("maze.txt")[0]
            visualizer = MazeVisualizer(
                matrix, route_coordinates, start, end
                )
            visualizer.render_ascii()
            # sleep(.1)

    @staticmethod
    def interactive_menu(
        configuration: MazeConfiguration,
        visualizer: MazeVisualizer,
        route_coordinates: list[tuple[int, int]],
        start: tuple[int, int],
        end: tuple[int, int],
        seed: float
    ) -> None:
        while True:
            print("\n=== A-Maze-ing Interactive Menu ===")
            print("1. Re-generate maze")
            print("2. Show / Hide the solution path")
            print("3. Next Color Combination")
            print("4. Exit")

            try:
                choice = input("Select an option (1-3): ").strip()
                print()
            except (EOFError, KeyboardInterrupt):
                sys.exit()
            match choice:
                case "1":
                    MazeVisualizer.generate_maze(
                        configuration,
                        visualizer,
                        route_coordinates,
                        start,
                        end,
                        seed
                    )
                case "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    visualizer.show_path = not visualizer.show_path
                    visualizer.render_ascii()
                case "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    visualizer.change_color_palette()
                    visualizer.render_ascii()
                case "4":
                    print("Exiting program.")
                    break
                case _:
                    print("Invalid option. Please try again.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <config_file>")
        sys.exit(1)

    config_filename = sys.argv[1]

    try:
        import parser_output
        matrix, start, end, ruta_str = (parser_output.
                                        load_configuration(config_filename))
        route_coordinates = plot_route(start, ruta_str)

    except ImportError:
        print("Error: Could not import module 'parser'."
              " Ensure parser.py is in the same directory.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{config_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading or parsing configuration: {e}")
        sys.exit(1)

    print("\n=== Maze ===")
    configuration = get_config("config.txt")
    maze = MazeGenerator(
            width=configuration.width,
            height=configuration.height,
            entry=configuration.entry,
            exit=configuration.exit,
            perfect=configuration.perfect,
            seed=configuration.seed,
            perfect_centered=configuration.perfect_centered
        )

    for _ in maze.generator():
        os.system('cls' if os.name == 'nt' else 'clear')
        transcripter(maze, "maze.txt")
        matrix = parser_output.load_configuration("maze.txt")[0]
        visualizer = MazeVisualizer(matrix, route_coordinates, start, end)
        visualizer.render_ascii()
        # sleep(.1)
    solution = path_finder(maze.maze, maze.ENTRY, maze.EXIT, maze.WIDTH)
    transcripter(maze, "maze.txt", solution)
    visualizer.interactive_menu(
        configuration,
        visualizer,
        route_coordinates,
        start,
        end,
        maze.SEED
    )


if __name__ == "__main__":
    main()
