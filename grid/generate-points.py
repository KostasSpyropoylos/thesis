import os
import random

class GeneratePoints:
    def __init__(self):
        # Check if the file exists to decide append or write mode
        mode = 'a' if os.path.isfile('points.csv') else 'w'
        
        # Open file and handle context with "with" statement
        with open("points.csv", mode) as f:
            if mode == 'w':
                f.write("normLatitude,normLongitude\n")
            
            # Generate and write 10,000 random coordinates
            for _ in range(1000):
                latitude, longitude = self.generate_random_coordinates()
                f.write(f"{latitude},{longitude}\n")
    
    def generate_random_coordinates(self):
        latitude = self.non_uniform_random_0_to_3()
        longitude = self.non_uniform_random_0_to_3()
        return latitude, longitude
    
    def non_uniform_random_0_to_3(self):
        # Generate a uniform random float between 0 and 3
        uniform_random = random.uniform(0, 3)
        
        # Apply a non-linear transformation for non-uniform distribution
        # Using a square root transformation to skew towards lower values
        non_uniform = 3 * (uniform_random / 3) ** 0.5
        
        return non_uniform

# Instantiate the GeneratePoints class to run
g = GeneratePoints()
