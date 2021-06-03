import noise
import numpy as np
import matplotlib.pyplot as plt

shape = (1024,1024)
scale = 100.0
octaves = 2
persistence = 0.3
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=0)
        
im = plt.imshow([[world[x][y] for y in range(shape[0])] for x in range(shape[1])], cmap='gist_gray_r', vmin=0, vmax=1)
plt.show()



blue = [65,105,225]
green = [34,139,34]
beach = [238, 214, 175]

def add_color(world):
    color_world = np.zeros(world.shape+(3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = blue
            elif world[i][j] < 0:
                color_world[i][j] = beach
            elif world[i][j] < 1.0:
                color_world[i][j] = green

    return color_world

color_world = add_color(world)

im = plt.imshow([[color_world[x][y] for y in range(shape[0])] for x in range(shape[1])], cmap='gist_gray_r', vmin=0, vmax=1)
plt.show()