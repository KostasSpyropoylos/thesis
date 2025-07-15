import os
import random
from scipy.stats import skewnorm
import pandas as pd


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


# g = GeneratePoints()

def generate_skewed_coordinates_and_save(
    num_points: int,
    latitude_skew: float,
    longitude_skew: float,
    output_filepath: str,
    lat_min: float = -90.0,
    lat_max: float = 90.0,
    lon_min: float = -180.0,
    lon_max: float = 180.0
):
    """
    Generates a dataset of latitudes and longitudes with skewed distributions
    and saves them to a specified file.

    The skewness of the distribution for both latitudes and longitudes can be
    controlled. The generated coordinates are scaled to fit within standard
    geographical bounds.

    Args:
        num_points (int): The number of coordinate pairs (latitude, longitude) to generate.
        latitude_skew (float): The skewness parameter for the latitude distribution.
                                A positive value skews the distribution towards lower
                                latitudes, a negative value towards higher latitudes.
                                A value of 0 results in a symmetric distribution.
        longitude_skew (float): The skewness parameter for the longitude distribution.
                                 A positive value skews towards lower longitudes,
                                 a negative value towards higher longitudes.
                                 A value of 0 results in a symmetric distribution.
        output_filepath (str): The path to the file where the generated coordinates
                                will be saved (e.g., 'coordinates.csv').
        lat_min (float): Minimum possible latitude value. Defaults to -90.0.
        lat_max (float): Maximum possible latitude value. Defaults to 90.0.
        lon_min (float): Minimum possible longitude value. Defaults to -180.0.
        lon_max (float): Maximum possible longitude value. Defaults to 180.0.

    Returns:
        None: The function saves the data to a file and does not return any value.
    """
    if num_points <= 0:
        print("Error: num_points must be a positive integer.")
        return

    # Generate skewed random numbers for latitudes
    # We use a standard normal distribution and then transform it
    # The `loc` and `scale` parameters of skewnorm are for mean and std dev of the underlying normal distribution
    # We'll map the generated values to the desired geographical range later
    latitudes_raw = skewnorm.rvs(a=latitude_skew, size=num_points)

    # Generate skewed random numbers for longitudes
    longitudes_raw = skewnorm.rvs(a=longitude_skew, size=num_points)

    # Scale raw values to fit within geographical bounds
    # First, normalize to [0, 1] range based on their min/max
    lat_norm = (latitudes_raw - latitudes_raw.min()) / (latitudes_raw.max() - latitudes_raw.min())
    lon_norm = (longitudes_raw - longitudes_raw.min()) / (longitudes_raw.max() - longitudes_raw.min())

    # Then, scale to the desired geographical range
    latitudes = lat_min + lat_norm * (lat_max - lat_min)
    longitudes = lon_min + lon_norm * (lon_max - lon_min)

    # Combine into a DataFrame for easy saving
    coords_df = pd.DataFrame({
        'latitude': latitudes,
        'longitude': longitudes
    })

    # Save to CSV
    try:
        coords_df.to_csv(output_filepath, index=False)
        print(f"Successfully generated {num_points} skewed coordinates and saved to '{output_filepath}'")
    except Exception as e:
        print(f"Error saving data to file: {e}")

# Example Usage:
# To use this function, you would call it like this:
generate_skewed_coordinates_and_save(
    num_points=100000,
    latitude_skew=-5,  # Skew towards higher latitudes (e.g., Northern Hemisphere)
    longitude_skew=3,  # Skew towards lower longitudes (e.g., Western Hemisphere)
    output_filepath='datasets/skewed_coords.csv'
)


# You can then load and visualize this data.
# For example, to load:
# import pandas as pd
# loaded_data = pd.read_csv('skewed_coords.csv')
# print(loaded_data.head())
