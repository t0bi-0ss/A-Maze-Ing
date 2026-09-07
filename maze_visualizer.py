"""ASCII rendering utilities for visualizing generated mazes and solutions."""

import itertools
import maze_generator

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

# Box-drawing characters for grid intersections (up, right, down, left)
_BOX_JUNCTIONS: dict[tuple[bool, bool, bool, bool], str] = {
    (False, False, False, False): " ",
    (True, False, False, False): "│",
    (False, False, True, False): "│",
    (True, False, True, False): "│",
    (False, False, False, True): "─",
    (False, True, False, False): "─",
    (False, True, False, True): "─",
    (False, True, True, False): "┌",
    (False, False, True, True): "┐",
    (True, True, False, False): "└",
    (True, False, False, True): "┘",
    (True, True, True, False): "├",
    (True, False, True, True): "┤",
    (False, True, True, True): "┬",
    (True, True, False, True): "┴",
    (True, True, True, True): "┼"
}

# Renderizator selector
RENDERIZATORS_ITERATOR = itertools.cycle(
    [
        "thick",
        "slender"
    ]
)


class MazeVisualizer:
    """Render a maze as an ASCII layout with optional path highlighting."""

    def __init__(self, route: list[tuple[int, int]],
                 start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Initialize the visualizer state and color palette.

        Args:
            route: Full path coordinates currently associated with the maze.
            start: Starting cell coordinate.
            end: Exit cell coordinate.
        """
        self.full_route = route
        self.start = start
        self.end = end
        self.show_path = False
        self.renderizator_selector = next(RENDERIZATORS_ITERATOR)
        self._palette_iterator = itertools.cycle(COLOR_PALETTES)
        (self.current_wall, self.current_42,
         self.current_route) = next(self._palette_iterator)

    def render_ascii_thick(
            self, maze: maze_generator.Maze, width: int
    ) -> None:
        """Print a maze matrix as a colored ASCII representation.

        Args:
            maze: 2D list of wall-bit values representing the maze.
        """

        import helper_f

        if not maze:
            print("ERROR: The maze is empty")
            return
        valid_rows = []
        common_width = width
        matrix = helper_f.matrix_converter(maze, width)
        for row in matrix:
            if (isinstance(row, list) and len(row) > 0 and
                    (all(isinstance(x, int) for x in row)) and
                    (len(row) == common_width)):
                valid_rows.append(row)
        if not valid_rows or len(valid_rows) != len(matrix):
            print(f"len valid rows: {len(valid_rows)}")
            print(f"len matrix: {len(matrix)}")
            print("Error: The maze matrix is invalid.")
            return

        columns = width
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
        for f in range(len(matrix)):
            body_line_top = self.current_wall + BLOCK + RESET_COLOR
            body_line_bottom = self.current_wall + BLOCK + RESET_COLOR

            for c in range(columns):
                v = matrix[f][c]
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
                    v_next = matrix[f][c + 1]
                    c2_42 = (v_next & LOCKED_CELL) == LOCKED_CELL

                    next_horizontal = False
                    if self.show_path:
                        for i in range(len(self.full_route) - 1):
                            current = self.full_route[i]
                            next_pt = self.full_route[i + 1]
                            if (current == (f, c) and
                                next_pt == (f, c + 1)) or (
                                    current == (f, c + 1) and next_pt == (f, c)
                            ):
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
            if f < len(matrix) - 1:
                connector_line = self.current_wall + BLOCK + RESET_COLOR
                for c in range(columns):
                    v = matrix[f][c]
                    v_bottom = matrix[f + 1][c]

                    c1_42 = (v & LOCKED_CELL) == LOCKED_CELL
                    c3_42 = (v_bottom & LOCKED_CELL) == LOCKED_CELL

                    next_vertical = False
                    if self.show_path:
                        for i in range(len(self.full_route) - 1):
                            current = self.full_route[i]
                            next_pt = self.full_route[i + 1]
                            if (current == (f, c) and
                                next_pt == (f + 1, c)) or (
                                    current == (f + 1, c) and next_pt == (f, c)
                            ):
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
                        v_right = matrix[f][c + 1]
                        v_bot_right = matrix[f + 1][c + 1]

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

    def render_ascii_slender(
            self, maze: maze_generator.Maze, width: int
    ) -> None:
        """Render the maze with thin walls and open corridors
        to the terminal.

        Args:
            maze: Flat list or generator data of maze cells.
            width: Number of cells per row.
        """
        import helper_f

        if not maze:
            print("ERROR: The maze is empty")
            return

        matrix = helper_f.matrix_converter(maze, width)
        if not matrix:
            print("Error: The maze matrix is invalid.")
            return

        rows = len(matrix)
        cols = width
        reset = "\033[0m"

        # Theme colors
        wall_col = self.current_wall
        route_col = self.current_route
        block_42_col = self.current_42

        # Start and Exit highlight colors (matching original: vibrant
        # orange start, neon lime end)
        start_col = "\033[38;5;208m"
        end_col = "\033[38;5;118m"

        # Path connections set for O(1) membership checks
        set_ruta = set(self.full_route) if self.show_path else set()

        # Build pair set of consecutive route steps: {(cell_a, cell_b), ...}
        route_edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
        if self.show_path and len(self.full_route) > 1:
            for i in range(len(self.full_route) - 1):
                c1 = self.full_route[i]
                c2 = self.full_route[i + 1]
                route_edges.add((c1, c2))
                route_edges.add((c2, c1))

        def is_horiz_wall(r: int, c: int) -> bool:
            """Check if horizontal wall segment exists between
            row r-1 and r at col c."""
            if r == 0 or r == rows:
                return True
            top_cell = matrix[r - 1][c]
            bot_cell = matrix[r][c]
            return bool((top_cell & WALL_SOUTH) or (bot_cell & WALL_NORTH))

        def is_vert_wall(r: int, c: int) -> bool:
            """Check if vertical wall segment exists between col
            c-1 and c at row r."""
            if c == 0 or c == cols:
                return True
            left_cell = matrix[r][c - 1]
            right_cell = matrix[r][c]
            return bool((left_cell & WALL_EAST) or (right_cell & WALL_WEST))

        # Render top border down to bottom border
        for r in range(rows + 1):
            # 1. HORIZONTAL LINE (Intersections & Horizontal Walls / Doorways)
            h_line_parts: list[str] = []
            for c in range(cols + 1):
                # Intersection corner at (r, c)
                up = (r > 0) and is_vert_wall(r - 1, c)
                down = (r < rows) and is_vert_wall(r, c)
                left = (c > 0) and is_horiz_wall(r, c - 1)
                right = (c < cols) and is_horiz_wall(r, c)

                junction_char = _BOX_JUNCTIONS.get((
                    up, right, down, left), "┼")
                h_line_parts.append(wall_col + junction_char + reset)

                # Horizontal wall or doorway between vertex
                # (r, c) and (r, c + 1)
                if c < cols:
                    if is_horiz_wall(r, c):
                        h_line_parts.append(wall_col + "───" + reset)
                    else:
                        # Open doorway between (r-1, c) and (r, c)
                        if ((r - 1, c), (r, c)) in route_edges:
                            # Solution path passing vertically through doorway
                            h_line_parts.append(route_col + " │ " + reset)
                        else:
                            h_line_parts.append("   ")

            print("".join(h_line_parts))

            # 2. CELL INTERIOR LINE (Vertical walls & Cell interiors)
            if r < rows:
                c_line_parts: list[str] = []
                for c in range(cols + 1):
                    # Vertical wall or doorway on the left of cell (r, c)
                    if is_vert_wall(r, c):
                        c_line_parts.append(wall_col + "│" + reset)
                    else:
                        # Open doorway between (r, c-1) and (r, c)
                        if ((r, c - 1), (r, c)) in route_edges:
                            # Solution path passing
                            # horizontally through doorway
                            c_line_parts.append(route_col + "─" + reset)
                        else:
                            c_line_parts.append(" ")

                    # Inside cell (r, c) (3 characters wide)
                    if c < cols:
                        val = matrix[r][c]
                        is_locked = (val & LOCKED_CELL) == LOCKED_CELL

                        if (r, c) == self.start:
                            c_line_parts.append(start_col + "███" + reset)
                        elif (r, c) == self.end:
                            c_line_parts.append(end_col + "███" + reset)
                        elif is_locked:
                            # 42 pattern or locked obstacle block
                            c_line_parts.append(block_42_col + "███" + reset)
                        elif (r, c) in set_ruta:
                            # Detect which directions connect to this cell
                            has_n = ((r, c), (r - 1, c)) in route_edges
                            has_s = ((r, c), (r + 1, c)) in route_edges
                            has_e = ((r, c), (r, c + 1)) in route_edges
                            has_w = ((r, c), (r, c - 1)) in route_edges

                            if has_w and has_e:
                                glyph = "───"
                            elif has_n and has_s:
                                glyph = " │ "
                            elif has_n and has_e:
                                glyph = " └─"
                            elif has_n and has_w:
                                glyph = "─┘ "
                            elif has_s and has_e:
                                glyph = " ┌─"
                            elif has_s and has_w:
                                glyph = "─┐ "
                            elif has_e:
                                glyph = " ──"
                            elif has_w:
                                glyph = "── "
                            elif has_n or has_s:
                                glyph = " │ "
                            else:
                                glyph = " · "
                            c_line_parts.append(route_col + glyph + reset)
                        else:
                            c_line_parts.append("   ")

                print("".join(c_line_parts))

    def change_color_palette(self) -> None:
        """Advance to the next predefined color palette.

        This updates the wall, static-block, and route colors used during the
        next render.
        """
        (self.current_wall, self.current_42,
         self.current_route) = next(self._palette_iterator)

    def change_renderizator(self) -> None:
        """
        Advance to the next predefined selector
        """

        self.renderizator_selector = next(RENDERIZATORS_ITERATOR)

    def renderize(
            self,
            maze: maze_generator.Maze,
            width: int
    ) -> None:
        """
        Renders maze according to current selected renderizator
        """
        if self.renderizator_selector == "thick":
            self.render_ascii_thick(maze, width)
        elif self.renderizator_selector == "slender":
            self.render_ascii_slender(maze, width)
        else:
            raise SystemExit(
                "An error occured with current selected"
                "renderizator: Unrecognized renderizator"
            )
