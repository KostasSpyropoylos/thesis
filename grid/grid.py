import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import math
# Define MBR, Cell, and Grid classes as per the corrected code
class MBR:
    mbrs = []
    def __init__(self, xmax, xmin, ymax, ymin):
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin
        MBR.mbrs.append(self)
        
class Geometry:
    all = []
    def __init__(self,x,y):
        self.x=x
        self.y=y
        Geometry.all.append(self)
    def getGeometry(self):
        return self.x,self.y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    
    def __repr__(self) -> str:
        return f"{self.x} {self.y}"
    
class Cell:
    cells =[]
    def __init__(self, xmin,ymin,xmax,ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.geoms = []
        Cell.cells.append(self)
        
    def add(self,g):
        self.geoms.append(Geometry(g.x,g.y))    
	
    def print(self):
        for geoms in Geometry.all:
            print(geoms.name)
            
    def getGeometry(self):
        return self.geoms
    
    def subdivide(self, divisions=2,deltaX=None,deltaY=None):
        """Subdivide the cell into smaller cells."""

        subcells = []
        for i in range(divisions):
            for j in range(divisions):
                xmin = self.xmin + i * deltaX
                xmax = self.xmin + (i + 1) * deltaX
                ymin = self.ymin + j * deltaY
                ymax = self.ymin + (j + 1) * deltaY
                print('xmin:',xmin,' ymin:',ymin,' xmax:',xmax,' ymax:',ymax)
                subcells.append(Cell(xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin))

        return subcells
    
    def __repr__(self):
        return f"Cell({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax})"

class Grid:
    def __init__(self, xmin,ymin,xmax,ymax, m):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.m=m
        self.deltax = (self.xmax - self.xmin) / m  # Calculate the width of each cell
        self.deltay = (self.ymax - self.ymin) / m  # Calculate the height of each cell
        print(f"deltaX:{self.deltax} deltaY:{self.deltay}")
        # print('deltaX:',self.deltax,' deltaY:',self.deltay)
        self.cells = [[0]*int(self.deltax)]*int(self.deltay)  # 2D list to store cells
        # self.cells=[]
        self.points = [[0]*int(self.deltax)]*int(self.deltay)
        self.create_grid()

    def create_grid(self):
        for i in range(self.m):
            row = []
            for j in range(self.m):
                xmin = self.xmin + i * self.deltax
                xmax = self.xmin + (i + 1) * self.deltax
                ymin = self.ymin + j * self.deltay
                ymax = self.ymin + (j + 1) * self.deltay
                # print('xmin:',xmin,' ymin:',ymin,' xmax:',xmax,' ymax:',ymax)
                row.append(Cell(xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin))
            # print(f"{row} {i}")
            self.cells.append(row)
            # print(self.cells)
    	
    def add(self,g):
        cell = self.findCell(g.x,g.y)
        cell.add(Geometry(g.x,g.y))
        self.points.append(cell)
	
    def findCell(self,x, y):
        i = (int)((x -self.xmin)/self.deltax )
        j = (int)((y -self.ymin)/self.deltay)
        return self.cells[i][j]
    def divideGrid(self,subdivisions=2):
        new_grid = []
        for i in range(self.m):
            subdivided_rows = [[] for _ in range(subdivisions)]
            for j in range(self.m):
                subcells = self.cells[i][j].subdivide(subdivisions,self.deltax,self.deltay)
            
            # Add subcells to the appropriate rows
            for i in range(subdivisions):
                subdivided_rows[i].append(subcells[i * subdivisions:(i + 1) * subdivisions])
                print(subdivided_rows[i])
            new_grid.append(subdivided_rows)

        return new_grid

    def getGeometries(self):
        lats = []
        longs = []
        for geom in Geometry.all:
            lats.append(geom.y)
            longs.append(geom.x)
        return longs,lats
    
    def getPoints(self):
        for point in self.points:
            for geom in point.geoms:
                print(geom)
    

# Create a grid with MBR and visualize it using matplotlib
def plot():
    fig, ax = plt.subplots()
    
    # Draw each cell as a rectangle (grid visualization)
    # for i in range(grid.m):
        # for j in range(grid.m):
    for row in newGrid:
        for col in row:
            for obj in col:
                for cell in obj:
                    # cell = grid.cells[i][j]
                    rect = patches.Rectangle(
                        # (cell.xmin,cell.ymin),
                        (cell.xmin, cell.ymin),  # Bottom left corner
                        grid.deltax,                     # Width
                        grid.deltay,                     # Height
                        edgecolor='blue',
                        facecolor='none'
                    )
                    ax.add_patch(rect)
    # for i in range(subGrid.m):
    #     for j in range(subGrid.m):
    #         cell = subGrid.cells[i][j]
    #         rect = patches.Rectangle(
    #             (cell.xmin, cell.ymin),  # Bottom left corner
    #             subGrid.deltax,                     # Width
    #             subGrid.deltay,                     # Height
    #             edgecolor='blue',
    #             facecolor='none'
    #         )
    #         ax.add_patch(rect)
    
    # Step 4: Plot the points from the previous 'points' list
    # x_coords, y_coords = zip(*points)
    # ax.scatter(x_coords, y_coords, color='red', label='Original Points', zorder=5)
    # ax.scatter(subY, subX, color='red', label='Original Points', zorder=5)
    
    # Step 5: Plot the points from the CSV file
    ax.scatter(latitudes, longitudes, color='green', label='CSV Points', zorder=6)
    # ax.scatter(y, x, color='green', label='CSV Points', zorder=6)

    # Step 6: Set the limits of the plot based on the grid MBR
    # ax.set_xlim(grid.xmin, grid.xmax)
    # ax.set_ylim(grid.ymin, grid.ymax)
    ax.set_aspect('equal')

    # Add plot title, labels, and grid
    plt.title('Grid with Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(False)
    plt.legend()
    plt.show()

def assignPointsToGrid(x, y, grid:Grid):
    geom = Geometry(x,y)
    grid.add(geom)
    


csv_data = pd.read_csv('kmeans_spatial_points.csv')
# Step 2: Extract normLatitude and normLongitude columns
latitudes = csv_data['normLatitude']
longitudes = csv_data['normLongitude']
maxLatitude= latitudes.max()
maxLatitude = math.ceil(maxLatitude)
maxLongitude= longitudes.max()
# print(maxLongitude)
maxLongitude = math.ceil(maxLongitude)

points_array = np.column_stack((longitudes, latitudes))

# mbr = MBR(xmax=maxLongitude, xmin=0, ymax=maxLatitude, ymin=0) 
grid = Grid(xmin=0, ymin=0, xmax=maxLongitude,  ymax=maxLatitude,   m=2)
result = [assignPointsToGrid(x,y,grid) for x,y in zip(csv_data['normLongitude'],csv_data['normLatitude'])]
newGrid=grid.divideGrid()    


subGrid = Grid(0.5,0,1,0.5,4)


plot()

