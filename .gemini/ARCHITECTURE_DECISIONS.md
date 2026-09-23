# Experimental Architecture & Design Decisions

This document outlines the recent refactoring of the spatial clustering comparison pipeline (K-Means vs. Grid-Based vs. R-Tree). It serves as documentation for the methodology used to enforce fair constraints, scale the experiments, and the rationale behind the chosen architectural techniques over available alternatives.

---

## 1. Strict k-Groups Constraint

**Problem:** To compare different clustering algorithms fairly, they must all output the exact same number of clusters ($k$). Initially, K-Means outputted $k$, but the Grid and R-Tree methods outputted a variable number of groups depending on data density and leaf capacity.

**Implementation:** 
An `enforce_k_groups(k)` post-processing step was introduced for both `Grid` and `RTreeSpatialAnalyzer`. 
- **Grid:** We extract all non-empty grid cells and their centroids.
- **R-Tree:** We extract all leaf nodes and the centers of their Minimum Bounding Rectangles (MBRs).
We then run an Agglomerative Hierarchical Clustering (`sklearn.cluster.AgglomerativeClustering` with average linkage) on these centers to merge the closest cells/leaves until exactly $k$ groups remain. A new covering bounding circle is generated for each merged super-group.

**Alternative Techniques Rejected:**
1. **Dynamic Parameter Tuning:** We could have written a search algorithm to dynamically guess the Grid's $m \times m$ resolution or the R-Tree's node capacity until it happens to produce $k$ clusters. 
   * *Why Rejected:* Highly unpredictable, non-linear, and computationally expensive. Small parameter tweaks often jump from $k=15$ directly to $k=30$ without hitting $k=20$.
2. **K-Means on the Grid/R-Tree Centers:** We could have run K-Means on the initial valid cells to group them into $k$.
   * *Why Rejected:* Running K-Means inside the Grid/R-Tree implementation conceptually dilutes the spatial comparison. By using hierarchical agglomerative clustering, we strictly respect and merge *adjacent spatial neighborhoods* bottom-up, keeping the core philosophy of spatial partitioning intact.

---

## 2. Multi-Run Execution & Handling Non-Determinism

**Problem:** The spatial clustering algorithms exhibit variance depending on initialization or boundary placement. Comparing a single execution of each method could lead to statistical anomalies.

**Implementation:** 
The pipeline in `main.py` evaluates each algorithm `n_runs` times (e.g., 5, 10, or 50 times) per $k$ and logs the execution that yielded the **minimum overlap area**.
- **K-Means:** Relies on its natural `init` non-determinism.
- **Grid:** Implemented **Boundary Jittering**. The starting bounding box `(xmin, ymin)` is shifted by a random continuous value between `[0, 0.5]` for every run.
- **R-Tree (STR):** Implemented **Micro-Variance**. We add tiny random noise (`1e-8`) to the dataset before insertion to subtly alter the sorting order without violating coordinate integrity.

**Alternative Techniques Rejected:**
- **Standardizing a Single Fixed Seed:** We could have forced a static seed to ensure the script does the exact same thing every time.
   * *Why Rejected:* This introduces bias. Grid algorithms suffer from the *Modifiable Areal Unit Problem (MAUP)*. If a highly dense data clump happens to fall exactly on a grid boundary line in the single deterministic run, the Grid algorithm is unfairly penalized. Jittering averages out these boundary artifacts for a scientifically sound comparison.

---

## 3. Sort-Tile-Recursive (STR) Bulk Loading for R-Tree

**Problem:** Standard dynamic R-trees suffer from "dead space" (high overlap between MBRs) because they insert points one by one, making the tree heavily dependent on the insertion sequence.

**Implementation:** 
Switched to a generator-based bulk loading approach using `rtree.index.Index(stream_data())`. 

**Alternative Techniques Rejected:**
- **Dynamic Pointwise Insertion (Previous Approach):** Inserting `df.iterrows()` into the tree iteratively.
   * *Why Rejected:* Pointwise insertion leads to severe tree degradation on static datasets. STR (Sort-Tile-Recursive) builds the tree bottom-up by mathematically sorting and tiling the data into perfectly packed nodes. This ensures minimal bounding box overlap—directly optimizing our primary evaluation metric.

---

## 4. Scaled Experimental Pipeline & Memory Tracking

**Problem:** Running 3 algorithms $\times$ 5 $k$-values $\times$ 50 runs = 750 heavy spatial evaluations. Memory leaks and execution tracking become a major issue.

**Implementation:**
- Rewrote `main.py` to loop systematically, track cumulative time, and save results to `experiment_results.csv`.
- Used `psutil` to track RAM (RSS) usage after every parameter sweep.
- Explicit memory clearing via `Geometry.clear_all()` was implemented.

**Alternative Techniques Rejected:**
- **Relying on Python's Garbage Collector:** 
   * *Why Rejected:* Custom OOP structures (like appending `self` to a class attribute `Geometry.all`) establish persistent references. Relying on default garbage collection would cause a memory leak accumulating millions of geometries across 750 runs, crashing the system. Explicit memory clearance guarantees O(1) memory complexity across infinite runs.

---

## 5. Automated Cluster Visualization

**Problem:** Numerical overlap scores don't provide intuition about *why* an algorithm failed or succeeded geometrically. 

**Implementation:**
A uniform plotting function was integrated to save the **best** clustering layout for each algorithm and each $k$ natively to `images/run-expirement/`. This enforces visual verification of the numerical overlap metric.
