import os
import random
from scipy.stats import skewnorm
import pandas as pd
import numpy as np


class GeneratePoints:
    def __init__(self):

        mode = "a" if os.path.isfile("points.csv") else "w"

        with open("points.csv", mode) as f:
            if mode == "w":
                f.write("normLatitude,normLongitude\n")

            for _ in range(1000):
                latitude, longitude = self.generate_random_coordinates()
                f.write(f"{latitude},{longitude}\n")

    def generate_random_coordinates(self):
        latitude = self.non_uniform_random_0_to_3()
        longitude = self.non_uniform_random_0_to_3()
        return latitude, longitude

    def non_uniform_random_0_to_3(self):

        uniform_random = random.uniform(0, 3)

        non_uniform = 3 * (uniform_random / 3) ** 0.5

        return non_uniform


def generate_skewed_coordinates_and_save(
    num_points: int,
    latitude_skew: float,
    longitude_skew: float,
    output_filepath: str = "",
    lat_min: float = -4.0,
    lat_max: float = 4.0,
    lon_min: float = -4.0,
    lon_max: float = 4.0,
    random_seed: int = None,
    outlier_clip_percentile: float = 99.9,
    save_file=False,
    bounded: bool = True,
):
    """
    Generates skewed coordinates with outlier protection and reproducibility.
    """
    if num_points <= 0:
        raise ValueError("num_points must be a positive integer.")

    # Set seed for reproducibility
    if random_seed is not None:
        np.random.seed(random_seed)

    # 1. Generate Raw Data
    # skewnorm.rvs(a, loc, scale, size)
    latitudes_raw = skewnorm.rvs(a=latitude_skew, size=num_points)
    longitudes_raw = skewnorm.rvs(a=longitude_skew, size=num_points)

    # 2. Outlier Protection (Clip extreme tails before normalizing)
    # This prevents one random point from squishing the entire dataset.
    # We clip the top/bottom 0.1% (or custom percentile)
    lat_lower = np.percentile(latitudes_raw, 100 - outlier_clip_percentile)
    lat_upper = np.percentile(latitudes_raw, outlier_clip_percentile)
    lon_lower = np.percentile(longitudes_raw, 100 - outlier_clip_percentile)
    lon_upper = np.percentile(longitudes_raw, outlier_clip_percentile)

    # Clip the data to these robust bounds
    latitudes_raw = np.clip(latitudes_raw, lat_lower, lat_upper)
    longitudes_raw = np.clip(longitudes_raw, lon_lower, lon_upper)

    if bounded:
        # 3. Min-Max Normalization (now safe from extreme outliers)
        lat_norm = (latitudes_raw - latitudes_raw.min()) / (
            latitudes_raw.max() - latitudes_raw.min()
        )
        lon_norm = (longitudes_raw - longitudes_raw.min()) / (
            longitudes_raw.max() - longitudes_raw.min()
        )
    
        # 4. Scale to geographical bounds
        latitudes = lat_min + lat_norm * (lat_max - lat_min)
        longitudes = lon_min + lon_norm * (lon_max - lon_min)
    else:
        latitudes = latitudes_raw
        longitudes = longitudes_raw

    coords_df = pd.DataFrame({"latitude": latitudes, "longitude": longitudes})
    if save_file:
        try:
            coords_df.to_csv(output_filepath, index=False)
            print(f"Success: {num_points} points saved to '{output_filepath}'.")
        except Exception as e:
            print(f"Error saving file: {e}")
        return coords_df
    else:
        return coords_df


