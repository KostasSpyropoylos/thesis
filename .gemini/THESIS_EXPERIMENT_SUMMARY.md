# Thesis Experiment Strategy & Update Roadmap

This document serves as an optimized mental model mapping the original thesis report (`ΤΕΧΝΙΚΗ ΑΝΑΦΟΡΑ ΠΤΥΧΙΑΚΗ v1.md`) to the newly refactored experimental pipeline (`main.py`, scalable datasets, etc.). It acts as a bridge for future updates to the official thesis document.

## 1. Core Thesis Objective Alignment
The core goal defined in the thesis is to evaluate K-Means against Grid-based and R-Tree spatial indexing techniques, primarily to minimize overlapping clusters on **skewed** and **overlapping** datasets while ensuring 100% data coverage.

**How our new implementation achieves this:**
- We ensure a mathematically fair comparison by explicitly restricting Grid and R-Tree to output exactly $k$ clusters (matching K-Means).
- We test this across dynamically scaled datasets up to 100,000 points.
- We accurately measure the overlap metric using the provided circular intersection math (Case 1, 2, and 3).

---

## 2. What Needs to be Updated in the Thesis Later

Based on the original report, here are the key sections we will need to rewrite or expand to reflect our new advanced implementation:

### A. Section 4: Techniques and Overlap Reduction
- **Grid Updates (4.1):** We must add documentation on the `enforce_k_groups(k)` method (Agglomerative Hierarchical Clustering) that post-processes the cells to exactly $k$ clusters. We must also document **Boundary Jittering** (random shifts of xmin/ymin) introduced to mitigate the Modifiable Areal Unit Problem (MAUP) across multiple runs.
- **R-Tree Updates (4.2):** We must replace mentions of standard incremental R-Tree insertion with the new **STR (Sort-Tile-Recursive) Bulk Loading** approach. This guarantees minimal overlap bottom-up. We also need to add the leaf-agglomeration to enforce the $k$ restriction.

### B. Section 6: Algorithm Code Description
- **Data Generation (6.1):** Update this section to state that the dataset pipeline (`utils/generate_large_datasets.py`) now generates enterprise-scale datasets (10k, 50k, 100k points) spanning tightly clustered, widespread, and heavily skewed scenarios, rather than just small 1,000-point subsets.
- **Algorithm Architecture (6.2):** We need to mention the multi-run strategy (`n_runs=100`) wrapped inside `main.py` which tracks the best overlap configuration and monitors RAM (using `psutil`) to prevent OOP memory leaks via `Geometry.clear_all()`.

### C. Section 7: Experimental Evaluation
- We will need to inject the newly generated empirical results (`experiment_results.csv`) into the thesis.
- We must showcase the automatically generated visualizations located in `images/run-expirement/` (e.g., `kmeans_skewed_high_10000_k50.png`) to visually prove how Grid and R-Tree dynamically adapt to skewed data boundaries compared to K-Means.

---

## 3. Immediate Takeaways for the Agent
1. **The Math is Validated:** The overlap logic specified in Section 7.1.1 (the trigonometric intersection of circles) matches the implementation in the codebase perfectly.
2. **K-Groups is Critical:** The thesis emphasizes creating "distinct boundaries" and "complete coverage". Agglomerative clustering to force $k$ groups satisfies this thesis goal flawlessly without dropping outlier points (unlike DBSCAN).
3. **Execution Scale:** The thesis originally aimed for theoretical proofs, but the current pipeline proves it practically at large scales.

**Next Steps:** Use this summary as the foundation to rewrite and inject content directly into `ΤΕΧΝΙΚΗ ΑΝΑΦΟΡΑ ΠΤΥΧΙΑΚΗ v1.md` when the user requests the final documentation polish.
