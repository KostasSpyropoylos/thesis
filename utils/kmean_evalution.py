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


def compute_total_overlap(centers, radii):
    """
    Compute total overlap across all clusters.
    """
    if radii is None or len(radii) == 0:
        raise ValueError("Radii computation failed, received None or empty array.")

    total_overlap = 0
    num_clusters = len(centers)
    Pi = 3.141592653589793

    for i in range(num_clusters):
        r1 = radii[i]
        for j in range(i + 1, num_clusters):
            r2 = radii[j]
            distance = math.sqrt(
                (centers[i][0] - centers[j][0]) ** 2
                + (centers[i][1] - centers[j][1]) ** 2
            )

            if distance > (r1 + r2):
                continue

            if distance <= abs(r1 - r2):
                total_overlap += Pi * min(r1, r2) ** 2
                continue

            part1 = r1**2 * math.acos(
                (distance**2 + r1**2 - r2**2) / (2 * distance * r1)
            )
            part2 = r2**2 * math.acos(
                (distance**2 + r2**2 - r1**2) / (2 * distance * r2)
            )
            part3 = 0.5 * math.sqrt(
                (-distance + r1 + r2)
                * (distance + r1 - r2)
                * (distance - r1 + r2)
                * (distance + r1 + r2)
            )

            total_overlap += part1 + part2 - part3

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
