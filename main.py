import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import math
from grid.grid import Geometry, Grid


def plot():
    fig, ax = plt.subplots()
    # Visualize grid
    colors = ["red", "blue", "green", "yellow"]
    cnt = 0
    geometriesLen = len(Geometry.all)
    print((geometriesLen))
    arr = []
    for i in range(grid.m):
        for j in range(grid.m):
            cell = grid.cells[i][j]
            geoms = grid.cells[i][j].getGeometry()
            for geom in geoms:
                arr.append((geom.x, geom.y))

            # print(arr[:][0])

            ax.set_aspect("equal")
            rect = patches.Rectangle(
                # (cell.xmin,cell.ymin),
                (cell.xmin, cell.ymin),  # Bottom left corner
                grid.deltax,  # Width
                grid.deltay,  # Height
                edgecolor="blue",
                facecolor="none",
            )
            ax.add_patch(rect)
            centroid_x = grid.centroids[i][j][0]  # x-coordinate
            centroid_y = grid.centroids[i][j][1]  # y-coordinate

            # Plot the centroid
            ax.scatter(centroid_y, centroid_x, color="red", label=None, zorder=8)

            # Get the radius for the current cell
            radius = grid.cell_radius[i][j]
            print(radius)
            # Create a circle patch

            # Visualize subgrid
            # for row in newGrid:
            #     for cell in row:
            x_elements = [a for a, b in arr]
            y_elements = [b for a, b in arr]
            ax.scatter(y_elements, x_elements, color="black", label=None)
            cnt = cnt + 1

    ax.set_aspect("equal")

    plt.title("Grid with Points")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(False)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # csv_data = pd.read_csv('points.csv', nrows=1000000)
    csv_data = pd.read_csv("grid/points.csv")
    latitudes = csv_data["normLatitude"]
    longitudes = csv_data["normLongitude"]
    maxLatitude = latitudes.max()
    minLatitude = latitudes.min()
    minLatitude = math.floor(minLatitude)
    maxLatitude = math.ceil(maxLatitude)
    
    maxLongitude = longitudes.max()
    maxLongitude = math.ceil(maxLongitude)
    
    minLongtitude = longitudes.min()
    minLongtitude = math.floor(minLongtitude)
    
    points_array = np.column_stack((longitudes, latitudes))

    # initiate grid 2x2
    grid = Grid(
        xmin=minLongtitude, ymin=minLatitude, xmax=maxLongitude, ymax=maxLatitude, m=2
    )
    # assign points to grid
    grid.assignPointsToGrid(zip(csv_data["normLongitude"], csv_data["normLatitude"]))

    # divide each cell into to a new 2x2 grid
    # newGrid = grid.divideGrid()

    plot()
