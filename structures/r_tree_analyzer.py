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

    def load_data_from_csv(self, file_path, chunksize=1000):
        """
        Efficiently reads normLatitude and normLongitude from a CSV file in chunks.
        """
        try:
            required_cols = ["normLatitude", "normLongitude"]
            
            chunk_iter = pd.read_csv(file_path, nrows=1000,chunksize=chunksize)
            item_id = 0
            for chunk in chunk_iter:
                if not all(col in chunk.columns for col in required_cols):
                    raise ValueError("CSV file must contain 'normLatitude' and 'normLongitude' columns.")
                
                latitudes = chunk["normLatitude"].to_numpy()
                longitudes = chunk["normLongitude"].to_numpy()
                for latitude, longitude in zip(latitudes, longitudes):
                    xmin, ymin = longitude, latitude
                    xmax, ymax = longitude, latitude
                    self.rtree_index.insert(item_id, (xmin, ymin, xmax, ymax))
                    
                    self.circle_data.append({"center": (longitude, latitude), "radius": 1})
                    item_id += 1
            print(f"R-tree built with {item_id} entries.")
            return True
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return False
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")
            return False

    def compute_overlap(self):
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

    def visualize(self, title="R-tree Leaf MBR Centers as Circles"):
        """
        Visualizes the circles based on the pre-calculated circle_data.
        """
        if not self.circle_data:
            print("No circle data available for visualization. Load data first.")
            return

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        centers = np.array([c["center"] for c in self.circle_data])
        radii = np.array([c["radius"] for c in self.circle_data])

        for center, radius in zip(centers, radii):
            circle = patches.Circle(
                center,
                radius,
                facecolor="skyblue",
                edgecolor="blue",
                alpha=0.6,
                linewidth=0.8,
            )
            ax.add_patch(circle)

        if centers.size > 0 and radii.size > 0:
            min_x_data = np.min(centers[:, 0] - radii)
            max_x_data = np.max(centers[:, 0] + radii)
            min_y_data = np.min(centers[:, 1] - radii)
            max_y_data = np.max(centers[:, 1] + radii)
            buffer = np.max(radii) * 2 if np.max(radii) > 0 else 5
            ax.set_xlim(min_x_data - buffer, max_x_data + buffer)
            ax.set_ylim(min_y_data - buffer, max_y_data + buffer)
        else:
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)

        plt.grid(True, linestyle="--", alpha=0.7)
        plt.show()

    def query_intersection(self, query_box):
        """
        Performs an intersection query on the R-tree.
        Args:
            query_box (tuple): (xmin, ymin, xmax, ymax)
        Returns:
            list: IDs of items whose MBRs intersect with the query_box.
        """
        return list(self.rtree_index.intersection(query_box))

if __name__ == "__main__":
    csv_file_path = "./grid/points.csv"
    analyzer = RTreeSpatialAnalyzer()
    if analyzer.load_data_from_csv(csv_file_path,1000):
        total_overlap = analyzer.compute_overlap()
        print(f"Total computed overlap area among circles: {total_overlap:.2f}")
        analyzer.visualize("Spatial Data Points as Circles from CSV")
        query_box_example = (20, 20, 60, 60)
        intersecting_ids = analyzer.query_intersection(query_box_example)
        print(f"\nQuerying for items intersecting with MBR: {query_box_example}")
        print(f"Found {len(intersecting_ids)} intersecting items (IDs: {intersecting_ids}).")
    else:
        print("Failed to load data. Cannot proceed with analysis.")