# pathfinding.py

def dfs(grid, start, goals, update_gui):
    """Depth-First Search (DFS) algorithm to find a path to one of the goal cells.
    
    Args:
        grid (list): The grid representation.
        start (tuple): Starting position (column, row).
        goals (list): List of goal positions.
        update_gui (function): Function to call to update the GUI after each move.
    
    Returns:
        list: The path taken to reach a goal or an empty list if no path found.
    """
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = set()
    path = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        path.append(current)

        # Update GUI to show current position and all visited cells
        update_gui(current, visited)

        # Check if the current position is a goal
        if current in goals:
            print(f"Goal reached at: {current}")
            return path  # Return the path if a goal is reached

        # Get possible movements in order: UP, LEFT, DOWN, RIGHT
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # UP, LEFT, DOWN, RIGHT
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < cols and  # Check column bounds
                0 <= neighbor[1] < rows and  # Check row bounds
                grid[neighbor[1]][neighbor[0]] not in ['W', 'M'] and  # Avoid walls and marker
                neighbor not in visited):  # Avoid revisiting nodes
                stack.append(neighbor)

    print("No path to goal found.")
    return []  # Return an empty list if no path found
