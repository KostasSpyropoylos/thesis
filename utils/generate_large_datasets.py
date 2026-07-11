import os
from generate_points import generate_normal_coordinates, generate_skewed_coordinates_and_save

def generate_all_large_datasets():
    # Ensure datasets directory exists
    os.makedirs("../datasets", exist_ok=True)
    
    # We will generate datasets of sizes 10k, 50k, 100k
    sizes = [10000, 50000, 100000]
    
    for size in sizes:
        print(f"Generating datasets for size: {size}...")
        
        # 1. Tight Cluster (Normal)
        generate_normal_coordinates(
            num_points=size,
            lat_mean=0.0, lat_std=0.5,
            lon_mean=0.0, lon_std=0.5,
            output_filepath=f"../datasets/normal_tight_{size}.csv",
            save_file=True, random_seed=42
        )
        
        # 2. Wide Sprawl (Normal)
        generate_normal_coordinates(
            num_points=size,
            lat_mean=0.0, lat_std=2.0,
            lon_mean=0.0, lon_std=2.0,
            output_filepath=f"../datasets/normal_wide_{size}.csv",
            save_file=True, random_seed=42
        )
        
        # 3. Highly Skewed (Skewed)
        generate_skewed_coordinates_and_save(
            num_points=size,
            latitude_skew=10, longitude_skew=-5,
            output_filepath=f"../datasets/skewed_high_{size}.csv",
            save_file=True, random_seed=42
        )
        
        # 4. Moderately Skewed (Skewed)
        generate_skewed_coordinates_and_save(
            num_points=size,
            latitude_skew=-5, longitude_skew=10,
            output_filepath=f"../datasets/skewed_mod_{size}.csv",
            save_file=True, random_seed=42
        )

if __name__ == "__main__":
    generate_all_large_datasets()
    print("Large datasets successfully generated in the datasets directory.")
