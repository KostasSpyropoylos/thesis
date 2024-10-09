import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define MBR, Cell, and Grid classes as per the corrected code
class MBR:
    def __init__(self, xmax, xmin, ymax, ymin):
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin

class Cell:
    def __init__(self, mbr, objects=None):
        self.mbr = mbr
        self.objects = objects if objects is not None else []

class Grid:
    def __init__(self, mbr, m):
        self.mbr = mbr  # The MBR for the entire grid
        self.m = m      # Number of divisions along each axis
        self.deltax = (mbr.xmax - mbr.xmin) / m  # Calculate the width of each cell
        self.deltay = (mbr.ymax - mbr.ymin) / m  # Calculate the height of each cell
        self.cells = []  # 2D list to store cells
        self.create_grid()

    def create_grid(self):
        for i in range(self.m):
            row = []
            for j in range(self.m):
                xmin = self.mbr.xmin + i * self.deltax
                xmax = self.mbr.xmin + (i + 1) * self.deltax
                ymin = self.mbr.ymin + j * self.deltay
                ymax = self.mbr.ymin + (j + 1) * self.deltay
                cell_mbr = MBR(xmax, xmin, ymax, ymin)
                row.append(Cell(cell_mbr))
            self.cells.append(row)

# Create a grid with MBR and visualize it using matplotlib
mbr = MBR(5, 0, 5, 0)  # The MBR for the whole grid
grid = Grid(mbr, 5)  # Create a grid with 5x5 cells

# Visualize the grid using matplotlib
fig, ax = plt.subplots()

# Draw each cell as a rectangle
for i in range(grid.m):
    for j in range(grid.m):
        cell = grid.cells[i][j]
        rect = patches.Rectangle(
            (cell.mbr.xmin, cell.mbr.ymin),  # Bottom left corner
            grid.deltax,                     # Width
            grid.deltay,                     # Height
            edgecolor='blue',
            facecolor='none'
        )
        ax.add_patch(rect)

# Set the limits of the plot
ax.set_xlim(grid.mbr.xmin, grid.mbr.xmax)
ax.set_ylim(grid.mbr.ymin, grid.mbr.ymax)
ax.set_aspect('equal')

# Display the plot
plt.title('Grid Visualization')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()
