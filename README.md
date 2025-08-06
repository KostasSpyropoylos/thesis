# Alternative Spatial Clustering Methods for Skewed Data: Grid-Based and R-Tree Approaches

## Grid-Based and R-Tree Spatial Clustering Algorithms

This repository contains two spatial clustering approaches designed to optimize clustering for skewed datasets: a **Grid-Based Clustering** algorithm,  **Grid-Based Density Clustering** algorithm and an **R-Tree Spatial Analyzer**. Both are implemented in Python and are intended for research and thesis work focused on improving clustering performance and overlap minimization in spatially skewed data.

---

## 1. Grid-Based Clustering

**Location:** `structures/grid.py`

### Overview

The grid-based approach partitions the spatial domain into a uniform grid of cells. Each cell aggregates points, computes its centroid, and determines a "cluster radius" (the maximum distance from centroid to any point in the cell). Overlap between clusters is measured by the intersection of these circles.

### Key Features

- **Uniform grid partitioning**: Space is divided into `m x m` cells.
- **Centroid and radius calculation**: Each cell computes its centroid and the radius covering all its points.
- **Overlap detection**: Efficient algorithms to compute and visualize overlaps between clusters.
- **Visualization**: Matplotlib-based visualization of grid, points, centroids, radii, and overlaps.

### Usage

```python
from structures.grid import Grid

# Example: Create a grid and fit data
grid = Grid(xmin=0, ymin=0, xmax=100, ymax=100, m=10)
grid.fit(data)  # data is a list of (x, y) tuples

# Visualize the grid and clusters
grid.visualize_grid(show_points=True, show_centroids=True, show_radii=True, show_overlap=True)

# Compute total overlap area
overlap_area = grid.compute_grid_overlap()
print(f"Total overlap area: {overlap_area}")
```

---
---

## 2. Grid-Based Density Clustering

**Location:** `structures/grid.py`

### Overview

The grid-based approach partitions the spatial domain into a uniform grid of cells. Each cell aggregates points, computes its centroid, and determines a "cluster radius" (the maximum distance from centroid to any point in the cell). Overlap between clusters is measured by the intersection of these circles.

### Key Features

- **Uniform grid partitioning**: Space is divided into `m x m` cells.
- **Centroid and radius calculation**: Each cell computes its centroid and the radius covering all its points. It calculates the centroid based on the density of the cell
- **Overlap detection**: Efficient algorithms to compute and visualize overlaps between clusters.
- **Visualization**: Matplotlib-based visualization of grid, points, centroids, radii, and overlaps.

### Usage

```python
from structures.grid import DensityGrid

# Example: Create a grid and fit data
grid = DensityGrid(xmin=0, ymin=0, xmax=100, ymax=100, m=10)
grid.fit(data)  # data is a list of (x, y) tuples

# Visualize the grid and clusters
grid.visualize_grid(show_points=True, show_centroids=True, show_radii=True, show_overlap=True)

# Compute total overlap area
overlap_area = grid.compute_grid_overlap()
print(f"Total overlap area: {overlap_area}")
```

---

## 2. R-Tree Spatial Analyzer

**Location:** `structures/r_tree_analyzer.py`

### Overview

The R-Tree approach leverages spatial indexing for efficient management and querying of large, skewed datasets. Data points are indexed using an R-Tree, and clustering overlap is estimated by treating each point as a circle (with configurable radius) and computing pairwise overlaps.

### Key Features

- **Efficient spatial indexing**: Uses the rtree library for fast spatial queries.
- **Chunked CSV loading**: Handles large datasets efficiently by reading in chunks.
- **Overlap computation**: Calculates total overlap area among all circles.
- **Visualization**: Plots all circles and their overlaps for spatial insight.
- **Intersection queries**: Supports fast intersection queries for spatial regions.

### Usage

```python
from structures.r_tree_analyzer import RTreeSpatialAnalyzer

analyzer = RTreeSpatialAnalyzer()
if analyzer.load_data_from_csv("path/to/points.csv"):
    overlap = analyzer.compute_overlap()
    print(f"Total overlap: {overlap}")
    analyzer.visualize()
    # Example intersection query
    ids = analyzer.query_intersection((xmin, ymin, xmax, ymax))
    print(f"Intersecting IDs: {ids}")
```

