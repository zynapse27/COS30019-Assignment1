def dfs(grid, start, goals, update_gui=None):
    """
    Perform a Depth-First Search to find a path from start to one of the goal cells.
    
    Arguments:
    - grid: The grid representing the environment, where walls are marked.
    - start: The starting position of the agent (tuple of column, row).
    - goals: A list of goal positions (tuples of column, row).
    - update_gui: A callback function to update the GUI (optional).
    
    Returns:
    - path: The final path to the goal, or None if no path is found.
    """
    
    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions
    
    # Stack for DFS: Each element is a tuple (current_node, path_taken)
    stack = [(start, [start])]
    
    # Set to keep track of visited nodes
    visited = set()
    
    while stack:
        # Pop the most recent node (LIFO order)
        current, path = stack.pop()
        
        # Mark the current node as visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            update_gui(current, visited)
        
        # Check if the current node is a goal
        if current in goals:
            return path  # Return the path to the goal
        
        # Get neighbors using the provided get_neighbors function
        neighbors = get_neighbors(current, walls, rows, cols)
        
        # Add neighbors to the stack in reverse order to maintain UP, LEFT, DOWN, RIGHT expansion order
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    # If the stack is empty and no goal was found
    return None



def get_neighbors(cell, walls, rows, cols):
    """Get valid neighbors of a cell (UP, LEFT, DOWN, RIGHT) that are not walls."""
    col, row = cell
    neighbors = []

    # UP
    if row > 0 and (col, row - 1) not in walls:
        neighbors.append((col, row - 1))
    # LEFT
    if col > 0 and (col - 1, row) not in walls:
        neighbors.append((col - 1, row))
    # DOWN
    if row < rows - 1 and (col, row + 1) not in walls:
        neighbors.append((col, row + 1))
    # RIGHT
    if col < cols - 1 and (col + 1, row) not in walls:
        neighbors.append((col + 1, row))
    
    return neighbors