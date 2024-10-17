# file_parser.py

def parse_coordinates(coord_string):
    """Helper function to parse a string of coordinates in the format (col, row)."""
    coord_string = coord_string.split(')')[0] + ')'
    coord = coord_string.strip('()').split(',')
    return tuple(map(int, coord))

def read_input_file(input_file):
    """Read and parse the input file to extract grid dimensions, markers, goals, and walls."""
    try:
        with open(input_file, 'r') as file:
            # First line: grid dimensions
            first_line = file.readline().strip()
            grid_dimensions = first_line.split(']')[0] + ']'
            rows, cols = map(int, grid_dimensions.strip('[]').split(','))

            # Second line: marker coordinates (column index, row index)
            second_line = file.readline().strip()
            col_idx, row_idx = parse_coordinates(second_line)

            # Third line: goal states (coordinates) e.g. (7,0) | (10,3)
            third_line = file.readline().strip()
            goal_coords = third_line.split('|')
            goals = [parse_coordinates(goal.strip()) for goal in goal_coords]

            # Remaining lines: walls (col, row, width, height)
            walls = []
            for line in file:
                line = line.strip()
                if line:  # Ignore empty lines
                    wall_coordinates = parse_coordinates(line)
                    if len(wall_coordinates) == 4:
                        walls.append(wall_coordinates)

            return rows, cols, [(col_idx, row_idx)], goals, walls

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return None
    except ValueError as e:
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
