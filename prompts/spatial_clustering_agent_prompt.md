Role: You are an expert Python Data Scientist and Software Engineer.
Task: Refactor and extend an existing Python codebase that compares different spatial clustering/grouping algorithms (k-means, R-tree, and Grid-based partitioning).

Based on recent code review feedback, the current experimental methodology needs significant improvements to ensure a fair and scientifically sound comparison. Please implement the following 4 major updates:

1. Ensure Fair Comparison (Strict k-Groups Constraint)
Currently, the methods do not output the same number of clusters/groups, making the comparison unfair.

Requirement: All algorithms (k-means, R-tree, Grid) must be parameterized or post-processed to output exactly k groups.

Action: Adapt the Grid and R-tree implementations (either via algorithmic variations, hierarchical merging, or post-processing heuristics) so that their final output strictly matches the target k value provided to k-means.

2. Implement Multi-Run Execution (Handling Non-Determinism)
The algorithms exhibit non-deterministic behavior or high sensitivity to initial parameters (k-means depends on init centers, standard R-tree depends on insertion order, Grid depends on granularity).

Requirement: Each algorithm must be executed multiple times (e.g., n_runs = 50 or 100).

Action: Implement an evaluation metric to assess the quality of the clustering/grouping (e.g., minimum overlap, WCSS/inertia, or Silhouette score). Create a multi-run loop for each method, evaluate every run, and only retain and return the best result for the final comparison.

3. Implement STR R-Tree (Sort-Tile-Recursive)
To improve the R-tree performance and minimize bounding box overlap, we need to switch from a standard dynamic insertion R-tree to a bulk-loaded variant.

Requirement: Implement the STR (Sort-Tile-Recursive) algorithm for the R-tree.

Action: Use Python libraries that support STR bulk loading (e.g., the rtree package which uses libspatialindex under the hood, or implement a custom STR packing logic before building the tree) to ensure the data is sorted and tiled before insertion.

4. Expand the Experimental Setup & Scalability
The experimental pipeline needs to handle scale and hyperparameter sweeps.

Requirement: The setup must evaluate large datasets and varying values of k.

Action: * Update the data generation/loading pipeline to efficiently handle datasets on the scale of millions of points.

Create a parameter grid that iterates over k = [10, 20, 30, 40, 50].

Ensure the logging, memory management, and execution times are optimized and recorded for these large-scale runs.

Output Expectations:

Provide the updated Python code for the main experimental loop and the modified algorithm wrappers.

Clearly comment on where the "k-groups" constraint is enforced for R-tree and Grid.

Specify which metric you chose to define the "best" run in the multi-run execution.