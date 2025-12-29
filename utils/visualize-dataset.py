import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_skewed_coords(file_path="./datasets/skewed_coords.csv", output_name="coord_analysis.png"):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # Create a figure with a complex layout
    fig = plt.figure(figsize=(16, 12))
    grid = plt.GridSpec(2, 2, wspace=0.3, hspace=0.3)

    # 1. Hexbin Plot (Density Analysis)
    # Better than scatter for skewed data because it shows where the "mass" is.
    ax_hex = fig.add_subplot(grid[0, 0])
    hb = ax_hex.hexbin(df['longitude'], df['latitude'], gridsize=30, cmap='YlOrRd', mincnt=1)
    fig.colorbar(hb, ax=ax_hex, label='Point Count')
    ax_hex.set_title("Density Heatmap (Hexbin)")
    ax_hex.set_xlabel("Longitude")
    ax_hex.set_ylabel("Latitude")

    # 2. Joint Plot Style (Marginal Distributions)
    # This helps see exactly which axis is causing the skew.
    ax_main = fig.add_subplot(grid[0, 1])
    sns.kdeplot(data=df, x='longitude', y='latitude', ax=ax_main, fill=True, thresh=0.05, cmap="Blues")
    ax_main.scatter(df['longitude'], df['latitude'], s=1, alpha=0.3, color='black')
    ax_main.set_title("KDE Contour + Scatter Overlay")

    # 3. Longitude Skewness (CDF)
    ax_long = fig.add_subplot(grid[1, 0])
    sns.ecdfplot(data=df, x='longitude', ax=ax_long, color='red')
    ax_long.set_title("Longitude Cumulative Distribution")
    ax_long.grid(True, alpha=0.3)

    # 4. Latitude Skewness (CDF)
    ax_lat = fig.add_subplot(grid[1, 1])
    sns.ecdfplot(data=df, x='latitude', ax=ax_lat, color='green')
    ax_lat.set_title("Latitude Cumulative Distribution")
    ax_lat.grid(True, alpha=0.3)

    plt.suptitle(f"Spatial Skew Analysis: {file_path}", fontsize=16)
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Advanced analysis saved as {output_name}")

analyze_skewed_coords()