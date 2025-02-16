import os
import random


class GeneratePoints:
    def __init__(self):

        mode = "a" if os.path.isfile("points.csv") else "w"

        with open("points.csv", mode) as f:
            if mode == "w":
                f.write("normLatitude,normLongitude\n")

            for _ in range(1000):
                latitude, longitude = self.generate_random_coordinates()
                f.write(f"{latitude},{longitude}\n")

    def generate_random_coordinates(self):
        latitude = self.non_uniform_random_0_to_3()
        longitude = self.non_uniform_random_0_to_3()
        return latitude, longitude

    def non_uniform_random_0_to_3(self):

        uniform_random = random.uniform(0, 3)

        non_uniform = 3 * (uniform_random / 3) ** 0.5

        return non_uniform


g = GeneratePoints()
