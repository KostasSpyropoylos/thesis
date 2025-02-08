import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label


class Geometry:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getGeometry(self):
        return self.x, self.y


class Cell:
    def __init__(self):
        self.geoms = []

    def add(self, g):
        self.geoms.append(g)

    def is_dense(self, density_threshold):
        return len(self.geoms) > density_threshold


class Grid:
    def __init__(self, data, l=None):
        self.data = np.array(data)
        self.n, self.m = self.data.shape

        # Compute grid size adaptively if not provided
        self.l = l if l else self.compute_optimal_l()

        # Compute min/max for each feature
        self.x_min = np.min(self.data, axis=0)
        self.x_max = np.max(self.data, axis=0)

        # Scale data to fit in [1, l+1]
        self.scaled_data = self.scale_data()

        # Create grid structure
        self.cells = self.create_grid()

    def compute_optimal_l(self):
        """Compute the grid resolution (l) based on dataset properties."""
        return int(np.sqrt(self.n))  # Default: sqrt(n), can be modified

    def scale_data(self):
        """Apply the scaling function Φ(x) to transform features to range [1, l+1]."""
        return 1 + (self.data - self.x_min) / (self.x_max - self.x_min) * self.l

    def get_grid_index(self, x):
        """Get the grid cell index for a given point x, clamped to valid range."""
        index = np.floor(
            1 + (x - self.x_min) / (self.x_max - self.x_min) * self.l
        ).astype(int)
        return tuple(np.clip(index - 1, 0, self.l - 1))

    def create_grid(self):
        """Initialize a grid and assign points to cells."""
        grid = {}
        for i, x in enumerate(self.scaled_data):
            cell_index = self.get_grid_index(x)
            if cell_index not in grid:
                grid[cell_index] = Cell()
            grid[cell_index].add(Geometry(*self.data[i]))
        return grid

    def cluster(self, density_threshold):
        """Perform density-based clustering on the grid."""
        density_grid = np.zeros((self.l, self.l), dtype=int)

        for (i, j), cell in self.cells.items():
            if cell.is_dense(density_threshold):
                density_grid[i, j] = 1

        labeled_grid, num_clusters = label(density_grid)
        return labeled_grid, num_clusters

    def visualize(self, labeled_grid):
        """Visualize the grid-based clusters with proper color mapping."""
        plt.figure(figsize=(8, 6))

        cluster_labels = np.unique(labeled_grid)
        num_clusters = len(cluster_labels) - (1 if 0 in cluster_labels else 0)

        for (i, j), cell in self.cells.items():
            cluster_id = labeled_grid[i, j]
            for geom in cell.geoms:
                plt.scatter(
                    geom.x,
                    geom.y,
                    c=[cluster_id],
                    cmap="tab10",
                    s=20,
                    vmin=0,
                    vmax=num_clusters,
                )

        plt.colorbar(label="Cluster ID")
        plt.title(f"Grid-Based Density Clustering (GBDC) - {num_clusters} Clusters")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.show()
