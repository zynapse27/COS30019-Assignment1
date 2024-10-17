import sys
import tkinter as tk

def display_grid_gui(rows, cols, markers=None, goals=None, walls=None, path_cell=None):
    """Create a tkinter GUI to display the grid based on given rows and columns."""
    root = tk.Tk()
    root.title("Grid Visualization")
    
    # Create a canvas for drawing the grid
    canvas = tk.Canvas(root, width=cols * 50, height=rows * 50, bg='white')
    canvas.pack()

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * 50, row * 50
            x2, y2 = x1 + 50, y1 + 50
            
            # Determine color based on cell type
            if walls and any((col >= wall_col and col < wall_col + wall_width and
                              row >= wall_row and row < wall_row + wall_height)
                             for (wall_col, wall_row, wall_width, wall_height) in walls):
                color = 'gray'  # Wall
            elif markers and (col, row) in markers:
                color = 'red'   # Marker
            elif goals and (col, row) in goals:
                color = 'green' # Goal
            else:
                color = 'white'  # Empty cell

            # Create rectangle for cell
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

    # Draw the pathfinding cell if specified
    if path_cell:
        path_x1 = path_cell[0] * 50 + 10  # Offset for the smaller square
        path_y1 = path_cell[1] * 50 + 10
        path_x2 = path_x1 + 30
        path_y2 = path_y1 + 30
        canvas.create_rectangle(path_x1, path_y1, path_x2, path_y2, fill='lightgray', outline='black')

    root.mainloop()

def parse_coordinates(coord_string):
    """Helper function to parse a string of coordinates in the format (col, row)."""
    coord_string = coord_string.split(')')[0] + ')'  # Ensure it closes the parentheses
    coord = coord_string.strip('()').split(',')
    return tuple(map(int, coord))

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

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

            # Print the specifications
            print(f"Grid Dimensions: {rows} rows, {cols} columns")
            print(f"Marker at: (Column: {col_idx}, Row: {row_idx})")
            print(f"Goal states at: {goals}")
            print(f"Walls at: {walls}")
            
            # Specify the cell to visualize the pathfinding
            pathfinding_cell = (col_idx, row_idx)  # Example: currently the marker cell
            
            # Call the GUI display function
            display_grid_gui(rows, cols, markers=[(col_idx, row_idx)], goals=goals, walls=walls, path_cell=pathfinding_cell)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except ValueError as e:
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
