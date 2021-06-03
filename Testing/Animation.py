import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import matplotlib.animation as animation
import pandas as pd
import time
from matplotlib.animation import FuncAnimation

nx = 10
ny = 10

fig = plt.figure()
grid = np.zeros((nx, ny))
grid[4][4] = 1
im = plt.imshow(grid, cmap='gist_gray_r', vmin=0, vmax=1)

def init():
    im.set_data(np.zeros((nx, ny)))

def animate(i):
    for i,j in np.ndindex(grid.shape):
        vertMove = random.randint(-1,1)
        horizMove = random.randint(-1,1)
        """ EDGE CASES"""
        if(i < 1 and horizMove == -1):
            horizMove = random.randint(0,1)
        if(i > 8 and horizMove == 1):
            horizMove = random.randint(-1,0)
        if(j < 1 and vertMove == -1):
            vertMove = random.randint(0,1)
        if(j > 8 and vertMove == 1):
            vertMove = random.randint(-1,0)
        """"""
        if(grid[i, j] == 1):
            grid[i][j] = 0
            grid[i + horizMove][j + vertMove] = 1
        
        
    im.set_data(grid)
    return im

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny,
                               interval=100)
plt.show()