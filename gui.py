# gui.py

import tkinter as tk

class GridDisplay:
    def __init__(self, rows, cols, markers=None, goals=None, walls=None):
        self.rows = rows
        self.cols = cols
        self.markers = markers if markers else []
        self.goals = goals if goals else []
        self.walls = walls if walls else []
        self.final_path = []  # Store the final path for re-drawing after resize
        self.visited_cells = [] # Store visited cells to re-render them
        self.current_pathfinding_cell = None  # Store the current pathfinding cell
        self.cell_size = 50  # Default size of each cell in pixels

        self.root = tk.Tk()

        # Set the default window size (Width x Height)
        default_width = 600 
        default_height = 275 
        self.root.geometry(f"{default_width}x{default_height}")
        self.root.title("Search Grid Visualization")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind the resizing event to a function
        self.root.bind("<Configure>", self.on_resize)

        self.draw_grid()

    def on_resize(self, event):
        """Handle window resizing."""
        new_width = event.width
        new_height = event.height
        self.cell_size = min(new_width // self.cols, new_height // self.rows)

        # Redraw the grid with the new cell size
        self.canvas.delete("all")
        self.draw_grid()

        # Redraw visited cells and final path after resizing
        self.update_search_cells(self.visited_cells)
        if self.final_path:
            self.draw_final_path(self.final_path)
        
        # Redraw the pathfinding cell after resizing
        if self.current_pathfinding_cell:
            self.update_pathfinding_cell(self.current_pathfinding_cell)

    def draw_grid(self):
        """Draw the entire grid with walls, markers, and goals."""
        for row in range(self.rows):
            for col in range(self.cols):
                color = 'white'
                if (col, row) in self.markers:
                    color = 'red'
                elif (col, row) in self.goals:
                    color = 'green'
                elif any(wall[0] <= col < wall[0] + wall[2] and wall[1] <= row < wall[1] + wall[3] for wall in self.walls):
                    color = 'gray'

                # Draw the cell with the updated cell size
                self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size,
                                             (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                                             fill=color, outline='')

        # Draw grid lines
        self.draw_grid_lines()

    def draw_grid_lines(self):
        """Draw the grid lines on top of the cells."""
        for i in range(self.rows + 1):
            self.canvas.create_line(0, i * self.cell_size, self.cols * self.cell_size, i * self.cell_size, fill='black')
        for i in range(self.cols + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.rows * self.cell_size, fill='black')

    def update_search_cells(self, visited_cells):
        """Update the grid to show all searched cells in light green."""
        self.visited_cells = visited_cells  # Store visited cells for re-rendering
        for cell in visited_cells:
            if cell not in self.goals and cell not in self.markers:
                x1 = cell[0] * self.cell_size
                y1 = cell[1] * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.visited_cells.add(cell)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightgreen', outline='black', tags="visited_cell")

        self.draw_grid_lines()

    def update_pathfinding_cell(self, path_cell):
        """Update the position of the pathfinding cell."""
        self.current_pathfinding_cell = path_cell  # Store the current pathfinding cell for re-rendering
        self.canvas.delete("path_cell")
        smaller_square_size = self.cell_size * 0.7
        offset = (self.cell_size - smaller_square_size) // 2
        path_x1 = path_cell[0] * self.cell_size + offset
        path_y1 = path_cell[1] * self.cell_size + offset
        path_x2 = path_x1 + smaller_square_size
        path_y2 = path_y1 + smaller_square_size
        self.canvas.create_rectangle(path_x1, path_y1, path_x2, path_y2, fill='red3', tags="path_cell")

        self.root.update()

    def draw_final_path(self, path):
        """Draw the final path as a blue line after the goal is reached."""
        self.final_path = path  # Store the final path for re-drawing after resize
        for i in range(len(path) - 1):
            x1 = path[i][0] * self.cell_size + self.cell_size // 2
            y1 = path[i][1] * self.cell_size + self.cell_size // 2
            x2 = path[i + 1][0] * self.cell_size + self.cell_size // 2
            y2 = path[i + 1][1] * self.cell_size + self.cell_size // 2
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)

    def update_potential_nodes(self, potential_nodes):
        """Highlight potential nodes being evaluated."""
        for node in potential_nodes:
            x1 = node[0] * self.cell_size
            y1 = node[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            if node not in self.goals and node not in self.markers and node not in self.visited_cells:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightpink', outline='black', tags="potential_node")

        self.root.update()

    def reset(self):
        """Reset the grid to its initial state."""
        self.visited_cells = []
        self.draw_grid()  # Redraw the grid in its initial state

def display_grid_gui(rows, cols, markers=None, goals=None, walls=None):
    """Create the GUI and handle updates during DFS."""
    grid_display = GridDisplay(rows, cols, markers, goals, walls)

    return grid_display  # Return the grid display instance for updating

class SearchTreeDisplay:
    def __init__(self, parent_map):
        self.parent_map = parent_map
        self.root = tk.Toplevel()
        self.root.title("Search Tree Visualization")

        # Set default window size and position (500x925, on the right half of the screen)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Position on the right half of the screen
        x_position = int(screen_width * 0.75) - 250  # Adjust to center on the right half
        y_position = int((screen_height - 800) / 2)  # Center vertically

        # Apply window geometry
        self.root.geometry(f"500x800+{x_position}+{y_position}")

        # Canvas setup with scroll region
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<MouseWheel>", self.zoom)  # Bind scroll for zooming
        self.canvas.bind("<ButtonPress-1>", self.start_pan)  # Bind mouse press for panning
        self.canvas.bind("<B1-Motion>", self.pan)  # Bind motion for panning

        # Initial drawing settings
        self.node_radius = 25  # Increased node size
        self.zoom_level = 1.0
        self.pan_start_x, self.pan_start_y = 0, 0
        self.offset_x, self.offset_y = 250, 30  # Adjust starting offsets to center the tree in the window

        # Draw the tree with default positions and settings
        self.draw_tree()

    def zoom(self, event):
        """Zoom in or out with mouse scroll wheel."""
        scale = 1.1 if event.delta > 0 else 0.9  # Zoom factor
        self.zoom_level *= scale
        self.canvas.scale("all", event.x, event.y, scale, scale)
        self.update_scroll_region()

    def start_pan(self, event):
        """Store the initial coordinates when mouse button is pressed."""
        self.pan_start_x, self.pan_start_y = event.x, event.y

    def pan(self, event):
        """Pan the view by dragging with the mouse button 1."""
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.canvas.move("all", dx, dy)
        self.pan_start_x, self.pan_start_y = event.x, event.y
        self.update_scroll_region()

    def update_scroll_region(self):
        """Update the scroll region to fit the current view."""
        bbox = self.canvas.bbox("all")
        self.canvas.config(scrollregion=bbox)

    def draw_tree(self):
        positions = {}
        x, y = self.offset_x, self.offset_y
        start_node = next(iter(self.parent_map))  # Arbitrarily choose starting node
        self._draw_node(start_node, x, y, positions, depth=1)

    def _draw_node(self, node, x, y, positions, depth):
        positions[node] = (x, y)
        node_tag = f"node_{node}"  # Unique tag for each node

        # Draw node with updated radius
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius,
                                fill='lightblue', tags=node_tag)
        self.canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"), tags=node_tag)

        # Find and draw connections to child nodes
        children = [child for child, parent in self.parent_map.items() if parent == node]
        if children:
            next_y = y + 100  # Increased vertical spacing
            for i, child in enumerate(children):
                next_x = x + (i - len(children) // 2) * 100  # Horizontal spacing between children
                self.canvas.create_line(x, y + self.node_radius, next_x, next_y - self.node_radius, fill='black', tags=node_tag)
                self._draw_node(child, next_x, next_y, positions, depth + 1)