import random
import tkinter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import matplotlib.animation as animation
import pandas as pd
import time
from matplotlib.animation import FuncAnimation


class Cell:
    def __init__(self,position,population,infectedPopulation,infected,daysInfected):
        self.position = position
        self.population=population
        self.infectedPopulation=infectedPopulation
        self.infected=infected
        self.daysInfected=daysInfected
        
grid = [[Cell((x,y) , random.randint(0,5) , 0 , False , 0) for x in range(100)] for y in range(100)]#randomize a grid for the population parameter
grid[5][5].infected =  True#starting infected cell


#fig = plt.figure(figsize=(7, 7))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)
#ax.set_xlim(0, 1), ax.set_xticks([])
#ax.set_ylim(0, 1), ax.set_yticks([])


totalInfected = 0
days = 5
maxPopulation=0
chance =0
infectedPopulation = 0
todaysInfected = 0
todaysInfectedList = []


for x in range(days):#days to loop
    #infectedPopulation = 0
    #todaysInfected =0
    InfectedCells = []#store infeccted cells
    for i in range(len(grid)):#cycle throug the grid
        for j in range(len(grid[i])):
            if(grid[i][j].population > maxPopulation and x == 0):
                maxPopulation=grid[i][j].population
            if(grid[i][j].infected==True):
                grid[i][j].daysInfected+=1#increases the number of days infected for the current infected cell
                InfectedCells.append(grid[i][j])#add infected cells to an array
                todaysInfected += grid[i][j].population
    print(todaysInfected)
    spreadReduction = 0.4
    count =0
    for cell in InfectedCells:#loop through infected cells in the current day

        todaysInfected += InfectedCells[count].infectedPopulation
        
        currentInfectedPos = cell.position#returns a touple
        x,y = currentInfectedPos#breaking up a touple(x,y) to int values
        if(x+1 < len(grid)):#check if at right bound
            chance = (InfectedCells[count].population + grid[y][x+1].population)/(2*maxPopulation)  #this is average of 2 populations normalized to max pop
        randomNumber = random.random()#coinflip
        if (chance > randomNumber and x+1 < len(grid)):
            grid[y][x+1].infected=True#spread Right
        if (x-1 >= 0):#check if at left bound
            chance = (InfectedCells[count].population + grid[y][x-1].population)/(2*maxPopulation)  #this is average of 2 populations normalized to max pop
        randomNumber = random.random()#coinflip
        if (chance > randomNumber and x-1 >= 0):
            grid[y][x-1].infected=True#spread Left
        if (y+1 < len(grid)):#check if at top bound
            chance = (InfectedCells[count].population + grid[y+1][x].population)/(2*maxPopulation)  #this is average of 2 populations normalized to max pop
        randomNumber = random.random()#coinflip
        if (chance > randomNumber and y+1 < len(grid)):
            grid[y+1][x].infected=True#spread Up
        if (y-1 >= len(grid)):#check if at bottom bound
            chance = (InfectedCells[count].population + grid[y-1][x].population)/(2*maxPopulation)  #this is average of 2 populations normalized to max pop
        randomNumber = random.random()#coinflip
        if (chance > randomNumber and y-1 >= 0):
            grid[y-1][x].infected=True#spread Down
        notOutofBounds = False
        count+=1

    plt.imshow([[grid[y][x].infected for x in range(10)] for y in range(10)] ,cmap = 'Blues')#plot population
    
    plt.draw()
    plt.show()

#def update(frame_number):




#THIS IS THE CODE THAT SPREADS AND SHOWS INFECTED SHOULD ONLY BE RUN AT LOW AMOUNT OF DAYS
    #plt.imshow([[grid[y][x].infected for x in range(10)] for y in range(10)] ,cmap = 'Blues')#plot population
    #plt.plot()
    #time.sleep(1.5)
    #plt.show()

#animation = FuncAnimation(fig, update, interval=10)
#plt.show()

for i in range(len(grid)):#cycle throug the grid
  for j in range(len(grid[i])):
    if(grid[i][j].daysInfected > 30):
      grid[i][j].infected = False


totalPopulation = 0 
for i in range(len(grid)):#cycle throug the grid
        for j in range(len(grid[i])):
            print(grid[i][j].position,grid[i][j].population,grid[i][j].infected)
            if(grid[i][j].infected == True):
                totalInfected += grid[i][j].population
                totalPopulation += grid[i][j].population

#plt.imshow([[grid[y][x].population for x in range(100)] for y in range(100)] ,cmap = 'Blues')#plot population
#plt.plot()
#plt.show()

