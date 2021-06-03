import noise
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

x,y = 100, 100
shape = (x,y)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=x, 
                                    repeaty=y, 
                                    base=0)


for i in range(shape[0]):
    for j in range(shape[1]):
        if(world[i][j] == 0):
            world[i][j] = 0
plt.imshow([[world[y][x] for x in range(shape[0])] for y in range(shape[1])] ,cmap = 'Blues')        
#plt.imshow([[world[x][y] for y in range(shape[0])] for x in range(shape[1])], cmap='Blues', vmin=0, vmax=1)
plt.show() 