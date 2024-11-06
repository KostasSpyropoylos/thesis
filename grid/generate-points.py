import os.path
import random 
class GeneratePoints:
    
    def __init__(self):
        if os.path.isfile('points.csv'):
            f = open("points.csv",'a')
            
        else:
            f = open("points.csv",'w')
            f.write(f"normLatitude,normLongitude\n")
        for i in range(10000):
            x,y = self.generateRandomCoordinates()
            f.write(f"{x},{y}\n")   
        f.close()
    def generateRandomCoordinates(self):
        x = self.non_uniform_random_1_to_3()
        y = self.non_uniform_random_1_to_3()
        return x,y    
    def non_uniform_random_1_to_3(self):
        # Generate a random float uniformly between 1 and 3
        uniform_random = random.uniform(1,2)
        
        # Apply a non-linear transformation to skew the distribution
        # Here, we'll use a square function as an example
        non_uniform = 1 + (uniform_random - 1) ** 2
        
        return non_uniform
            
g = GeneratePoints()