def load_configuration(
    file_name: str
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    """
        Reading the maze.txt file
    """
    map_lines: list[list[int]] = []
    meta_lines: list[str] = []
    map_block_finished = False

    with open(file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()

            # An empty line marks the end of reading the hexadecimal matrix
            if not clean_line:
                if len(map_lines) > 0:
                    map_block_finished = True
                continue

            if clean_line.startswith('#'):
                continue

            # Phase 1: Hexadecimal maze extraction
            if not map_block_finished:
                if all(c in "0123456789abcdefABCDEF" for c in clean_line):
                    integer_row = [int(c, 16) for c in clean_line]
                    map_lines.append(integer_row)
                else:
                    map_block_finished = True

            # Phase 2: Sequentially store metadata lines after the empty space
            if map_block_finished and clean_line:
                meta_lines.append(clean_line)

    # Initializing values
    start: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (0, 0)
    path_str: str = ""

    # START
    if len(meta_lines) > 0:
        try:
            start_line = meta_lines[0]
            if ',' in start_line:
                x_str, y_str = start_line.split(',')
                start = (int(y_str.strip()), int(x_str.strip()))
        except Exception:
            pass

    # END
    if len(meta_lines) > 1:
        try:
            end_line = meta_lines[1]
            if ',' in end_line:
                x_str, y_str = end_line.split(',')
                end = (int(y_str.strip()), int(x_str.strip()))
        except Exception:
            pass

    # Solution
    if len(meta_lines) > 2:
        path_str = meta_lines[2].strip()

    return map_lines, start, end, path_str
