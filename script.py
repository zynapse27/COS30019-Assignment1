# script.py

import sys
import os
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
        'CUS1': pathfinding.iddfs,
        'CUS2': pathfinding.bidirectional_astar
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
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <algorithm> [--all-goals]")
        print("Available algorithms: DFS, BFS, GBFS, ASTAR, CUS1, CUS2")
        sys.exit(1)

    input_file = sys.argv[1]
    algorithm_name = sys.argv[2]
    find_all_goals = '--all-goals' in sys.argv

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
        print("Available algorithms: DFS, BFS, GBFS, ASTAR, CUS1, CUS2")
        sys.exit(1)

    # Define GUI update functions
    def update_gui(current, visited, potential_nodes):
        grid_display.update_potential_nodes(potential_nodes)  # Update potential nodes
        grid_display.update_search_cells(visited)  # Update visited cells
        grid_display.update_pathfinding_cell(current)  # Update current cell
        time.sleep(0.1)  # Delay for visualization

    def clear_gui():
        grid_display.reset()  # Reset the grid to its initial state

    # Find paths to all goals
    current_position = start_position
    remaining_goals = goals[:]
    total_node_count = 0
    final_path = []

    # Display the input file and algorithm name, if all goals mode is not enabled
    if find_all_goals == False:
        if algorithm_name.upper() == "CUS2":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(sys.argv[1], "CUS2 (Bidirectional A*)")
        elif algorithm_name.upper() != "CUS1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(sys.argv[1], algorithm_name.upper())  # Display the input file and algorithm name

    if find_all_goals:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Finding path to all goals...")

    while remaining_goals:
        # Find the path to the closest goal
        path, node_count = algorithm(grid, current_position, remaining_goals, update_gui, clear_gui)
        total_node_count += node_count
        total_goal_count = len(goals) - len(remaining_goals)

        if path:
            # Get the reached goal from the last element of the path
            reached_goal = path[-1]

            if find_all_goals:
                print(f"\nGoal {total_goal_count + 1} reached!") 

            # Add the found path to the final path, excluding the start point if it's already in the path
            if final_path:
                final_path.extend(path[1:])
            else:
                final_path.extend(path)

            # CUS1 (IDDFS) name is only printed here as it will constantly print current depth while searching
            if algorithm_name.upper() == "CUS1" and find_all_goals == False:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(sys.argv[1], "CUS1 (IDDFS)")
                
            print(f"<Node {reached_goal}> {node_count}")  # Display the coordinates of the reached goal

            directions = convert_path_to_directions(path)
            print(directions)  # Display the directions in the console

            # Remove the reached goal from the list of remaining goals
            remaining_goals.remove(reached_goal)

            # Update the current position to the reached goal
            current_position = reached_goal

            if not find_all_goals:
                break  # Stop after finding the first goal if --all-goals is not specified
        else:
            print("No goal is reachable.", total_node_count)  # Display the node count when no goal is reachable
            break

    # Draw the entire final path if all goals are found
    if final_path:
        grid_display.draw_final_path(final_path)  # Draw the blue line representing the entire final path
        grid_display.update_pathfinding_cell(final_path[-1])  # Updates path cell again so it appears on top of the final path

        if find_all_goals:
            
            # Assign algorithm name 
            if algorithm_name.upper() == "CUS1":
                method = "CUS1 (IDDFS)"
            elif algorithm_name.upper() == "CUS2":
                method = "CUS2 (Bidirectional A*)"
            else:
                method = algorithm_name.upper()   

            grid_display.update_pathfinding_cell(final_path[-1])  # Updates path cell again; mainly for Bidirectional A*
            print("\nAll goals reached!")
            print("Algorithm:", method)
            print("Map used:", sys.argv[1])
            print(f"Goals reached: {goals}")
            print(f"Total nodes expanded: {total_node_count}")
            print(f"Final path length: {len(final_path)}")       
            print(f"Final path to all goals: {convert_path_to_directions(final_path)}")


    # Keep the GUI open after pathfinding is complete
    grid_display.root.mainloop()

if __name__ == "__main__":
    main()