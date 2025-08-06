import math
from math import acos, sin, sqrt
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
import pandas as pd
import numpy as np

def compute_cluster_radii(X, labels, centers):
    """
    Compute the radius of each cluster, defined as the maximum distance
    from any point in the cluster to the cluster centroid.
    """
    num_clusters = len(centers)
    radii = np.zeros(num_clusters)
    X_np = X

    for i in range(num_clusters):
        cluster_points = X_np[labels == i]
        if len(cluster_points) > 0:
            radii[i] = max(euclidean(p, centers[i]) for p in cluster_points)

    return radii


import math

def compute_total_overlap(centers: list[tuple[float, float]], radii: list[float]) -> float:
    """
    Compute total overlap across all clusters (circles).

    Args:
        centers: A list of tuples, where each tuple (x, y) represents the
                 coordinates of a circle's center.
        radii: A list of floats, where each float represents the radius
               of a corresponding circle.

    Returns:
        The total overlapping area among all pairs of circles.

    Raises:
        ValueError: If radii is None or an empty list.
    """
    if radii is None or len(radii) == 0:
        raise ValueError("Radii computation failed, received None or empty array.")

    total_overlap = 0.0
    num_clusters = len(centers)

    for i in range(num_clusters):
        r1 = radii[i]
        # Optimization: Start j from i + 1 to avoid duplicate calculations (pair (A,B) is same as (B,A))
        # and to avoid comparing a circle with itself.
        for j in range(i + 1, num_clusters):
            r2 = radii[j]

            # Calculate the distance between the centers of the two circles
            distance = math.sqrt(
                (centers[i][0] - centers[j][0]) ** 2 +
                (centers[i][1] - centers[j][1]) ** 2
            )

            # Case 1: Circles do not overlap (distance is greater than or equal to the sum of radii)
            if distance >= (r1 + r2):
                continue

            # Case 2: One circle is completely contained within the other
            # The overlap area is the area of the smaller circle
            if distance <= abs(r1 - r2):
                total_overlap += math.pi * min(r1, r2) ** 2
                continue

            # Case 3: Circles partially overlap
            # Use the formula for the area of intersection of two circles
            # d = distance between centers
            # r1, r2 = radii of the circles

            # Calculate arguments for math.acos.
            # Clamp values to [-1, 1] to prevent ValueError due to floating-point inaccuracies.
            arg1 = (distance**2 + r1**2 - r2**2) / (2 * distance * r1)
            arg2 = (distance**2 + r2**2 - r1**2) / (2 * distance * r2)

            arg1 = max(-1.0, min(1.0, arg1))
            arg2 = max(-1.0, min(1.0, arg2))

            part1 = r1**2 * math.acos(arg1)
            part2 = r2**2 * math.acos(arg2)
            
            # The square root part of the formula, representing the area of a triangle formed by centers and intersection points
            part3 = 0.5 * math.sqrt(
                (-distance + r1 + r2) *
                (distance + r1 - r2) *
                (distance - r1 + r2) *
                (distance + r1 + r2)
            )
            
            total_overlap += (part1 + part2 - part3)

    return total_overlap

def evaluate_kmeans_overlap(X, n_clusters):
    """
    Run KMeans clustering and compute total overlap.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_
    radii = compute_cluster_radii(X, labels, centers)

    return compute_total_overlap(centers, radii), labels, centers, radii
