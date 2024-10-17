# main.py

import sys
from file_parser import read_input_file
from grid import create_grid, print_grid
from gui import display_grid_gui
from pathfinding import dfs
import time

def print_specifications(rows, cols, markers, goals, walls):
    """Print the grid specifications including markers, goals, and walls."""
    print(f"Grid Dimensions: {rows} rows, {cols} columns")
    print(f"Marker Cell at: {markers}")
    print(f"Goal Cells at: {goals}")
    print(f"Walls at: {walls}")
    print("\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    # Read input file
    result = read_input_file(input_file)
    if result is None:
        sys.exit(1)

    rows, cols, markers, goals, walls = result

    # Print specifications for debugging
    print_specifications(rows, cols, markers, goals, walls)

    # Create and print the grid for debugging
    grid = create_grid(rows, cols, markers, goals, walls)
    print("Grid Representation:")
    print_grid(grid)

    # Specify the starting position of the light gray square (the marker cell)
    start_position = (markers[0][0], markers[0][1])

    # Create the GUI display
    grid_display = display_grid_gui(rows, cols, markers=markers, goals=goals, walls=walls)

    # Call the DFS to find a path to one of the goal cells
    def update_gui(current, visited):
        grid_display.update_search_cells(visited)  # Update the light green searched cells
        grid_display.update_pathfinding_cell(current)  # Update the current pathfinding cell
        time.sleep(0.1)  # Delay for visualization (adjust as needed)

    path = dfs(grid, start_position, goals, update_gui)

    # Final update for the GUI after reaching the goal
    if path:
        print(f"Path found: {path}")
        # Update the GUI to show the final path taken
        for step in path:
            grid_display.update_pathfinding_cell(step)
            time.sleep(0.1)  # Delay for visualization of the path
    else:
        print("No path found to any goal cell.")

    # Keep the GUI open after pathfinding is complete
    grid_display.root.mainloop()

if __name__ == "__main__":
    main()
