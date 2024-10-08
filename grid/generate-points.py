import os.path
import random 
class GeneratePoints:
    
    def __init__(self):
        if os.path.isfile('points.txt'):
            f = open("points.txt",'a')
            
        else:
            f = open("points.txt",'w')
        for i in range(10):
            x,y = self.generateRandomCoordinates()
            f.write(f"{x},{y}\n")   
        f.close()
    def generateRandomCoordinates(self):
        x = random.uniform(0,10.93)
        y = random.uniform(0,10.93)
        return x,y    

            
g = GeneratePoints()