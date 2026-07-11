import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def visualize_comparison(rtree_mbrs, grid_obj, X, kmeans_results):
    """
    Master function to plot R-tree, Grid, and K-Means side-by-side.

    Parameters:
    - rtree_mbrs: List of (xmin, ymin, xmax, ymax) tuples.
    - grid_obj: The Grid instance.
    - X: The original data points (needed for the scatter plot).
    - kmeans_results: Tuple returned by evaluate_kmeans_overlap -> (overlap, labels, centers, radii)
    """

    # Create a figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))

    # Unpack axes
    ax_rtree, ax_grid, ax_kmeans = axes

    # --- 1. Plot R-Tree MBRs ---
    plot_rtree_on_ax(ax_rtree, rtree_mbrs)

    # --- 2. Plot Grid ---
    plot_grid_on_ax(ax_grid, grid_obj)

    # --- 3. Plot K-Means ---
    # Unpack carefully based on your function's return order:
    # return compute_total_overlap(...), labels, centers, radii
    overlap_score, labels, centers, radii = kmeans_results

    plot_kmeans_on_ax(ax_kmeans, X, labels, centers, radii, overlap_score)

    plt.tight_layout()
    fig.savefig("spatial_comparison_combined.png", dpi=500, bbox_inches="tight")
    plt.show()


# --- Helper Functions (Keep these as they were) ---


def plot_rtree_on_ax(ax, mbrs):
    ax.set_aspect("equal")
    ax.set_title(f"R-tree Leaf MBRs ({len(mbrs)} leaves)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    if not mbrs:
        ax.text(0.5, 0.5, "No MBR Data", ha="center", transform=ax.transAxes)
        return

    global_min_x, global_min_y = float("inf"), float("inf")
    global_max_x, global_max_y = float("-inf"), float("-inf")

    for x_min, y_min, x_max, y_max in mbrs:
        width = x_max - x_min
        height = y_max - y_min

        rect = patches.Rectangle(
            (x_min, y_min),
            width,
            height,
            linewidth=1.5,
            edgecolor="green",
            facecolor="palegreen",
            alpha=0.4,
            linestyle="-",
        )
        ax.add_patch(rect)

        global_min_x = min(global_min_x, x_min)
        global_min_y = min(global_min_y, y_min)
        global_max_x = max(global_max_x, x_max)
        global_max_y = max(global_max_y, y_max)

    buffer_x = (global_max_x - global_min_x) * 0.1 if mbrs else 1
    buffer_y = (global_max_y - global_min_y) * 0.1 if mbrs else 1
    ax.set_xlim(global_min_x - buffer_x, global_max_x + buffer_x)
    ax.set_ylim(global_min_y - buffer_y, global_max_y + buffer_y)

    legend_elements = [
        patches.Patch(
            facecolor="palegreen", edgecolor="green", alpha=0.4, label="Leaf MBR"
        )
    ]
    ax.legend(handles=legend_elements, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)


def plot_grid_on_ax(ax, grid):
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Grid Clustering")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")

    # Plot grid cells
    for i in range(grid.m):
        for j in range(grid.m):
            cell = grid.cells[i][j]
            rect = patches.Rectangle(
                (cell.x_min, cell.y_min),
                grid.delta_x,
                grid.delta_y,
                facecolor="none",
                edgecolor="gray",
                linestyle="--",
                alpha=0.5,
            )
            ax.add_patch(rect)

    # Plot points
    all_x, all_y = [], []
    for i in range(grid.m):
        for j in range(grid.m):
            for geom in grid.cells[i][j].get_geometry():
                all_x.append(geom.x)
                all_y.append(geom.y)
    if all_x and all_y:
        ax.scatter(
            all_x, all_y, color="blue", s=10, label="Data Points", zorder=2, alpha=0.3
        )

    # Plot centroids and radii
    centroids_x, centroids_y = [], []
    for i in range(grid.m):
        for j in range(grid.m):
            centroid = grid.centroids[i][j]
            radius = grid.cell_radius[i][j]

            if centroid is not None and (centroid[0] != 0 or centroid[1] != 0):
                centroids_x.append(centroid[0])
                centroids_y.append(centroid[1])
                if radius > 0:
                    circle = patches.Circle(
                        (centroid[0], centroid[1]),
                        radius,
                        color="green",
                        alpha=0.2,
                    )
                    ax.add_patch(circle)

    # if centroids_x:
    #     ax.scatter(
    #         centroids_x,
    #         centroids_y,
    #         color="red",
    #         marker="x",
    #         s=100,
    #         label="Centroids",
    #         zorder=3,
    #     )

    ax.set_xlim(grid.x_min, grid.x_max)
    ax.set_ylim(grid.y_min, grid.y_max)

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)


def plot_kmeans_on_ax(ax, X, labels, centers, radii, overlap_score):
    ax.set_aspect("equal")
    ax.set_title(f"K-Means (k={len(centers)})\nOverlap: {overlap_score:.4f}")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")

    # Plot Data Points
    ax.scatter(
        X[:, 0], X[:, 1], c=labels, cmap="viridis", s=10, alpha=0.3, label="Data Points"
    )

    # Plot Centroids
    ax.scatter(
        centers[:, 0],
        centers[:, 1],
        c="red",
        marker="x",
        s=100,
        linewidths=3,
        zorder=10,
        label="Centroids",
    )

    # Plot Cluster Circles
    for center, radius in zip(centers, radii):
        circle = patches.Circle(
            center,
            radius,
            facecolor="none",
            edgecolor="red",
            linestyle="--",
            linewidth=1.5,
            alpha=0.8,
        )
        ax.add_patch(circle)

    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)
