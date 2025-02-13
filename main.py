import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import math
from grid.gbdc import Geometry, Grid


def plot():
    fig, ax = plt.subplots()

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

            ax.set_aspect("equal")
            rect = patches.Rectangle(
                (cell.xmin, cell.ymin),
                grid.deltax,
                grid.deltay,
                edgecolor="blue",
                facecolor="none",
            )
            ax.add_patch(rect)
            centroid_x = grid.centroids[i][j][0]
            centroid_y = grid.centroids[i][j][1]

            ax.scatter(centroid_y, centroid_x, color="red", label=None, zorder=8)

            radius = grid.cell_radius[i][j]
            print(radius)

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
    csv_data = pd.read_csv("grid/points.csv")
    latitudes = csv_data["normLatitude"].values
    longitudes = csv_data["normLongitude"].values

    minLatitude = math.floor(latitudes.min())
    maxLatitude = math.ceil(latitudes.max())
    minLongitude = math.floor(longitudes.min())
    maxLongitude = math.ceil(longitudes.max())

    points_array = np.column_stack((longitudes, latitudes))

    grid = Grid(points_array)
    labeled_grid, num_clusters = grid.cluster(density_threshold=10)
    print("Number of clusters:", num_clusters)
    grid.visualize(labeled_grid)
