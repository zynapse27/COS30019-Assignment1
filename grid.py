# grid.py

def create_grid(rows, cols, markers=None, goals=None, walls=None):
    """Create a grid representation with markers, goals, and walls."""
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    if markers:
        for marker in markers:
            grid[marker[1]][marker[0]] = 'M'  # M for Marker

    if goals:
        for goal in goals:
            grid[goal[1]][goal[0]] = 'G'  # G for Goal

    if walls:
        for wall in walls:
            wall_col, wall_row, wall_width, wall_height = wall
            for r in range(wall_row, wall_row + wall_height):
                for c in range(wall_col, wall_col + wall_width):
                    grid[r][c] = 'W'  # W for Wall

    return grid


