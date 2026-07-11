import os
import shutil
from generate_points import generate_normal_coordinates, generate_skewed_coordinates_and_save

def generate_all_datasets():
    datasets_dir = "../datasets"
    
    # 1. Clean the old datasets
    if os.path.exists(datasets_dir):
        shutil.rmtree(datasets_dir)
    os.makedirs(datasets_dir, exist_ok=True)
    
    size = 10000
    
    print("Generating 4 Normal UNBOUNDED datasets...")
    generate_normal_coordinates(size, lat_mean=0, lat_std=10, lon_mean=0, lon_std=10, output_filepath=f"{datasets_dir}/normal_unbounded_1.csv", save_file=True, bounded=False, random_seed=42)
    generate_normal_coordinates(size, lat_mean=50, lat_std=5, lon_mean=-20, lon_std=15, output_filepath=f"{datasets_dir}/normal_unbounded_2.csv", save_file=True, bounded=False, random_seed=43)
    generate_normal_coordinates(size, lat_mean=-100, lat_std=50, lon_mean=100, lon_std=50, output_filepath=f"{datasets_dir}/normal_unbounded_3.csv", save_file=True, bounded=False, random_seed=44)
    generate_normal_coordinates(size, lat_mean=0, lat_std=1, lon_mean=0, lon_std=100, output_filepath=f"{datasets_dir}/normal_unbounded_4.csv", save_file=True, bounded=False, random_seed=45)
    
    print("Generating 4 Skewed UNBOUNDED datasets...")
    generate_skewed_coordinates_and_save(size, latitude_skew=10, longitude_skew=-5, output_filepath=f"{datasets_dir}/skewed_unbounded_1.csv", save_file=True, bounded=False, random_seed=46)
    generate_skewed_coordinates_and_save(size, latitude_skew=-10, longitude_skew=-10, output_filepath=f"{datasets_dir}/skewed_unbounded_2.csv", save_file=True, bounded=False, random_seed=47)
    generate_skewed_coordinates_and_save(size, latitude_skew=20, longitude_skew=5, output_filepath=f"{datasets_dir}/skewed_unbounded_3.csv", save_file=True, bounded=False, random_seed=48)
    generate_skewed_coordinates_and_save(size, latitude_skew=-20, longitude_skew=20, output_filepath=f"{datasets_dir}/skewed_unbounded_4.csv", save_file=True, bounded=False, random_seed=49)
    
    print("Generating 2 Normal BOUNDED [-4, 4] datasets...")
    generate_normal_coordinates(size, lat_mean=0, lat_std=2, lon_mean=0, lon_std=2, lat_min=-4, lat_max=4, lon_min=-4, lon_max=4, output_filepath=f"{datasets_dir}/normal_bounded_1.csv", save_file=True, bounded=True, random_seed=50)
    generate_normal_coordinates(size, lat_mean=2, lat_std=0.5, lon_mean=-2, lon_std=0.5, lat_min=-4, lat_max=4, lon_min=-4, lon_max=4, output_filepath=f"{datasets_dir}/normal_bounded_2.csv", save_file=True, bounded=True, random_seed=51)
    
    print("Generating 2 Skewed BOUNDED [-4, 4] datasets...")
    generate_skewed_coordinates_and_save(size, latitude_skew=15, longitude_skew=-15, lat_min=-4, lat_max=4, lon_min=-4, lon_max=4, output_filepath=f"{datasets_dir}/skewed_bounded_1.csv", save_file=True, bounded=True, random_seed=52)
    generate_skewed_coordinates_and_save(size, latitude_skew=-5, longitude_skew=5, lat_min=-4, lat_max=4, lon_min=-4, lon_max=4, output_filepath=f"{datasets_dir}/skewed_bounded_2.csv", save_file=True, bounded=True, random_seed=53)
    
    print("All 12 customized datasets successfully generated.")

if __name__ == "__main__":
    generate_all_datasets()
