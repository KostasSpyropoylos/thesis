class Geometry:
    all = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        Geometry.all.append(self)

    def get_geometry(self):
        return self.x, self.y

    def __repr__(self) -> str:
        return f"Geometry(x={self.x}, y={self.y})"

    @classmethod
    def clear_all(cls):
        cls.all = []

