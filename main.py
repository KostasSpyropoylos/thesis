import pandas as pd
import numpy as np
import math
import time
import psutil
import os
import sys
import matplotlib.pyplot as plt

# Add current directory to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from structures.grid import Geometry, Grid

from structures.r_tree_analyzer import RTreeSpatialAnalyzer
from utils.kmeans_evaluation import evaluate_kmeans_overlap

def get_memory_usage():
    """Returns the memory usage of the current process in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def save_visualization(data, centers, radii, title, filename):
    plt.figure(figsize=(10, 8))
    # plot data points
    plt.scatter(data[:, 1], data[:, 0], c='lightgray', s=10, alpha=0.5, label='Data')
    
    # plot centers and radii
    for i, (center, r) in enumerate(zip(centers, radii)):
        plt.scatter(center[1], center[0], c='red', marker='x', s=100)
        circle = plt.Circle((center[1], center[0]), r, color='blue', fill=False, linestyle='dashed')
        plt.gca().add_patch(circle)
        
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    # Ensure axes are equal so circles look like circles
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle=":", alpha=0.6)
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def run_experiments(file_path, k_values, n_runs=10):
    """
    Runs the experimental pipeline scaling over multiple k values and evaluating 
    clustering algorithms multiple times to ensure fair comparison and robustness.
    """
    print(f"--- Loading data from {file_path} ---")
    try:
        # Load dataset
        csv_data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please provide a valid dataset.")
        return

    dataset_name = os.path.splitext(os.path.basename(file_path))[0]

    # Use generic columns if normLatitude isn't present
    lat_col = "normLatitude" if "normLatitude" in csv_data.columns else "latitude"
    lon_col = "normLongitude" if "normLongitude" in csv_data.columns else "longitude"

    if lat_col not in csv_data.columns or lon_col not in csv_data.columns:
        print(f"Error: Could not find latitude/longitude columns in {file_path}")
        return

    latitudes = csv_data[lat_col]
    longitudes = csv_data[lon_col]
    
    min_lat = math.floor(latitudes.min())
    max_lat = math.ceil(latitudes.max())
    min_lon = math.floor(longitudes.min())
    max_lon = math.ceil(longitudes.max())
    
    kmeans_data = csv_data[[lat_col, lon_col]].to_numpy()
    
    results = []
    
    image_dir = "images/run-expirement"
    os.makedirs(image_dir, exist_ok=True)
    
    for k in k_values:
        print(f"\n======================================")
        print(f"     Evaluating k = {k} ")
        print(f"======================================")
        
        # 1. K-Means
        best_kmeans_score = float('inf')
        best_kmeans_centers = None
        best_kmeans_radii = None
        start_time = time.time()
        for run in range(n_runs):
            # K-means uses random initialization, so each run produces different results.
            overlap_score, labels, centers, radii = evaluate_kmeans_overlap(kmeans_data, n_clusters=k)
            if overlap_score < best_kmeans_score:
                best_kmeans_score = overlap_score
                best_kmeans_centers = centers
                best_kmeans_radii = radii
        kmeans_time = time.time() - start_time
        print(f"[K-Means] Best Overlap (k={k}): {best_kmeans_score:.4f} | Total Time ({n_runs} runs): {kmeans_time:.2f}s")
        
        # 2. Grid-based
        best_grid_score = float('inf')
        best_grid_centers = None
        best_grid_radii = None
        start_time = time.time()
        for run in range(n_runs):
            # Jitter the grid boundaries to simulate non-determinism/shift across multiple runs
            shift_x = np.random.uniform(0, 0.5)
            shift_y = np.random.uniform(0, 0.5)
            
            Geometry.clear_all()  # Ensure static list is clear for each run if needed (depends on implementation)
            grid = Grid(xmin=min_lon - shift_x, ymin=min_lat - shift_y, xmax=max_lon, ymax=max_lat, m=20)
            
            data_tuples = list(zip(longitudes, latitudes))
            grid.fit(data_tuples)
            
            # Enforce exact k groups (Fair Comparison)
            grid.enforce_k_groups(k)
            score = grid.compute_grid_overlap()
            
            if score < best_grid_score:
                best_grid_score = score
                best_grid_centers = [(c[1], c[0]) for c in grid.final_centroids] # (lat, lon) for compatibility with plot func which swaps
                best_grid_radii = grid.final_radii
        grid_time = time.time() - start_time
        print(f"[Grid]    Best Overlap (k={k}): {best_grid_score:.4f} | Total Time ({n_runs} runs): {grid_time:.2f}s")
        
        # 3. R-Tree (STR)
        best_rtree_score = float('inf')
        best_rtree_centers = None
        best_rtree_radii = None
        start_time = time.time()
        for run in range(n_runs):
            analyzer = RTreeSpatialAnalyzer()
            # load_data_from_csv now does STR bulk loading and adds a tiny random jitter automatically
            success = analyzer.load_data_from_csv(file_path, required_cols=[lat_col, lon_col])
            
            if success:
                # Enforce exact k groups (Fair Comparison)
                analyzer.enforce_k_groups(k)
                score = analyzer.compute_leaves_overlap(analyzer.final_clusters)
                
                if score < best_rtree_score:
                    best_rtree_score = score
                    # Convert to (lat, lon) format for standard plotting wrapper
                    best_rtree_centers = [(c["K"][1], c["K"][0]) for c in analyzer.final_clusters]
                    best_rtree_radii = [c["r"] for c in analyzer.final_clusters]
        rtree_time = time.time() - start_time
        print(f"[R-Tree]  Best Overlap (k={k}): {best_rtree_score:.4f} | Total Time ({n_runs} runs): {rtree_time:.2f}s")
        
        # Record Memory and Results
        mem_usage = get_memory_usage()
        print(f"\n=> Memory usage after k={k}: {mem_usage:.2f} MB")
        
        # Generate visualizations for the best run of each algorithm
        save_visualization(kmeans_data, best_kmeans_centers, best_kmeans_radii, f'K-Means Clusters (k={k}, Dataset={dataset_name})', f'{image_dir}/kmeans_{dataset_name}_k{k}.png')
        save_visualization(kmeans_data, best_grid_centers, best_grid_radii, f'Grid Clusters (k={k}, Dataset={dataset_name})', f'{image_dir}/grid_{dataset_name}_k{k}.png')
        save_visualization(kmeans_data, best_rtree_centers, best_rtree_radii, f'R-Tree Clusters (k={k}, Dataset={dataset_name})', f'{image_dir}/rtree_{dataset_name}_k{k}.png')
        print(f"=> Saved visualizations for k={k} in {image_dir}/")
        
        results.append({
            'dataset': dataset_name,
            'k': k,
            'kmeans_overlap': best_kmeans_score,
            'grid_overlap': best_grid_score,
            'rtree_overlap': best_rtree_score,
            'kmeans_time': kmeans_time,
            'grid_time': grid_time,
            'rtree_time': rtree_time,
            'memory_mb': mem_usage
        })
        
    print(f"\n[DONE] Completed evaluation for {dataset_name}.")
    return results


if __name__ == "__main__":
    import glob
    
    # Get all dataset paths
    dataset_paths = glob.glob("datasets/*.csv")
    
    if not dataset_paths:
        print("No valid dataset found in the expected locations.")
        sys.exit(1)
        
    # Parameter grid setup
    k_values = [10, 20, 30, 40, 50]
    num_runs = 5 # Set to a reasonable number to prevent extreme wait times across many datasets. Increase for thesis final run.
    
    all_results = []
    
    for file_path in dataset_paths:
        dataset_results = run_experiments(file_path, k_values, n_runs=num_runs)
        if dataset_results:
            all_results.extend(dataset_results)
            
    # Save all results to a master CSV
    df_all_results = pd.DataFrame(all_results)
    output_csv = "experiment_results.csv"
    df_all_results.to_csv(output_csv, index=False)
    print(f"\n[SUCCESS] Master experiment completed. All results saved to {output_csv}")
