import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_charts(csv_path="experiment_results.csv", output_dir="images/charts"):
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path)
    
    if 'dataset' in df.columns:
        # Group by 'k' and calculate the mean across all 12 dataset configurations
        df = df.drop(columns=['dataset']).groupby('k').mean().reset_index()
        title_suffix = "(Mean across all 12 Dataset Variants)"
    else:
        title_suffix = "(skewed_high_10000)"
        
    k_vals = df['k']
    
    # 1. Overlap Comparison Chart
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, df['kmeans_overlap'], marker='o', label='K-Means', linewidth=2)
    plt.plot(k_vals, df['grid_overlap'], marker='s', label='Grid', linewidth=2)
    plt.plot(k_vals, df['rtree_overlap'], marker='^', label='R-Tree', linewidth=2)
    plt.title(f'Cluster Overlap Area vs. k {title_suffix}', fontsize=14)
    plt.xlabel('Number of Clusters (k)', fontsize=12)
    plt.ylabel('Total Overlap Area', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f'{output_dir}/overlap_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Execution Time Comparison Chart
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, df['kmeans_time'], marker='o', label='K-Means', linewidth=2)
    plt.plot(k_vals, df['grid_time'], marker='s', label='Grid', linewidth=2)
    plt.plot(k_vals, df['rtree_time'], marker='^', label='R-Tree', linewidth=2)
    plt.title(f'Execution Time vs. k {title_suffix}\n(Total over 100 runs)', fontsize=14)
    plt.xlabel('Number of Clusters (k)', fontsize=12)
    plt.ylabel('Time (Seconds)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f'{output_dir}/time_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Memory Usage Chart
    plt.figure(figsize=(10, 6))
    plt.plot(k_vals, df['memory_mb'], marker='d', color='purple', label='RAM Usage (MB)', linewidth=2)
    plt.title(f'Memory Consumption Across k-Evaluations {title_suffix}', fontsize=14)
    plt.xlabel('Number of Clusters (k)', fontsize=12)
    plt.ylabel('Memory (MB)', fontsize=12)
    # Set y-axis bounds to show it's relatively flat
    plt.ylim(0, df['memory_mb'].max() * 1.5)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f'{output_dir}/memory_usage.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Successfully generated 3 comparison charts in {output_dir}/")

if __name__ == "__main__":
    generate_charts("../experiment_results.csv", "../images/charts")
