import random
from rtree import index
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import pandas as pd
import numpy as np


class RTreeSpatialAnalyzer:
    """
    Efficient spatial data management using R-tree, optimized for large CSVs.
    """

    def __init__(self):
        self.rtree_index = index.Index()
        self.circle_data = []

    def load_data_from_csv(
        self, file_path, chunksize=1000, required_cols=["normLatitude", "normLongitude"]
    ):
        """
        Efficiently bulk-loads data into R-tree using STR (Sort-Tile-Recursive) packing.
        """
        try:
            latitude_col = required_cols[0]
            longitude_col = required_cols[1]
            df = pd.read_csv(file_path)
            if not all(col in df.columns for col in required_cols):
                raise ValueError("CSV must contain specified columns.")
            
            latitudes = df[latitude_col].to_numpy()
            longitudes = df[longitude_col].to_numpy()
            
            # Small jitter to allow STR variance across runs if data order changes
            noise_lat = np.random.normal(0, 1e-8, size=len(latitudes))
            noise_lon = np.random.normal(0, 1e-8, size=len(longitudes))
            latitudes = latitudes + noise_lat
            longitudes = longitudes + noise_lon
            
            self.circle_data = []
            
            def stream_data():
                for i, (lat, lon) in enumerate(zip(latitudes, longitudes)):
                    x_min, y_min = lon - 0.5, lat - 0.5
                    x_max, y_max = lon + 0.5, lat + 0.5
                    self.circle_data.append({"center": (lon, lat), "radius": 0.5, "point": (lon, lat)})
                    yield (i, (x_min, y_min, x_max, y_max), i)
                    
            p = index.Property()
            # Bulk load with STR
            self.rtree_index = index.Index(stream_data(), properties=p)
            # print(f"R-tree built with {len(self.circle_data)} entries using STR.")
            return True
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")
            return False

    def compute_tree_overlap(self):
        """
        Compute total overlap metric for the circles derived from the MBRs.
        Returns the total overlap area.
        Optimized for large datasets using NumPy.
        """
        if not self.circle_data:
            print("No circle data available. Load data first.")
            return 0.0

        centers = np.array([c["center"] for c in self.circle_data])
        radii = np.array([c["radius"] for c in self.circle_data])
        total_overlap = 0.0
        Pi = math.pi
        n = len(centers)

        for i in range(n):
            c1 = centers[i]
            r1 = radii[i]
            for j in range(i + 1, n):
                c2 = centers[j]
                r2 = radii[j]
                if r1 == 0 or r2 == 0:
                    continue
                dist = np.linalg.norm(c2 - c1)
                if dist >= (r1 + r2):
                    continue
                if dist <= abs(r1 - r2):
                    total_overlap += Pi * min(r1, r2) ** 2
                    continue

                part1 = r1**2 * math.acos((dist**2 + r1**2 - r2**2) / (2 * dist * r1))
                part2 = r2**2 * math.acos((dist**2 + r2**2 - r1**2) / (2 * dist * r2))
                part3 = 0.5 * math.sqrt(
                    (-dist + r1 + r2)
                    * (dist + r1 - r2)
                    * (dist - r1 + r2)
                    * (dist + r1 + r2)
                )
                overlap_area = part1 + part2 - part3
                total_overlap += overlap_area
        return total_overlap

    def find_leaf_clusters(self):
        """
        Returns a list of clusters {C1(K1, r1), C2(K2, r2)} based on R-tree Leaf MBRs.
        """
        clusters = []

        # Iterate over the leaves of the R-tree
        # .leaves() returns tuples of (id, child_ids, bounds)
        try:
            leaves = self.rtree_index.leaves()
        except AttributeError:
            print(
                "Error: The current Rtree version might not expose .leaves(). Update libspatialindex."
            )
            return []

        for leaf in leaves:
            bounds = leaf[2]

            x_min, y_min, x_max, y_max = bounds

            # Calculate Center K (midpoint of MBR)
            kx = (x_min + x_max) / 2.0
            ky = (y_min + y_max) / 2.0

            # Calculate Radius r (half-diagonal of MBR)
            # This ensures the circle covers the rectangular leaf MBR completely
            width = x_max - x_min
            height = y_max - y_min
            r_cluster = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)

            clusters.append(
                {
                    "K": (kx, ky),
                    "r": r_cluster,
                    "mbr": (
                        x_min,
                        y_min,
                        x_max,
                        y_max,
                    ),  # Storing MBR for visualization
                }
            )

        # print(f"Extracted {len(clusters)} clusters from R-tree leaves.")
        return clusters

    def enforce_k_groups(self, k: int):
        """
        Enforces exactly k groups by hierarchically merging the R-tree leaf clusters.
        """
        from sklearn.cluster import AgglomerativeClustering
        
        leaves = self.find_leaf_clusters()
        if len(leaves) <= k:
            self.final_clusters = leaves
            return
            
        leaf_centers = [leaf["K"] for leaf in leaves]
        clustering = AgglomerativeClustering(n_clusters=k, linkage='average')
        labels = clustering.fit_predict(leaf_centers)
        
        self.final_clusters = []
        
        for group_idx in range(k):
            min_x, min_y = float('inf'), float('inf')
            max_x, max_y = float('-inf'), float('-inf')
            
            for idx, label in enumerate(labels):
                if label == group_idx:
                    mbr = leaves[idx]["mbr"]
                    min_x = min(min_x, mbr[0])
                    min_y = min(min_y, mbr[1])
                    max_x = max(max_x, mbr[2])
                    max_y = max(max_y, mbr[3])
                    
            if min_x == float('inf'):
                continue
                
            kx = (min_x + max_x) / 2.0
            ky = (min_y + max_y) / 2.0
            width = max_x - min_x
            height = max_y - min_y
            r_cluster = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)
            
            self.final_clusters.append({
                "K": (kx, ky),
                "r": r_cluster,
                "mbr": (min_x, min_y, max_x, max_y)
            })

    def visualize_leaf_clusters(self, clusters):
        """
        Visualizes the original data, the Leaf MBRs (green boxes),
        and the resulting Clusters (red circles).
        """
        if not clusters:
            print("No clusters to visualize.")
            return

        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_aspect("equal")
        ax.set_title(f"Leaf-Based Clustering ({len(clusters)} clusters)")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # 1. Plot original items (faint blue)
        centers = np.array([c["center"] for c in self.circle_data])
        if centers.size > 0:
            ax.scatter(
                centers[:, 0],
                centers[:, 1],
                c="skyblue",
                s=10,
                alpha=0.3,
                label="Items",
            )

        # 2. Plot Leaf Clusters
        for clust in clusters:
            kx, ky = clust["K"]
            r = clust["r"]
            x_min, y_min, x_max, y_max = clust["mbr"]
            w = x_max - x_min
            h = y_max - y_min

            # Draw MBR (The actual R-tree leaf boundary) - Green Dashed
            rect = patches.Rectangle(
                (x_min, y_min),
                w,
                h,
                linewidth=1,
                edgecolor="green",
                facecolor="none",
                linestyle="--",
            )
            ax.add_patch(rect)

            # Draw Cluster Circle (The covering circle) - Red
            circle = patches.Circle(
                (kx, ky), r, linewidth=2, edgecolor="red", facecolor="none"
            )
            ax.add_patch(circle)

            # Draw Center
            ax.plot(kx, ky, "rx", markersize=5)

        # Legend and Scaling
        # Create dummy handles for legend
        legend_elements = [
            patches.Patch(facecolor="skyblue", alpha=0.3, label="Original Data"),
            patches.Patch(
                edgecolor="green",
                facecolor="none",
                linestyle="--",
                label="R-tree Leaf MBR",
            ),
            patches.Patch(edgecolor="red", facecolor="none", label="Cluster C(K, r)"),
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        # Auto-scale view
        if clusters:
            all_k = np.array([c["K"] for c in clusters])
            max_r = max(c["r"] for c in clusters)
            ax.set_xlim(
                np.min(all_k[:, 0]) - max_r - 1, np.max(all_k[:, 0]) + max_r + 1
            )
            ax.set_ylim(
                np.min(all_k[:, 1]) - max_r - 1, np.max(all_k[:, 1]) + max_r + 1
            )

        plt.grid(True, linestyle=":", alpha=0.6)
        plt.show()

    def compute_leaves_overlap(self, clusters):
        """
        Computes the total overlap area between the Cluster circles (C1, C2...).
        Matches the syntax and formula logic of compute_grid_overlap.
        """
        if not clusters:
            print("No clusters provided for overlap calculation.")
            return 0.0

        total_overlap = 0.0
        PI = math.pi
        n = len(clusters)

        centers = [c["K"] for c in clusters]
        radii = [c["r"] for c in clusters]

        # Iterate through unique pairs
        for i in range(n):
            centroid1 = centers[i]
            r1 = radii[i]

            if r1 == 0:
                continue

            for j in range(i + 1, n):
                centroid2 = centers[j]
                r2 = radii[j]

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
                # Calculate arguments for acos with safety clamping (max/min)
                arg1 = (distance**2 + r1**2 - r2**2) / (2 * distance * r1)
                arg2 = (distance**2 + r2**2 - r1**2) / (2 * distance * r2)

                # Clamp values to [-1.0, 1.0] to prevent floating point domain errors
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

    def get_leaf_mbrs(self):
        """
        Extracts the Minimum Bounding Rectangles (MBRs) of the R-tree leaves.
        Returns a list of tuples: (x_min, y_min, x_max, y_max)
        """
        mbrs = []
        try:
            # .leaves() returns tuples of (id, child_ids, bounds)
            # bounds is (xmin, ymin, xmax, ymax)
            leaves = self.rtree_index.leaves()
        except AttributeError:
            print("Error: Rtree version mismatch. Ensure libspatialindex is loaded.")
            return []

        for leaf in leaves:
            bounds = leaf[2]  # Extract the bounding box
            mbrs.append(bounds)

        # print(f"Extracted {len(mbrs)} Leaf MBRs from R-tree.")
        return mbrs

    def compute_mbr_overlap(self, mbrs):
        """
        Computes the total overlap area between all Leaf MBRs.
        Uses Rectangle Intersection logic (not Circles).
        """
        if not mbrs:
            print("No MBRs provided for overlap calculation.")
            return 0.0

        total_overlap_area = 0.0
        n = len(mbrs)

        # Iterate through unique pairs of MBRs
        for i in range(n):
            # MBR 1
            min_x1, min_y1, max_x1, max_y1 = mbrs[i]

            for j in range(i + 1, n):
                # MBR 2
                min_x2, min_y2, max_x2, max_y2 = mbrs[j]

                # Calculate intersection bounds
                # The start of the intersection is the max of the starts
                inter_xmin = max(min_x1, min_x2)
                inter_ymin = max(min_y1, min_y2)

                # The end of the intersection is the min of the ends
                inter_xmax = min(max_x1, max_x2)
                inter_ymax = min(max_y1, max_y2)

                # Check if there is an actual overlap
                if inter_xmax > inter_xmin and inter_ymax > inter_ymin:
                    overlap_width = inter_xmax - inter_xmin
                    overlap_height = inter_ymax - inter_ymin

                    intersection_area = overlap_width * overlap_height
                    total_overlap_area += intersection_area

        return total_overlap_area

    def visualize_mbrs(self, mbrs):
        """
        Visualizes ONLY the MBRs (rectangles).
        """
        if not mbrs:
            print("No MBRs to visualize.")
            return

        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_aspect("equal")
        ax.set_title(f"R-tree Leaf MBR Visualization ({len(mbrs)} leaves)")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Track min/max for plot scaling
        global_min_x, global_min_y = float("inf"), float("inf")
        global_max_x, global_max_y = float("-inf"), float("-inf")

        for x_min, y_min, x_max, y_max in mbrs:
            width = x_max - x_min
            height = y_max - y_min

            # Create rectangle patch
            # facecolor='none' makes it transparent, edgecolor sets the border
            rect = patches.Rectangle(
                (x_min, y_min),
                width,
                height,
                linewidth=1.5,
                edgecolor="green",
                facecolor="palegreen",
                alpha=0.4,  # Slight fill to see overlap density better
                linestyle="-",
            )
            ax.add_patch(rect)

            # Update global bounds for the view
            global_min_x = min(global_min_x, x_min)
            global_min_y = min(global_min_y, y_min)
            global_max_x = max(global_max_x, x_max)
            global_max_y = max(global_max_y, y_max)

        # Set plot limits with a small buffer
        if len(mbrs) > 0:
            buffer_x = (global_max_x - global_min_x) * 0.1
            buffer_y = (global_max_y - global_min_y) * 0.1
            ax.set_xlim(global_min_x - buffer_x, global_max_x + buffer_x)
            ax.set_ylim(global_min_y - buffer_y, global_max_y + buffer_y)

        # Legend
        legend_elements = [
            patches.Patch(
                facecolor="palegreen", edgecolor="green", alpha=0.4, label="Leaf MBR"
            ),
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        plt.grid(True, linestyle=":", alpha=0.6)
        fig.savefig("rtree_set_1.png", dpi=300, bbox_inches="tight")
        plt.show()


# if __name__ == "__main__":
#     csv_file_path = "./datasets/skewed_coords.csv"
#     analyzer = RTreeSpatialAnalyzer()
#     if analyzer.load_data_from_csv(
#         csv_file_path, 1000, required_cols=["latitude", "longitude"]
#     ):
#         total_overlap = analyzer.compute_overlap()
#         print(f"Total computed overlap area among circles: {total_overlap:.2f}")
#         analyzer.visualize("Spatial Data Points as Circles from CSV")
#     else:
#         print("Failed to load data. Cannot proceed with analysis.")
