import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def visualize_dataset(file_path="./datasets/skewed_coords.csv",output_name="visualized_coords.png"):
    try:
        df = pd.read_csv(file_path)
        
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return

    if df.empty:
        print("No data available.")
        return

    fig, ax = plt.subplots(figsize=(10, 10))
    

    # ax.scatter(df['normLongitude'], df['normLatitude'], c='blue', edgecolors='white')
    ax.scatter(df['longitude'], df['latitude'], c='blue', edgecolors='white')

    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Coordinate Distribution")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle="--", alpha=0.7)
    
    plt.savefig(output_name)
    print(f"Visualization saved successfully as {output_name}")
    
    plt.close(fig)
        
        
visualize_dataset()