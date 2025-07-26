import random
from rtree import index
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import pandas as pd # Import pandas

def read_data_from_csv(file_path):
    """
    Reads normLatitude and normLongitude from a CSV file and converts them
    into a format suitable for R-tree (xmin, ymin, xmax, ymax).
    For points, xmin = xmax and ymin = ymax.
    """
    try:
        df = pd.read_csv(file_path)

        # Check if required columns exist
        if 'normLatitude' not in df.columns or 'normLongitude' not in df.columns:
            raise ValueError("CSV file must contain 'normLatitude' and 'normLongitude' columns.")

        data = []
        for i, row in df.iterrows():
            latitude = row['normLatitude']
            longitude = row['normLongitude']
            # For a point, the MBR is a degenerate rectangle where min = max
            # Using longitude as X and latitude as Y for typical mapping conventions
            xmin, ymin = longitude, latitude
            xmax, ymax = longitude, latitude
            data.append((i, (xmin, ymin, xmax, ymax)))
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return []

def build_rtree_and_get_leaves(data):
    """
    Builds an R-tree from the sample data and extracts the MBRs of all items
    (which correspond to leaf nodes when individual items are inserted).
    """
    idx = index.Index()
    for item_id, bbox_coords in data:
        idx.insert(item_id, bbox_coords)
    return idx, [bbox_coords for _, bbox_coords in data] # Return the original data bboxes as leaf MBRs

def calculate_circle_data(leaf_mbrs):
    """
    Calculates the center and radius for each circle based on the leaf MBRs.
    Returns a list of dictionaries, each with 'center' and 'radius'.
    For points (where MBR is degenerate), a small default radius is used.
    """
    circle_data = []
    for mbr_coords in leaf_mbrs:
        xmin, ymin, xmax, ymax = mbr_coords
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        width = xmax - xmin
        height = ymax - ymin
        
        # For points, width and height will be 0. We need a visible radius.
        radius = min(width, height) / 2
        if radius == 0:
            radius = 0.5 # A small default radius for point visualization
        
        circle_data.append({'center': (center_x, center_y), 'radius': radius})
    return circle_data

def compute_total_circle_overlap(circles):
    """
    Compute total overlap metric for a list of circles.
    Each circle in 'circles' should be a dictionary with 'center':(x,y) and 'radius':r.
    This function adapts the provided grid overlap logic for an arbitrary list of circles.
    """
    total_overlap = 0
    num_circles = len(circles)
    Pi = math.pi # Use math.pi for better precision

    # Iterate through all unique pairs of circles
    for i in range(num_circles):
        for j in range(i + 1, num_circles): # Avoid self-comparison and double-counting pairs
            circle1 = circles[i]
            circle2 = circles[j]

            centroid1 = circle1['center']
            r1 = circle1['radius']

            centroid2 = circle2['center']
            r2 = circle2['radius']

            if r1 == 0 or r2 == 0:
                continue

            distance = math.sqrt(
                (centroid2[0] - centroid1[0]) ** 2
                + (centroid2[1] - centroid1[1]) ** 2
            )

            if distance >= (r1 + r2):
                # Circles are too far apart to overlap
                continue

            if distance <= abs(r1 - r2):
                # One circle is completely contained within the other
                total_overlap += Pi * min(r1, r2) ** 2
                continue

            # Standard formula for overlap area of two intersecting circles
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

            overlap_area = part1 + part2 - part3
            total_overlap += overlap_area

    return total_overlap

def visualize_circles_from_mbr_centers(circle_data, title="R-tree Leaf MBR Centers as Circles"):
    """
    Visualizes the circles based on the pre-calculated circle_data.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(title)
    ax.set_xlabel("Longitude") # Updated label
    ax.set_ylabel("Latitude")  # Updated label

    all_x_centers = []
    all_y_centers = []
    all_radii = []

    for circle_info in circle_data:
        center_x, center_y = circle_info['center']
        radius = circle_info['radius']
        all_x_centers.append(center_x)
        all_y_centers.append(center_y)
        all_radii.append(radius)

        circle = patches.Circle((center_x, center_y), radius,
                                facecolor='skyblue', edgecolor='blue', alpha=0.6, linewidth=0.8)
        ax.add_patch(circle)

    # Set plot limits dynamically based on the data centers and radii
    if all_x_centers and all_y_centers and all_radii:
        min_x_data = min(c - r for c, r in zip(all_x_centers, all_radii))
        max_x_data = max(c + r for c, r in zip(all_x_centers, all_radii))
        min_y_data = min(c - r for c, r in zip(all_y_centers, all_radii))
        max_y_data = max(c + r for c, r in zip(all_y_centers, all_radii))

        buffer = max(all_radii) * 2 # A buffer relative to the largest radius, increased for better visibility of points
        if buffer == 0: buffer = 5 # Default if all radii are 0

        ax.set_xlim(min_x_data - buffer, max_x_data + buffer)
        ax.set_ylim(min_y_data - buffer, max_y_data + buffer)
    else:
        # Default limits if no data
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    csv_file_path = './grid/points.csv' # Define your CSV file path here

    print(f"Reading data from '{csv_file_path}'...")
    sample_data_from_csv = read_data_from_csv(csv_file_path)

    if not sample_data_from_csv:
        print("No data read from CSV. Exiting.")
    else:
        print(f"Successfully read {len(sample_data_from_csv)} items from CSV.")

        print("Building R-tree and extracting leaf MBRs...")
        rtree_index, leaf_mbrs = build_rtree_and_get_leaves(sample_data_from_csv)

        print(f"Number of leaf MBRs extracted: {len(leaf_mbrs)}")

        # Calculate circle data (centers and radii) from leaf MBRs
        print("Calculating circle data (centers and radii)...")
        circles_for_overlap_metric = calculate_circle_data(leaf_mbrs)

        # Compute the total overlap metric
        print("Computing total circle overlap...")
        total_overlap_area = compute_total_circle_overlap(circles_for_overlap_metric)
        print(f"Total computed overlap area among circles: {total_overlap_area:.2f}")

        print("Visualizing leaf MBR centers as circles...")
        visualize_circles_from_mbr_centers(circles_for_overlap_metric)

        print("\nDemonstrating a query intersection (R-tree's primary function):")
        # Define a query box that might intersect some of your sample data
        # Adjust these coordinates based on the range of your CSV data
        query_box = (20, 20, 60, 60) # Example: (min_lon, min_lat, max_lon, max_lat)
        print(f"Querying for items intersecting with MBR: {query_box}")
        intersecting_ids = list(rtree_index.intersection(query_box))
        print(f"Found {len(intersecting_ids)} intersecting items (IDs: {intersecting_ids}).")