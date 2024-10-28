import heapq

# Depth-First Search (DFS)
def dfs(grid, start, goals, update_gui=None, clear_gui=None):

    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions
    
    # Stack for DFS: Each element is a tuple (current_node, path_taken)
    stack = [(start, [start])]
    
    # Set to keep track of visited nodes
    visited = set()
    node_count = 0  # Counter for nodes created

    while stack:
        # Pop the most recent node (LIFO order)
        current, path = stack.pop()
        
        # Mark the current node as visited
        if current in visited:
            continue
        
        visited.add(current)
        node_count += 1  # Increment the node counter
        
        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            potential_nodes = get_neighbors(current, walls, rows, cols)
            update_gui(current, visited, potential_nodes)
        
        # Check if the current node is a goal
        if current in goals:
            return path, node_count  # Return the path to the goal and the node count
        
        # Get neighbors using the provided get_neighbors function
        neighbors = get_neighbors(current, walls, rows, cols)
        
        # Add neighbors to the stack in reverse order to maintain UP, LEFT, DOWN, RIGHT expansion order
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    # If the stack is empty and no goal was found
    return None, node_count  # Return None for path and the node count

# Breadth-First Search (BFS)
def bfs(grid, start, goals, update_gui=None, clear_gui=None):
    
    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions
    
    # Queue for BFS: Each element is a tuple (current_node, path_taken)
    queue = [(start, [start])]
    
    # Set to keep track of visited nodes
    visited = set()
    node_count = 0  # Counter for nodes created

    while queue:
        # Dequeue the oldest node (FIFO order)
        current, path = queue.pop(0)
        
        # Mark the current node as visited
        if current in visited:
            continue
        
        visited.add(current)
        node_count += 1  # Increment the node counter
        
        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            update_gui(current, visited)
        
        # Check if the current node is a goal
        if current in goals:
            return path, node_count  # Return the path to the goal and the node count
        
        # Get neighbors using the provided get_neighbors function
        neighbors = get_neighbors(current, walls, rows, cols)
        
        # Enqueue neighbors to the queue
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    
    # If the queue is empty and no goal was found
    return None, node_count  # Return None for path and the node count


# Heuristic function for Greedy Best-First Search (GBFS)
# Manhattan Distance
def manhattan_distance(node, goals):
    return min(abs(node[0] - goal[0]) + abs(node[1] - goal[1]) for goal in goals)

# Greedy Best-First Search (GBFS)
def gbfs(grid, start, goals, update_gui=None, clear_gui=None):
    """
    Perform a Greedy Best-First Search to find a path from start to one of the goal cells.
    
    Arguments:
    - grid: The grid representing the environment, where walls are marked.
    - start: The starting position of the agent (tuple of column, row).
    - goals: A list of goal positions (tuples of column, row).
    - update_gui: A callback function to update the GUI (optional).
    
    Returns:
    - path: The final path to the goal, or None if no path is found.
    - node_count: The total number of nodes created during the search.
    """
    
    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions
    
    # Priority queue for GBFS: Each element is a tuple (priority, (current_node, path_taken))
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Initial node has 0 priority
    came_from = {start: None}  # To reconstruct the path
    node_count = 0  # Counter for nodes created

    # Set to keep track of visited nodes
    visited = set()

    while priority_queue:
        # Pop the node with the lowest heuristic cost (the best node)
        _, current = heapq.heappop(priority_queue)

        # Mark the current node as visited
        if current in visited:
            continue
        
        visited.add(current)
        node_count += 1  # Increment the node counter
        
        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            update_gui(current, visited)
        
        # Check if the current node is a goal
        if current in goals:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse the path to get from start to goal
            return path, node_count  # Return the path to the goal and the node count
        
        # Get neighbors using the provided get_neighbors function
        neighbors = get_neighbors(current, walls, rows, cols)

        # Enqueue neighbors with their heuristic cost (priority)
        for neighbor in neighbors:
            if neighbor not in visited:
                # Calculate the priority using the heuristic function
                priority = manhattan_distance(neighbor, goals)
                heapq.heappush(priority_queue, (priority, neighbor))
                if neighbor not in came_from:  # Only update if neighbor is seen for the first time
                    came_from[neighbor] = current

    # If the priority queue is empty and no goal was found
    return None, node_count  # Return None for path and the node count

# A* Search Algorithm
def astar(grid, start, goals, update_gui=None, clear_gui=None):
    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions

    # Priority queue for A* (min-heap)
    open_list = []
    start_f_value = manhattan_distance(start, goals)
    heapq.heappush(open_list, (start_f_value, 0, start, [start]))  # (f(n), g(n), position, path)

    # To reconstruct the path
    came_from = {start: None}
    node_count = 0  # Counter for nodes created

    # g_score for each node
    g_score = {start: 0}  
    # f_score for each node
    f_score = {start: start_f_value}

    visited = set()  # Set to keep track of visited nodes

    while open_list:
        # Get the node with the lowest f(n) score
        current_f, current_g, current, path = heapq.heappop(open_list)

        # Skip if already visited
        if current in visited:
            continue

        # Mark the current node as visited
        visited.add(current)

        # Increment the node counter
        node_count += 1  

        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            update_gui(current, visited)

        # Check if the current node is a goal
        if current in goals:
            # Reconstruct the path to the goal
            full_path = []
            while current is not None:
                full_path.append(current)
                current = came_from[current]
            full_path.reverse()  # Reverse to get path from start to goal
            return full_path, len(visited)  # Return path and visited node count
        
        # Get neighbors using the provided get_neighbors function
        for neighbor in get_neighbors(current, walls, rows, cols):
            tentative_g_score = g_score[current] + 1  # Cost from current to neighbor is assumed to be 1

            # If this path to neighbor is better than any previous one
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goals)

                if neighbor not in visited:
                    heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor, path + [neighbor]))

    # If the open_list is empty and no goal was found
    return None, node_count  # Return None for path and the visited node count


# Iterative Deepening Depth-First Search (IDDFS)
def iddfs(grid, start, goals, update_gui=None, clear_gui=None):

    def dls(node, depth, path, visited): # Depth-limited search function, to be called recursively by the IDDFS function
    # Essentially DFS but simplified and modified to have a depth limit

        # Stops the search if the depth limit is reached 
        if depth == 0:
            return None  
        
        # Mark the current node as visited
        if node in visited:
            return None

        visited.add(node)
        
        # Update the GUI with the current position and visited nodes (if a GUI callback is provided)
        if update_gui:
            update_gui(node, visited)
        
        # Check if the current node is a goal
        if node in goals:
            return path  # Return the path to the goal
        
        # Get neighbors using the provided get_neighbors function
        neighbors = get_neighbors(node, walls, rows, cols)
        
        for neighbor in neighbors:
            result = dls(neighbor, depth - 1, path + [neighbor], visited)
            if result is not None:
                return result  # Return the found path if not None

        return None  # No path found at this depth

    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    walls = {(c, r) for r in range(rows) for c in range(cols) if grid[r][c] == 'W'}  # Collect wall positions

    # Iterate over depth limits until a goal is found
    for depth in range(rows * cols):  # Arbitrary limit based on grid size
        print(f"Depth: {depth}")
        visited = set()  # Reset visited for each depth limit
        path = dls(start, depth, [start], visited)  # Perform depth-limited search
        if path is not None:
            return path, len(visited)  # Return path and the number of unique nodes visited
        clear_gui()

    return None, 0  # If no path is found within the limits

#Helper function to get valid neighbors of a cell that are not walls.
def get_neighbors(cell, walls, rows, cols):
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