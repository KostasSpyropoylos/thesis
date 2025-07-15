import pandas as pd
import numpy as np
import math

def load_data(path:str):
    """
    Load data from a CSV file and extract latitude and longitude columns.
    Args:
        path (str): Path to the CSV file.
        \n example "grid/points.csv"
    Returns:
        tuple: A tuple containing the latitude and longitude Series.
    """
    
    csv_data = pd.read_csv(f"{path}")
    latitudes = csv_data["normLatitude"]
    longitudes = csv_data["normLongitude"]
    return latitudes, longitudes
    
    
    
def get_min_max_coordinates_from_dataset(path:str):
    """
    Loads geographical data from a specified path and calculates the minimum and maximum
    latitude and longitude values, rounded to the nearest integer. It also returns
    the combined longitude and latitude data as a NumPy array of points.

    Args:
        path (str): The file path to the dataset containing geographical data.
                    It is assumed that `load_data(path)` will return two
                    NumPy arrays: one for latitudes and one for longitudes.

    Returns:
        tuple: A tuple containing:
            - points_array (np.ndarray): A NumPy array where each row represents
                                         a geographical point [longitude, latitude].
            - minLongitude (int): The minimum longitude value, floored to the nearest integer.
            - minLatitude (int): The minimum latitude value, floored to the nearest integer.
            - maxLongitude (int): The maximum longitude value, ceiled to the nearest integer.
            - maxLatitude (int): The maximum latitude value, ceiled to the nearest integer.
    """
    latitudes, longitudes = load_data(path)
    maxLatitude = latitudes.max()
    minLatitude = latitudes.min()
    minLatitude = math.floor(minLatitude)
    maxLatitude = math.ceil(maxLatitude)

    maxLongitude = longitudes.max()
    maxLongitude = math.ceil(maxLongitude)

    minlongitude = longitudes.min()
    minlongitude = math.floor(minlongitude)

    points_array = np.column_stack((longitudes, latitudes))
    return points_array, minlongitude, minLatitude, maxLongitude, maxLatitude