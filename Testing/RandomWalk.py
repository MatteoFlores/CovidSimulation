import random
from itertools import count
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statistics

class RandWalk:
    def __init__(self):
        self.flip = 0
        self.heads = 0
        self.tails = 0
        self.net=0
        self.x, self.y , self.y2= [0,0] , [0,0] , [0,0]
        self.index = count()
    def animate(self, i):
        self.x.append(next(self.index))
        flip = random.randint(0, 1)
        if (flip == 0):
            self.heads +=1
            self.net += 1
        else:
            self.tails += 1
            self.net -= 1
        self.y.append(self.net)
        self.y2.append(statistics.stdev(self.y))
        plt.cla()
        plt.plot(self.x , self.y , label='chanel 1')
        plt.plot(self.x , self.y2 , label='chanel 2')
        plt.legend(loc='upper left')
        plt.tight_layout()
        
RW = RandWalk()
ani = FuncAnimation(plt.gcf(), RW.animate , interval=5) 
plt.show()