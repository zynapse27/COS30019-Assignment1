import sys

def create_grid(rows, cols):
    """Creates a grid with the specified number of rows and columns."""
    return [['.' for _ in range(cols)] for _ in range(rows)]

def print_grid(grid):
    """Prints the grid to the console."""
    for row in grid:
        print(" ".join(row))

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            first_line = file.readline().strip()
            # Expecting the first line to be in the format [rows,cols]
            dimensions = eval(first_line)  # Be careful with eval in production code
            if isinstance(dimensions, list) and len(dimensions) == 2:
                rows, cols = dimensions
                if isinstance(rows, int) and isinstance(cols, int) and rows > 0 and cols > 0:
                    # Print grid specifications
                    print(f"Grid Specifications: {rows} rows, {cols} columns\n")
                    
                    grid = create_grid(rows, cols)
                    print_grid(grid)
                else:
                    print("Error: Rows and columns must be positive integers.")
            else:
                print("Error: First line must be in the format [rows, cols].")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

