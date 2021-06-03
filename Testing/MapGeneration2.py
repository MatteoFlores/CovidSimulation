import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

shape = (100,100)
world = np.zeros(shape)
average = 0
leftVal = 0
botVal = 0
maxDivergence = 2
divergence = 0
world =  [[random.randint(0,1) for x in range(shape[0])] for y in range(shape[1])] 
count = 0

for a in range(100):
    for i in range(shape[0]):
        for j in range(shape[1]):
            if(i-1> 0 and j-1 > 0 and i+1< shape[0] and j+1 < shape[0]):
                if(world[i][j+1] == 0 and world[i][j-1] == 0 and world[i+1][j] == 0 and world[i-1][j] == 0):
                    world[i][j] = 0
                    #print("water")
                if(world[i][j+1] == 1 and world[i][j-1] == 1 and world[i+1][j] == 1 and world[i-1][j] == 1):
                    world[i][j] = 1
                    #print("land")
            else:
                world[i][j] = 0
            
plt.imshow([[world[y][x] for x in range(shape[0])] for y in range(shape[1])] ,cmap = 'Blues')        
#plt.imshow([[world[x][y] for y in range(shape[0])] for x in range(shape[1])], cmap='Blues', vmin=0, vmax=1)
plt.show() 
