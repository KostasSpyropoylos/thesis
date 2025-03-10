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
            geoms = grid.cells[i][j].getGeometry()

            arr = [(geom.x, geom.y) for geom in geoms]

            ax.set_aspect("equal")
            rect = patches.Rectangle(
                (cell.xmin, cell.ymin),  # Bottom left corner
                grid.deltax,  # Width
                grid.deltay,  # Height
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


def compute_cluster_radii(X, labels, centers):
    """
    Compute the radius of each cluster, defined as the maximum distance
    from any point in the cluster to the cluster centroid.
    """
    num_clusters = len(centers)
    radii = np.zeros(num_clusters)
    X_np = X

    for i in range(num_clusters):
        cluster_points = X_np[labels == i]
        if len(cluster_points) > 0:
            radii[i] = max(euclidean(p, centers[i]) for p in cluster_points)

    return radii


def compute_total_overlap(centers, radii):
    """
    Compute total overlap across all clusters.
    """
    if radii is None or len(radii) == 0:
        raise ValueError("Radii computation failed, received None or empty array.")

    total_overlap = 0
    num_clusters = len(centers)
    Pi = 3.141592653589793

    for i in range(num_clusters):
        r1 = radii[i]
        for j in range(i + 1, num_clusters):
            r2 = radii[j]
            distance = math.sqrt(
                (centers[i][0] - centers[j][0]) ** 2
                + (centers[i][1] - centers[j][1]) ** 2
            )

            if distance > (r1 + r2):
                continue

            if distance <= abs(r1 - r2):
                total_overlap += Pi * min(r1, r2) ** 2
                continue

            part1 = r1**2 * math.acos(
                (distance**2 + r1**2 - r2**2) / (2 * distance * r1)
            )
            part2 = r2**2 * math.acos(
                (distance**2 + r2**2 - r1**2) / (2 * distance * r2)
            )
            part3 = 0.5 * math.sqrt(
                (-distance + r1 + r2)
                * (distance + r1 - r2)
                * (distance - r1 + r2)
                * (distance + r1 + r2)
            )

            total_overlap += part1 + part2 - part3

    return total_overlap


def evaluate_kmeans_overlap(X, n_clusters):
    """
    Run KMeans clustering and compute total overlap.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_
    radii = compute_cluster_radii(X, labels, centers)

    return compute_total_overlap(centers, radii), labels, centers, radii


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
