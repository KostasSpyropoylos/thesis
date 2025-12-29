import math
from math import sqrt, acos, floor, sin
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cell import Cell
from geometry import Geometry


class Grid:
    def __init__(self, xmin, ymin, xmax, ymax, m):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.m = m
        self.deltax = (self.xmax - self.xmin) / m
        self.deltay = (self.ymax - self.ymin) / m

        # Initialize grid with empty cells
        self.cells = [
            [
                Cell(
                    xmin=self.xmin + i * self.deltax,
                    xmax=self.xmin + (i + 1) * self.deltax,
                    ymin=self.ymin + j * self.deltay,
                    ymax=self.ymin + (j + 1) * self.deltay,
                )
                for j in range(m)
            ]
            for i in range(m)
        ]

        # Centroids and radius storage
        self.centroids = [[cell.getCentroid() for cell in row] for row in self.cells]
        self.cell_radius = [[0 for _ in range(m)] for _ in range(m)]

    def findCell(self, x: float, y: float):
        """Find the appropriate cell for a given (x, y) coordinate."""
        i = min(max(int((x - self.xmin) / self.deltax), 0), self.m - 1)
        j = min(max(int((y - self.ymin) / self.deltay), 0), self.m - 1)
        return self.cells[i][j]

    def fit(self, data: tuple):
        """
        Assign points to their respective grid cells and update centroids and radii.
        Parameters:
            data(Tuple(X,Y)) : iterable
                An iterable containing (X, Y) coordinate pairs representing points to be assigned to the grid.
        """
        for x, y in data:
            geom = Geometry(x, y)
            cell: Cell = self.findCell(x, y)
            cell.add(geom)

        # Compute centroids and update radius
        self.getRadius()

    def getRadius(self):
        """Updates the radius for each cell"""
        for i in range(self.m):
            for j in range(self.m):
                cell = self.cells[i][j]
                points = cell.getGeometry()

                if points:
                    self.cell_radius[i][j] = max(
                        self.getDistance(p, self.centroids[i][j]) for p in points
                    )
                else:
                    self.cell_radius[i][j] = 0

    def getDistance(self, geom, centroid):
        """Compute Euclidean distance between a geometry and a centroid"""
        return math.sqrt((centroid[0] - geom.x) ** 2 + (centroid[1] - geom.y) ** 2)

    def getGeometries(self):
        """Return all geometries as separate lists of latitudes and longitudes"""
        longs, lats = zip(*[(geom.x, geom.y) for geom in Geometry.all])
        return list(longs), list(lats)

    def findOverlappingClusters(self):
        """Finds all overlapping clusters based on centroid distance and radius."""
        overlapping_clusters = []

        for i in range(self.m):
            for j in range(self.m):
                centroid1 = self.centroids[i][j]
                radius1 = self.cell_radius[i][j]

                if radius1 == 0:
                    continue

                for k in range(self.m):
                    for l in range(self.m):
                        # Same cell, skip
                        if (i, j) == (k, l):
                            continue

                        centroid2 = self.centroids[k][l]
                        radius2 = self.cell_radius[k][l]

                        if radius2 == 0:
                            continue

                        distance = math.sqrt(
                            (centroid2[0] - centroid1[0]) ** 2
                            + (centroid2[1] - centroid1[1]) ** 2
                        )

                        if distance < (radius1 + radius2):
                            overlapping_clusters.append(((i, j), (k, l)))

        return overlapping_clusters

    def compute_grid_overlap(self):
        """
        Compute total overlap metric.
        Optimized from O(M^4) to O(M^2) by considering each pair once.
        """
        total_overlap = 0.0
        PI = math.pi

        # Iterate through each unique pair of circles
        for i in range(self.m):
            for j in range(self.m):
                centroid1 = self.centroids[i][j]
                r1 = self.cell_radius[i][j]

                if r1 == 0:
                    continue

                for k in range(i, self.m):
                    for l in range(self.m):
                        if k == i and l <= j:
                            continue

                        centroid2 = self.centroids[k][l]
                        r2 = self.cell_radius[k][l]

                        if r2 == 0:
                            continue

                        distance = math.sqrt(
                            (centroid2[0] - centroid1[0]) ** 2
                            + (centroid2[1] - centroid1[1]) ** 2
                        )

                        # Case 1: Circles do not overlap
                        if distance >= (r1 + r2):
                            continue

                        # Case 2: One circle is completely contained within the other
                        if distance <= abs(r1 - r2):
                            total_overlap += PI * min(r1, r2) ** 2
                            continue
                        # Case 3: Circles partially overlap
                        
                        arg1 = (distance**2 + r1**2 - r2**2) / (2 * distance * r1)
                        arg2 = (distance**2 + r2**2 - r1**2) / (2 * distance * r2)

                        arg1 = max(-1.0, min(1.0, arg1))
                        arg2 = max(-1.0, min(1.0, arg2))

                        part1 = r1**2 * math.acos(arg1)
                        part2 = r2**2 * math.acos(arg2)

                        part3 = 0.5 * math.sqrt(
                            (-distance + r1 + r2)
                            * (distance + r1 - r2)
                            * (distance - r1 + r2)
                            * (distance + r1 + r2)
                        )

                        total_overlap += part1 + part2 - part3

        return total_overlap

    def visualize_grid(self, show_points=True, show_centroids=True, show_radii=True):
        """
        Visualizes the Grid, including cells, points, centroids, and cluster radii.
        Note: The 'Grid' class does not have an explicit `findOverlappingClusters`
        method that prints overlaps during iteration like DensityGrid does.
        If overlap visualization is desired, you'd need to call
        `findOverlappingClusters` and then iterate over its results.
        """
        fig, ax = plt.subplots(figsize=(10, 10))

        # Plot grid cells
        for i in range(self.m):
            for j in range(self.m):
                cell = self.cells[i][j]
                rect = plt.Rectangle(
                    (cell.xmin, cell.ymin),
                    self.deltax,
                    self.deltay,
                    facecolor="none",
                    edgecolor="gray",
                    linestyle="--",
                    alpha=0.5,
                )
                ax.add_patch(rect)

        # Plot points
        if show_points:
            all_x, all_y = [], []
            for i in range(self.m):
                for j in range(self.m):
                    for geom in self.cells[i][j].getGeometry():
                        all_x.append(geom.x)
                        all_y.append(geom.y)
            if all_x and all_y:
                ax.scatter(
                    all_x, all_y, color="blue", s=10, label="Data Points", zorder=2
                )

        # Plot centroids and radii
        centroids_x, centroids_y = [], []
        for i in range(self.m):
            for j in range(self.m):
                centroid = self.centroids[i][j]
                radius = self.cell_radius[i][j]
                if centroid != [0, 0]:
                    centroids_x.append(centroid[0])
                    centroids_y.append(centroid[1])
                    if show_radii and radius > 0:
                        circle = plt.Circle(
                            (centroid[0], centroid[1]),
                            radius,
                            color="green",
                            alpha=0.2,
                            label="Cluster Radius" if (i == 0 and j == 0) else "",
                        )
                        ax.add_patch(circle)

        if show_centroids and centroids_x and centroids_y:
            ax.scatter(
                centroids_x,
                centroids_y,
                color="red",
                marker="x",
                s=100,
                label="Centroids",
                zorder=3,
            )

        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Grid Visualization")
        ax.set_xlabel("X-coordinate")
        ax.set_ylabel("Y-coordinate")
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.show()


if __name__ == "__main__" :
    csv_data = pd.read_csv("datasets/skewed_coords.csv")
    # latitudes = csv_data["latitude"]
    # longitudes = csv_data["longitude"]
    latitudes = csv_data["latitude"]
    longitudes = csv_data["longitude"]

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
    kmeans_data = csv_data[["latitude", "longitude"]].to_numpy()
    grid = Grid(
        xmin=minLongtitude, ymin=minLatitude, xmax=maxLongitude, ymax=maxLatitude, m=20
    )
    # assign points to grid
    grid.fit(zip(csv_data["longitude"], csv_data["latitude"]))
        
    print(f"Grid Score: {grid.compute_grid_overlap()}")