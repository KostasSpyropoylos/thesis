from geometry import Geometry

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
