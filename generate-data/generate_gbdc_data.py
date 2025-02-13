import pandas as pd
import numpy as np


def generate_clustered_data(
    num_clusters=5,
    points_per_cluster=100,
    lat_range=(1, 5),
    lon_range=(0, 5),
    spread=0.2,
    filename="grid/points.csv",
):
    """
    Generates synthetic clustered lat/lon data for testing GBDC.

    Args:
        num_clusters (int): Number of clusters to create.
        points_per_cluster (int): Number of points per cluster.
        lat_range (tuple): Min/max range for latitudes.
        lon_range (tuple): Min/max range for longitudes.
        spread (float): Standard deviation of clusters (lower = tighter clusters).
        filename (str): Output file path.
    """
    np.random.seed(42)
    latitudes = []
    longitudes = []

    cluster_centers = np.column_stack(
        (
            np.random.uniform(lon_range[0], lon_range[1], num_clusters),
            np.random.uniform(lat_range[0], lat_range[1], num_clusters),
        )
    )

    for center_lon, center_lat in cluster_centers:
        cluster_lons = np.random.normal(center_lon, spread, points_per_cluster)
        cluster_lats = np.random.normal(center_lat, spread, points_per_cluster)

        latitudes.extend(cluster_lats)
        longitudes.extend(cluster_lons)

    df = pd.DataFrame({"normLatitude": latitudes, "normLongitude": longitudes})
    df.to_csv(filename, index=False)
    print(f"Clustered data saved to {filename}")


generate_clustered_data()
