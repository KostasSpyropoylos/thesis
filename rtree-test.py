
from rtree import index
from utils import load_data
import random
import matplotlib.pyplot as plt

def generator_function(lat,long,length):
    for i, coord in enumerate(range(0, length, 1)):
        yield (i, (coord, coord+1, coord, coord+1), coord)

# if __name__ == "__main__":
    
#     latitudes,longitudes = load_data.load_data("datasets/skewed_coords.csv")
#     # Create an R-tree index
    
#     idx=index.Index(generator_function(latitudes, longitudes, len(latitudes)))
#     print(idx)
    
def create_sample_rtree(num_items: int = 100, bounds_range: tuple = (0, 100)):
    """
    Creates a sample R-tree index with random rectangular items.

    Args:
        num_items (int): The number of items to insert into the R-tree.
        bounds_range (tuple): A tuple (min_coord, max_coord) defining the
                              range for generating random coordinates.

    Returns:
        rtree.index.Rtree: A new R-tree index populated with random items.
    """
    
    idx = index.Rtree()
    min_coord, max_coord = bounds_range
    for i in range(num_items):
        # Generate random coordinates for a rectangle
        x1 = random.uniform(min_coord, max_coord - 5) # Ensure width > 0
        y1 = random.uniform(min_coord, max_coord - 5) # Ensure height > 0
        x2 = x1 + random.uniform(1, 5) # Small random width
        y2 = y1 + random.uniform(1, 5) # Small random height
        idx.insert(i, (x1, y1, x2, y2))
    return idx

def visualize_rtree(rtree_index: index.Rtree, title: str = "R-tree Visualization"):
    """
    Visualizes the bounding boxes of an R-tree index using Matplotlib.

    This function iterates through all items in the R-tree and draws their
    bounding boxes. It also attempts to visualize internal node bounding boxes
    if the R-tree provides a way to access them (though direct access to internal
    node MBRs is not standard in `rtree` library for visualization).
    For simplicity, this visualization primarily shows the leaf-level item MBRs.

    Args:
        rtree_index (rtree.index.Rtree): The R-tree index to visualize.
        title (str): The title for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(title)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.grid(True, linestyle='--', alpha=0.6)

    # List to store all bounding box coordinates for setting plot limits
    all_coords = []

    bounds = list(rtree_index.intersection(rtree_index.bounds, objects=True))
    if not bounds:
        print("No items found in the R-tree.")
        return
    for bound in bounds:
        print(bound.bbox)
        minx, miny, maxx, maxy = bound.bbox
        item_id = bound.id
        # Add coordinates to the list for setting limits
        all_coords.extend([minx, miny, maxx, maxy])

        # Draw the rectangle
        rect = plt.Rectangle((minx, miny), maxx - minx, maxy - miny,
                             fill=False, edgecolor='blue', linewidth=1.5,
                             label=f"Item {item_id}" if item_id < 5 else "") # Label a few for clarity

    # Set plot limits based on all bounding boxes
    if all_coords:
        min_x = min(all_coords[::4]) # minx values
        min_y = min(all_coords[1::4]) # miny values
        max_x = max(all_coords[2::4]) # maxx values
        max_y = max(all_coords[3::4]) # maxy values

        # Add a small buffer to the limits
        x_buffer = (max_x - min_x) * 0.1 if (max_x - min_x) > 0 else 10
        y_buffer = (max_y - min_y) * 0.1 if (max_y - min_y) > 0 else 10

        ax.set_xlim(min_x - x_buffer, max_x + x_buffer)
        ax.set_ylim(min_y - y_buffer, max_y + y_buffer)
    else:
        # Default limits if no items were found
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)


    # Note: Directly visualizing internal node MBRs with the `rtree` library
    # is not straightforward as its public API primarily exposes leaf-level
    # item bounding boxes. For a true hierarchical visualization, one would
    # typically need to access the internal tree structure, which `rtree`
    # doesn't expose directly for security/stability reasons.
    # The current visualization shows the spatial distribution of the data items.

    plt.show()

# --- Example Usage ---
if __name__ == "__main__":
    # print("Creating a sample R-tree...")
    # my_rtree = create_sample_rtree(num_items=50, bounds_range=(0, 200))
    # print(f"R-tree created with {len(list(my_rtree.intersection(my_rtree.bounds, objects=True)))} items.")

    # print("Visualizing the R-tree...")
    # visualize_rtree(my_rtree, title="Sample R-tree Bounding Boxes")
    # print("Visualization complete.")

    # # You can also try with a different number of items or bounds
    # another_rtree = create_sample_rtree(num_items=5, bounds_range=(10, 50))
    # visualize_rtree(another_rtree, title="Smaller R-tree Example")
    my_rtree = create_sample_rtree(num_items=50, bounds_range=(0, 200))
    print(my_rtree)