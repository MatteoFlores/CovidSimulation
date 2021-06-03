import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

shape = (1000,1000)
world = np.zeros(shape)
average = 0
leftVal = 0
botVal = 0
maxDivergence = 10
divergence = 0
world[0][0] = random.randint(0,10)
for i in range(shape[0]):
    for j in range(shape[1]):
        if(j > 0):
            botVal = world[i][j-1]
        if(i > 0):
            leftVal = world[i-1][j]
        if(i-1 <= 0 ):#these 2 conditional statements make it so that if the is no left value or right value then the average will be the only existing neighbor
            leftVal = botVal
        if(i-1 <= 0 ):
            botVal = leftVal
        average = int(leftVal/2 + botVal/2)
        divergence =  random.randint(0-maxDivergence, maxDivergence)#still need to prohibit exceeding limits and negative numbers
        if(i + j != 0):#if not the first index
            if(average + divergence >= 0 or average + divergence < 10):#if generated value is still in range
                world[i][j] = average + divergence
            else:
                divergence = divergence*(-1)
plt.imshow([[world[y][x] for x in range(shape[0])] for y in range(shape[1])] ,cmap = 'Blues')        
#plt.imshow([[world[x][y] for y in range(shape[0])] for x in range(shape[1])], cmap='Blues', vmin=0, vmax=1)
plt.show() 


            
