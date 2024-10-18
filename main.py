import sys
from file_parser import read_input_file
from grid import create_grid
from gui import display_grid_gui
import pathfinding
import time

def select_algorithm(algorithm_name):
    """Map the algorithm name to the corresponding function, case-insensitively."""
    algorithms = {
        'dfs': pathfinding.dfs,
        # 'bfs': bfs,
        # 'astar': astar
    }
    return algorithms.get(algorithm_name.lower(), None)

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <algorithm>")
        print("Available algorithms: DFS, BFS, GBFS, ASTAR")
        sys.exit(1)

    input_file = sys.argv[1]
    algorithm_name = sys.argv[2]

    # Read input file
    result = read_input_file(input_file)
    if result is None:
        sys.exit(1)

    rows, cols, markers, goals, walls = result

    # Create the grid
    grid = create_grid(rows, cols, markers, goals, walls)

    # Specify the starting position of the light gray square (the marker cell)
    start_position = (markers[0][0], markers[0][1])

    # Create the GUI display
    grid_display = display_grid_gui(rows, cols, markers=markers, goals=goals, walls=walls)

    # Select the search algorithm
    algorithm = select_algorithm(algorithm_name)
    if algorithm is None:
        print(f"Error: Algorithm '{algorithm_name}' not recognized.")
        print("Available algorithms: DFS, BFS, GBFS, ASTAR")
        sys.exit(1)

    # Call the selected algorithm to find a path to one of the goal cells
    def update_gui(current, visited):
        grid_display.update_search_cells(visited)  # Update the light green searched cells
        grid_display.update_pathfinding_cell(current)  # Update the current pathfinding cell
        time.sleep(0.1)  # Delay for visualization (adjust as needed)

    path = algorithm(grid, start_position, goals, update_gui)

    # Final update for the GUI after reaching the goal
    if path:
        grid_display.draw_final_path(path)  # Draw the blue line representing the final path
    else:
        print("No path found to any goal cell.")

    # Keep the GUI open after pathfinding is complete
    grid_display.root.mainloop()

if __name__ == "__main__":
    main()
