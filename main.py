import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import math
from math import acos, sin, sqrt
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from grid.grid import Geometry, Grid, DensityGrid


def plot(grid):
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
            geoms = grid.cells[i][j].get_geometry()

            arr = [(geom.x, geom.y) for geom in geoms]

            ax.set_aspect("equal")
            rect = patches.Rectangle(
                (cell.x_min, cell.y_min),  # Bottom left corner
                grid.delta_x,  # Width
                grid.delta_y,  # Height
                edgecolor="blue",
                facecolor="none",
            )
            ax.add_patch(rect)

            centroid_x, centroid_y = grid.centroids[i][j]  # x, y coordinates
            ax.scatter(centroid_y, centroid_x, color="red", label=None, zorder=8)

            radius = grid.cell_radius[i][j]

            # **Draw the circle representing the radius**
            circle = plt.Circle(
                (centroid_y, centroid_x),  # Center (x, y)
                radius,  # Radius
                color="green",
                fill=False,
                linestyle="dashed",
            )
            ax.add_patch(circle)

            # Scatter the geometry points
            x_elements = [a for a, b in arr]
            y_elements = [b for a, b in arr]
            ax.scatter(y_elements, x_elements, color="black", label=None)

            ax.set_aspect("equal")
    plt.title("Grid with Points and Cell Radius")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(False)
    plt.legend()
    plt.show()





def plot_clusters(X, labels, centers, radii):
    """
    Plot the clustered data points with centroids and radii.
    """
    plt.figure(figsize=(8, 6))
    for i in range(len(centers)):
        cluster_points = X[labels == i]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f"Cluster {i}")
        plt.scatter(
            centers[i][0],
            centers[i][1],
            c="black",
            marker="x",
            s=100,
            label=f"Centroid {i}",
        )
        circle = plt.Circle(
            (centers[i][0], centers[i][1]),
            radii[i],
            color="r",
            fill=False,
            linestyle="dashed",
        )
        plt.gca().add_patch(circle)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.title("KMeans Clustering with Overlap Metric")
    plt.show()


if __name__ == "__main__":
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
    # initiate KMEANS
    kmeans_data = csv_data[["normLatitude", "normLongitude"]].to_numpy()
    overlap_score, labels, centers, radii = evaluate_kmeans_overlap(
        kmeans_data, n_clusters=7
    )

    # plot_clusters(kmeans_data, labels, centers, radii)

    # initiate grid 2x2
    grid = Grid(
        xmin=minLongtitude, ymin=minLatitude, xmax=maxLongitude, ymax=maxLatitude, m=20
    )
    # assign points to grid
    grid.fit(zip(csv_data["normLongitude"], csv_data["normLatitude"]))
    density_grid = DensityGrid(
        xmin=minLongtitude, ymin=minLatitude, xmax=maxLongitude, ymax=maxLatitude, m=20
    )
    # assign points to grid
    density_grid.fit(zip(csv_data["normLongitude"], csv_data["normLatitude"]))

    # print(grid.findOverlappingClusters())
    print("KMEANS Score:", overlap_score)
    print(f"Grid Score: {grid.compute_grid_overlap()}")
    print(f"Density Grid: {density_grid.compute_grid_overlap()}")
    plot(grid)
    # plot(density_grid)
