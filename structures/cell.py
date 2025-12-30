from structures.geometry import Geometry

class Cell:
    def __init__(self, x_min=None, y_min=None, x_max=None, y_max=None):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.geoms = []

    def add(self, g):
        """Add a geometry to the cell"""
        self.geoms.append(g)

    def get_geometry(self):
        """Return geometries assigned to this cell"""
        return self.geoms

    def get_centroid(self):
        """Compute and return centroid"""
        return [(self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2]

    def __repr__(self):
        return f"Cell({self.x_min}, {self.x_max}, {self.y_min}, {self.y_max})"
