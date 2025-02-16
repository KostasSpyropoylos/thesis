import math

import math


class Geometry:
    all = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        Geometry.all.append(self)

    def getGeometry(self):
        return self.x, self.y

    def __repr__(self) -> str:
        return f"Geometry(x={self.x}, y={self.y})"


class Cell:
    def __init__(self, xmin=None, ymin=None, xmax=None, ymax=None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.geoms = []

    def add(self, g):
        """Add a geometry to the cell"""
        self.geoms.append(g)

    def getGeometry(self):
        """Return geometries assigned to this cell"""
        return self.geoms

    def getCentroid(self):
        """Compute and return centroid"""
        return [(self.xmin + self.xmax) / 2, (self.ymin + self.ymax) / 2]

    def __repr__(self):
        return f"Cell({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax})"


class Grid:
    def __init__(self, xmin, ymin, xmax, ymax, m):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.m = m
        self.deltax = (self.xmax - self.xmin) / m
        self.deltay = (self.ymax - self.ymin) / m

        # Initialize grid with empty cells
        self.cells = [
            [
                Cell(
                    xmin=self.xmin + i * self.deltax,
                    xmax=self.xmin + (i + 1) * self.deltax,
                    ymin=self.ymin + j * self.deltay,
                    ymax=self.ymin + (j + 1) * self.deltay,
                )
                for j in range(m)
            ]
            for i in range(m)
        ]

        # Centroids and radius storage
        self.centroids = [[cell.getCentroid() for cell in row] for row in self.cells]
        self.cell_radius = [[0 for _ in range(m)] for _ in range(m)]

    def findCell(self, x, y):
        """Find the appropriate cell for a given (x, y) coordinate."""
        i = min(max(int((x - self.xmin) / self.deltax), 0), self.m - 1)
        j = min(max(int((y - self.ymin) / self.deltay), 0), self.m - 1)
        return self.cells[i][j], i, j

    def assignPointsToGrid(self, data):
        """Assign points to their respective grid cells and update centroids and radius"""
        for x, y in data:
            geom = Geometry(x, y)
            cell, i, j = self.findCell(x, y)
            cell.add(geom)

        # Compute centroids and update radius
        self.updateCentroidsAndRadius()

    def updateCentroidsAndRadius(self):
        """Recalculate centroids and update the radius for each cell"""
        for i in range(self.m):
            for j in range(self.m):
                cell = self.cells[i][j]
                points = cell.getGeometry()

                if points:
                    centroid = self.computeCentroid(points)
                    self.centroids[i][j] = centroid
                    self.cell_radius[i][j] = max(
                        self.getDistance(p, centroid) for p in points
                    )
                else:
                    self.cell_radius[i][j] = 0

    def computeCentroid(self, points):
        """Compute centroid as the mean of all points in a cell"""
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        return (
            [sum(x_coords) / len(points), sum(y_coords) / len(points)]
            if points
            else [0, 0]
        )

    def getDistance(self, geom, centroid):
        """Compute Euclidean distance between a geometry and a centroid"""
        return math.sqrt((centroid[0] - geom.x) ** 2 + (centroid[1] - geom.y) ** 2)

    def getGeometries(self):
        """Return all geometries as separate lists of latitudes and longitudes"""
        longs, lats = zip(*[(geom.x, geom.y) for geom in Geometry.all])
        return list(longs), list(lats)

    def findOverlappingClusters(self):
        """Finds all overlapping clusters based on centroid distance and radius."""
        overlapping_clusters = []

        for i in range(self.m):
            for j in range(self.m):
                centroid1 = self.centroids[i][j]
                radius1 = self.cell_radius[i][j]

                if radius1 == 0: 
                    continue

                for k in range(self.m):
                    for l in range(self.m):
                        # Same cell, skip
                        if (i, j) == (k, l): 
                            continue

                        centroid2 = self.centroids[k][l]
                        radius2 = self.cell_radius[k][l]

                        if radius2 == 0:  
                            continue

                        
                        distance = math.sqrt(
                            (centroid2[0] - centroid1[0]) ** 2
                            + (centroid2[1] - centroid1[1]) ** 2
                        )

                        if distance < (radius1 + radius2):
                            overlapping_clusters.append(((i, j), (k, l)))

        return overlapping_clusters
