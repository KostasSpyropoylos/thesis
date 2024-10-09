import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define MBR, Cell, and Grid classes as per the corrected code
class MBR:
    def __init__(self, xmax, xmin, ymax, ymin):
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
class Geometry:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def print(self):
        print('x:',self.x, ' y: ',self.y)
    
class Cell:
    def __init__(self, mbr, objects=None):
        self.mbr = mbr
        self.objects = objects if objects is not None else []
        self.geoms = []
           
    def add(self,g):
        self.geoms.append(Geometry(g.x,g.y))    
	
    def print(self):
        for obj in self.geoms:
            obj.print()

class Grid:
    def __init__(self, mbr, m):
        self.mbr = mbr  # The MBR for the entire grid
        self.m = m      # Number of divisions along each axis
        self.deltax = (mbr.xmax - mbr.xmin) / m  # Calculate the width of each cell
        self.deltay = (mbr.ymax - mbr.ymin) / m  # Calculate the height of each cell
        self.cells = []  # 2D list to store cells
        self.points = []
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
    	
    def add(self,g):
        cell = self.findCell(g.x,g.y)
        cell.print()
        cell.add(Geometry(g.x,g.y))
        self.points.append(cell)
	
    def findCell(self,x, y):
        self.deltax = (self.mbr.xmax - self.mbr.xmin)/self.m
        self.deltay = (self.mbr.ymax - self.mbr.ymin)/self.m
        i = (int)((x - self.mbr.xmin)/self.deltax )
        j = (int)((y - self.mbr.ymin)/self.deltay)
        return self.cells[i][j]
        # for (int i=0  i < m  i++) 
		# 	for (int j=0  j < m  j++) 
		# 		Cell c = cells[i][j]
		# 		if ((c.xmin < x && c.xmax > x) && (c.ymin < y && c.ymax > y))
		# 			return c`
    # def printPoints(self):
    #     for i in self.points:
    #         print(i.x)
	
# Create a grid with MBR and visualize it using matplotlib
mbr = MBR(1, 0, 1, 0)  # The MBR for the whole grid
grid = Grid(mbr, 5)  # Create a grid with 5x5 cells
# grid.add(Geometry(5, 8))
# grid.add(Geometry(5, 0))
# grid.add(Geometry(5, 2))
# grid.printPoints()
# Visualize the grid using matplotlib
# points = []
# with open("points.txt", "r") as f:
#     for line in f:
#         x, y = map(float, line.strip().split(","))
#         points.append((x, y))
import pandas as pd
df = pd.read_csv('kmeans_spatial_points.csv')
print(df.head())



csv_data = pd.read_csv('kmeans_spatial_points.csv')

# Step 2: Extract normLatitude and normLongitude columns
latitudes = csv_data['normLatitude']
longitudes = csv_data['normLongitude']

# Step 3: Assuming 'points' list and 'grid' object from previous example are defined
def plot():
    fig, ax = plt.subplots()

    # Draw each cell as a rectangle (grid visualization)
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

    # Step 4: Plot the points from the previous 'points' list
    # x_coords, y_coords = zip(*points)
    # ax.scatter(x_coords, y_coords, color='red', label='Original Points', zorder=5)

    # Step 5: Plot the points from the CSV file
    ax.scatter(latitudes, longitudes, color='green', label='CSV Points', zorder=6)

    # Step 6: Set the limits of the plot based on the grid MBR
    ax.set_xlim(grid.mbr.xmin, grid.mbr.xmax)
    ax.set_ylim(grid.mbr.ymin, grid.mbr.ymax)
    ax.set_aspect('equal')

    # Add plot title, labels, and grid
    plt.title('Grid with Original Points and CSV Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.legend()
    plt.show()
plot()