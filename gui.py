# gui.py

import tkinter as tk

class GridDisplay:
    def __init__(self, rows, cols, markers=None, goals=None, walls=None):
        self.rows = rows
        self.cols = cols
        self.markers = markers if markers else []
        self.goals = goals if goals else []
        self.walls = walls if walls else []
        self.cell_size = 50  # Size of each cell in pixels

        # Increase the canvas size based on the number of rows and columns
        self.canvas_width = cols * self.cell_size
        self.canvas_height = rows * self.cell_size
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.draw_grid()

    def draw_grid(self):
        """Draw the entire grid with walls, markers, and goals."""
        for row in range(self.rows):
            for col in range(self.cols):
                color = 'white'  # Default color for empty cells
                if (col, row) in self.markers:
                    color = 'red'  # Color for the marker
                elif (col, row) in self.goals:
                    color = 'green'  # Color for goal cells
                elif any(wall[0] <= col < wall[0] + wall[2] and wall[1] <= row < wall[1] + wall[3] for wall in self.walls):
                    color = 'gray'  # Color for walls
                
                # Draw the cell
                self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size,
                                             (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                                             fill=color, outline='')  # Fill the cell with color

        # Draw grid lines
        self.draw_grid_lines()

    def draw_grid_lines(self):
        """Draw the grid lines on top of the cells."""
        for i in range(self.rows + 1):
            self.canvas.create_line(0, i * self.cell_size, self.canvas_width, i * self.cell_size, fill='black')
        for i in range(self.cols + 1):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_height, fill='black')

    def update_search_cells(self, visited_cells):
        """Update the grid to show all searched cells in light green."""
        for cell in visited_cells:
            if cell not in self.goals and cell not in self.markers:  # Don't overwrite goal or marker cells
                x1 = cell[0] * self.cell_size
                y1 = cell[1] * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # Draw the searched cell with a light green background
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightgreen', outline='')  # Draw searched cell
        self.draw_grid_lines()  # Redraw grid lines on top

    def update_pathfinding_cell(self, path_cell):
        """Update the position of the pathfinding cell."""
        self.canvas.delete("path_cell")  # Clear previous path cell
        smaller_square_size = 35  # Size of the smaller square
        offset = (self.cell_size - smaller_square_size) // 2  # Calculate the offset to center the smaller square
        path_x1 = path_cell[0] * self.cell_size + offset  # Offset for the smaller square
        path_y1 = path_cell[1] * self.cell_size + offset  # Offset for the smaller square
        path_x2 = path_x1 + smaller_square_size  # Smaller square width
        path_y2 = path_y1 + smaller_square_size  # Smaller square height
        self.canvas.create_rectangle(path_x1, path_y1, path_x2, path_y2, fill='red3', tags="path_cell")  # Draw pathfinding square
        self.root.update()  # Update the GUI

    def draw_final_path(self, path):
        """Draw the final path as a blue line after the goal is reached."""
        for i in range(len(path) - 1):
            x1 = path[i][0] * self.cell_size + self.cell_size // 2
            y1 = path[i][1] * self.cell_size + self.cell_size // 2
            x2 = path[i + 1][0] * self.cell_size + self.cell_size // 2
            y2 = path[i + 1][1] * self.cell_size + self.cell_size // 2
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)  # Draw the blue path line
        self.root.update()  # Update the GUI to show the line

def display_grid_gui(rows, cols, markers=None, goals=None, walls=None):
    """Create the GUI and handle updates during DFS."""
    grid_display = GridDisplay(rows, cols, markers, goals, walls)

    return grid_display  # Return the grid display instance for updating