import math


class Geometry:
    all = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        Geometry.all.append(self)

    def getGeometry(self):
        return self.x, self.y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __repr__(self) -> str:
        return f"Geometry(x={self.x} y={self.y})"


class Cell:
    cells = []

    def __init__(self, xmin=None, ymin=None, xmax=None, ymax=None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.geoms = []
        Cell.cells.append(self)

    def add(self, g):
        self.geoms.append(Geometry(g.x, g.y))

    def getGeometry(self):
        return self.geoms

    def subdivide(self, divisions=2):
        """Subdivide the cell into smaller cells."""
        subcells = []
        for i in range(divisions):
            row = []
            for j in range(divisions):
                xmin = self.xmin + i * 0.25
                xmax = self.xmin + (i + 1) * 0.25
                ymin = self.ymin + j * 0.25
                ymax = self.ymin + (j + 1) * 0.25
                row.append(Cell(xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin))
            subcells.append(row)
        return subcells

    def __repr__(self):
        return f"Cell({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax})"


class Grid:
    centroids = [[0 for x in range(20)] for x in range(20)]
    cell_radius = [[0 for x in range(20)] for x in range(20)]

    def __init__(self, xmin, ymin, xmax, ymax, m):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.m = m
        self.deltax = (self.xmax - self.xmin) / m
        self.deltay = (self.ymax - self.ymin) / m

        self.cells = [[0 for x in range(m)] for x in range(m)]
        self.points = [[0] * int(self.deltax)] * int(self.deltay)
        self.create_grid()

    def create_grid(self):
        for i in range(self.m):
            for j in range(self.m):
                xmin = self.xmin + i * self.deltax
                xmax = self.xmin + (i + 1) * self.deltax
                ymin = self.ymin + j * self.deltay
                ymax = self.ymin + (j + 1) * self.deltay
                self.cells[i][j] = Cell(xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin)
                self.centroids[i][j] = [(xmax + xmin) / 2, (ymax + ymin) / 2]

    def assignPointsToGrid(self, data):
        for x, y in data:
            geom = Geometry(x, y)
            self.add(geom)
        for i in range(self.m):
            for j in range(self.m):
                self.centroids[i][j] = self.centroid(self.cells[i][j].getGeometry())
        self.getCellRadius()

    def add(self, g):
        cell = self.findCell(g.x, g.y)
        cell.add(Geometry(g.x, g.y))
        self.points.append(cell)

    def findCell(self, x, y):
        i = (int)((x - self.xmin) / self.deltax)
        j = (int)((y - self.ymin) / self.deltay)
        return self.cells[i][j]

    def centroid(self, points):
        """Function that finds each cell centroid by adding all the coordinates
        and dividing by the length of them"""

        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        _len = len(points)
        if _len > 0:
            centroid_x = sum(x_coords) / _len
            centroid_y = sum(y_coords) / _len
        else:
            centroid_x = 0
            centroid_y = 0
        return [centroid_x, centroid_y]

    def divideGrid(self, subdivisions=2):
        new_grid = []
        for row in self.cells:
            subdivided_rows = [[], []]
            for cell in row:
                subcells = cell.subdivide(2)
                subdivided_rows.extend(subcells)
            new_grid.extend(subdivided_rows)
        return new_grid

    def getCellRadius(self):
        for i in range(self.m):
            for j in range(self.m):
                for geom in self.cells[i][j].getGeometry():
                    dist = self.getDistance(geom, self.centroids[i][j])
                    if dist > self.cell_radius[i][j]:
                        self.cell_radius[i][j] = dist

    def getDistance(self, geom, centroid):
        dist = math.sqrt(
            math.pow(abs(centroid[0] - geom.x), 2)
            + math.pow(abs(centroid[1] - geom.y), 2)
        )
        return dist

    def getGeometries(self):
        lats = []
        longs = []
        for geom in Geometry.all:
            lats.append(geom.y)
            longs.append(geom.x)
        return longs, lats