def generate_normal_coordinates(
    num_points: int = 1000,
    output_filepath: str = "",
    lat_mean: float = 0.0,
    lat_std: float = 1.0,
    lon_mean: float = 0.0,
    lon_std: float = 1.0,
    lat_min: float = -4.0,
    lat_max: float = 4.0,
    lon_min: float = -4.0,
    lon_max: float = 4.0,
    random_seed: int = None,
    outlier_clip_percentile: float = 99.9,
    save_file=False,
    bounded: bool = True,
):
    """
    Generates coordinates based on a Normal (Gaussian) distribution
    with outlier protection and reproducibility.
    """
    if num_points <= 0:
        raise ValueError("num_points must be a positive integer.")

    # Set seed for reproducibility
    if random_seed is not None:
        np.random.seed(random_seed)

    # 1. Generate Raw Data using Normal Distribution
    # np.random.normal(loc=mean, scale=std, size=num_points)
    latitudes_raw = np.random.normal(loc=lat_mean, scale=lat_std, size=num_points)
    longitudes_raw = np.random.normal(loc=lon_mean, scale=lon_std, size=num_points)

    # 2. Outlier Protection (Clip extreme tails before normalizing)
    # This prevents one random point from squishing the entire dataset.
    # We clip the top/bottom 0.1% (or custom percentile)
    # Note: For Normal distribution, percentile clipping is very effective at removing extreme tails.
    lower_p = 100 - outlier_clip_percentile
    upper_p = outlier_clip_percentile

    lat_lower = np.percentile(latitudes_raw, lower_p)
    lat_upper = np.percentile(latitudes_raw, upper_p)
    lon_lower = np.percentile(longitudes_raw, lower_p)
    lon_upper = np.percentile(longitudes_raw, upper_p)

    # Clip the data to these robust bounds
    latitudes_raw = np.clip(latitudes_raw, lat_lower, lat_upper)
    longitudes_raw = np.clip(longitudes_raw, lon_lower, lon_upper)

    if bounded:
        # 3. Min-Max Normalization
        # Transforms the bell curve to fit exactly within 0.0 to 1.0
        lat_norm = (latitudes_raw - latitudes_raw.min()) / (
            latitudes_raw.max() - latitudes_raw.min()
        )
        lon_norm = (longitudes_raw - longitudes_raw.min()) / (
            longitudes_raw.max() - longitudes_raw.min()
        )
    
        # 4. Scale to geographical bounds
        # Maps the 0-1 range to your lat_min/lat_max
        latitudes = lat_min + lat_norm * (lat_max - lat_min)
        longitudes = lon_min + lon_norm * (lon_max - lon_min)
    else:
        latitudes = latitudes_raw
        longitudes = longitudes_raw

    coords_df = pd.DataFrame({"latitude": latitudes, "longitude": longitudes})

    if save_file:
        try:
            if not output_filepath:
                output_filepath = "normal_dist_coordinates.csv"
            coords_df.to_csv(output_filepath, index=False)
            print(f"Success: {num_points} points saved to '{output_filepath}'.")
        except Exception as e:
            print(f"Error saving file: {e}")
        return coords_df
    else:
        return coords_df


if __name__ == "__main__":
    # tight_cluster
    generate_normal_coordinates(
        num_points=1000,
        lat_mean=0.0,
        lat_std=0.5,  # Tight spread
        lon_mean=0.0,
        lon_std=0.5,
        output_filepath="datasets/normal_coords_1.csv",
        save_file=True,
        random_seed=42,
    )

    # wide_sprawl
    generate_normal_coordinates(
        num_points=1000,
        lat_mean=0.0,
        lat_std=2.0,  # Wide spread
        lon_mean=0.0,
        lon_std=2.0,
        output_filepath="datasets/normal_coords_2.csv",
        save_file=True,
        random_seed=42,
    )

    # linear_corridor
    generate_normal_coordinates(
        num_points=1000,
        lat_mean=0.0,
        lat_std=0.3,  # Narrow height
        lon_mean=0.0,
        lon_std=3.0,  # Wide width
        output_filepath="datasets/normal_coords_3.csv",
        save_file=True,
        random_seed=42,
    )

    # off_center
    generate_normal_coordinates(
        num_points=1000,
        lat_mean=2.0,
        lat_std=1.0,
        lon_mean=2.0,
        lon_std=1.0,  # Shifted to top-right
        output_filepath="datasets/normal_coords_4.csv",
        save_file=True,
        random_seed=42,
    )
