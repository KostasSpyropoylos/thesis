import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
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
        
    def print(self):
        print('x:',self.x, ' y: ',self.y)
    
    def getGeometry(self):
        return self.x,self.y
    
    
    
class Cell:
    cells =[]
    def __init__(self, mbr, objects=None):
        self.mbr = mbr
        self.objects = objects if objects is not None else []
        self.geoms = []
        Cell.cells.append(self.mbr)
        
    def add(self,g):
        self.geoms.append(Geometry(g.x,g.y))    
	
    def print(self):
        for geoms in Geometry.all:
            print(geoms.name)
    def getGeometry(self):
        arr = []
        return self.geoms
    
    

class Grid:
    def __init__(self, xmin,ymin,xmax,ymax, m):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.m=m
        self.deltax = (self.xmax - self.xmin) / m  # Calculate the width of each cell
        self.deltay = (self.ymax - self.ymin) / m  # Calculate the height of each cell
        # print('deltaX:',self.deltax,' deltaY:',self.deltay)
        self.cells = [[0]*int(self.deltax)]*int(self.deltay)  # 2D list to store cells
        self.points = [Cell(mbr)for i in range(m)]
        self.create_grid()

    def create_grid(self):
        for i in range(self.m):
            row = []
            for j in range(self.m):
                xmin = self.xmin + i * self.deltax
                xmax = self.xmin + (i + 1) * self.deltax
                ymin = self.ymin + j * self.deltay
                ymax = self.ymin + (j + 1) * self.deltay
                cell_mbr = MBR(xmax, xmin, ymax, ymin)
                # print('xmin:',xmin,' ymin:',ymin,' xmax:',xmax,' ymax:',ymax)
                row.append(Cell(cell_mbr))
            self.cells.append(row)
    	
    def add(self,g):
        cell = self.findCell(g.x,g.y)
        cell.add(Geometry(g.x,g.y))
        self.points.append(cell)
	
    def findCell(self,x, y):
        i = (int)((x -self.xmin)/self.deltax )
        j = (int)((y -self.ymin)/self.deltay)
        return self.cells[i][j]
        
    def getPoints(self):
        lat = []
        longs = []
        for geom in Geometry.all:
            lat.append(geom.y)
            longs.append(geom.x)
        return lat,longs

# Create a grid with MBR and visualize it using matplotlib

df = pd.read_csv('kmeans_spatial_points.csv')
# print(df.head())



import numpy as np
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
def assignPointsToGrid(x,y):
    geom = Geometry(x,y)
    grid.add(geom)
    
mbr = MBR(maxLatitude, 0, maxLongitude, 0)  # The MBR for the whole grid
grid = Grid(0,0,maxLongitude,maxLatitude, 2)
result = [assignPointsToGrid(x,y) for x,y in zip(csv_data['normLongitude'],csv_data['normLatitude'])]

latitudes,longitudes = grid.getPoints()    

# for cell in Cell.cells:
for mbr in MBR.mbrs:
    print(f"xmin {mbr.xmin} xmax {mbr.xmax} ymin {mbr.ymin} ymax {mbr.ymax}")

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
    ax.set_xlim(grid.xmin, grid.xmax)
    ax.set_ylim(grid.ymin, grid.ymax)
    ax.set_aspect('equal')

    # Add plot title, labels, and grid
    plt.title('Grid with Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(False)
    plt.legend()
    plt.show()
# plot()

