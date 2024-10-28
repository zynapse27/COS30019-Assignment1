import sys
from file_parser import read_input_file
from grid import create_grid
from gui import display_grid_gui
import pathfinding
import time

def select_algorithm(algorithm_name):
    # Maps the algorithm name to the corresponding function
    algorithms = {
        'DFS': pathfinding.dfs,
        'BFS': pathfinding.bfs,
        'GBFS': pathfinding.gbfs,
        'ASTAR': pathfinding.astar,
        'CUS1': pathfinding.iddfs
    }
    return algorithms.get(algorithm_name.upper(), None)

def convert_path_to_directions(path):
    directions = []
    direction_map = {
        (0, -1): 'up',
        (0, 1): 'down',
        (-1, 0): 'left',
        (1, 0): 'right'
    }
    
    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]
        move = (next_cell[0] - current[0], next_cell[1] - current[1])
        
        if move in direction_map:
            directions.append(direction_map[move])
    
    return directions


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <algorithm>")
        print("Available algorithms: DFS, BFS, GBFS, ASTAR, CUS1")
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
        time.sleep(0.1)  # Delay for visualization

    path, node_count = algorithm(grid, start_position, goals, update_gui)

    # Display the input file and algorithm name, nested if for CUS1 and CUS2 to specify algorithm
    if algorithm_name.upper() == "CUS1":
        print(sys.argv[1], "CUS1 (IDDFS)")  # Display the input file and algorithm name
    elif algorithm_name.upper() == "CUS2":
        print(sys.argv[1], "not implemented")
    else:
        print(sys.argv[1], algorithm_name.upper())  # Display the input file and algorithm name

    # Final update for the GUI after reaching the goal
    if path:
        grid_display.draw_final_path(path)  # Draw the blue line representing the final path
        update_gui(path[-1], []) # Update the GUI again so path cell appears on top of path line

        # Get the reached goal from the last element of the path
        reached_goal = path[-1]
        print(f"<Node {reached_goal}> {node_count}")  # Display the coordinates of the reached goal

        directions = convert_path_to_directions(path)
        print(directions)  # Display the directions in the console
    else:
        print("No goal is reachable.", node_count)  # Display the node count when no goal is reachable

    # Keep the GUI open after pathfinding is complete
    grid_display.root.mainloop()

if __name__ == "__main__":
    main()
