import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import matplotlib.animation as animation
import time
from matplotlib.animation import FuncAnimation
import noise

class Cell:
    def __init__(self,position,population,infectedPopulation,infected,daysInfected):
        self.position = position
        self.population = population
        self.infectedPopulation = infectedPopulation
        self.infected = infected
        self.daysInfected = daysInfected


class CVirus:
    def __init__(self):
        #grid x and y size
        self.nx = 100
        self.ny = 100
        self.chance = 0
        self.infectedPopulation = 0#probably dont need
        self.totalInfected = 0
        self.todaysInfected = []
        self.InfectedCells = []
        self.maxPopulation = 0
        self.grid = np.array( [[Cell((x,y) , random.randint(0,500) , 0 , False , 0) for x in range(self.nx)] for y in range(self.ny)] )#randomize a self.grid for the population parameter
        self.grid[49,49].infected = True
        self.infectedGrid = np.zeros([self.nx, self.ny], dtype=bool)#i think they all start off true
        self.numInfected = 0
        self.spreadReduction = 0
        self.fig = plt.figure() #this figure is for the animation
        self.im = plt.imshow([[self.grid[x][y].infected for x in range(self.nx)] for y in range(self.ny)], cmap='gist_gray_r', vmin=0, vmax=1)
        #self.im2 = plt.imshow([[self.grid[x][y].population for y in range(self.ny)] for x in range(self.nx)], cmap='Blues')


        """map generation (Celular Automata)"""
        shape = (100,100)
        WALL = 0
        FLOOR = 1
        fill_prob = 0.4

        self.new_map = np.ones(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                choice = random.uniform(0, 1)
                self.new_map[i][j] = WALL if choice < fill_prob else FLOOR

        # run for 6 generations
        generations = 7
        for generation in range(generations):
            for i in range(shape[0]):
                for j in range(shape[1]):
                    # get the number of walls 1 away from each index
                    # get the number of walls 2 away from each index
                    submap = self.new_map[max(i-1, 0):min(i+2, self.new_map.shape[0]),max(j-1, 0):min(j+2, self.new_map.shape[1])]
                    wallcount_1away = len(np.where(submap.flatten() == WALL)[0])
                    submap = self.new_map[max(i-2, 0):min(i+3, self.new_map.shape[0]),max(j-2, 0):min(j+3, self.new_map.shape[1])]
                    wallcount_2away = len(np.where(submap.flatten() == WALL)[0])
                    # this consolidates walls
                    # for first five generations build a scaffolding of walls
                    if generation < 5:
                        # if looking 1 away in all directions you see 5 or more walls
                        # consolidate this point into a wall, if that doesnt happpen
                        # and if looking 2 away in all directions you see less than
                        # 7 walls, add a wall, this consolidates and adds walls
                        if wallcount_1away >= 5 or wallcount_2away <= 7:
                            self.new_map[i][j] = WALL
                        else:
                            self.new_map[i][j] = FLOOR
                    # this consolidates open space, fills in standalone walls,
                    # after generation 5 consolidate walls and increase walking space
                    # if there are more than 5 walls nearby make that point a wall,
                    # otherwise add a floor
                    else:
                        # if looking 1 away in all direction you see 5 walls
                        # consolidate this point into a wall,
                        if wallcount_1away >= 5:
                            self.new_map[i][j] = WALL
                        else:
                            self.new_map[i][j] = FLOOR
        if wallcount_1away >= 5 or wallcount_2away <= 7:
            self.new_map[i][j] = WALL
        else:
            self.new_map[i][j] = FLOOR
        if i==0 or j == 0 or i == shape[0]-1 or j == shape[1]-1:
            self.new_map[i][j] = WALL 
        """"""


        """ perlin noise"""
        
        self.shape = (self.nx,self.ny)
        self.scale = 100.0
        self.octaves = 6
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.world = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.grid[i][j].population = noise.pnoise2(i/self.scale, 
                                            j/self.scale, 
                                            octaves=self.octaves, 
                                            persistence=self.persistence, 
                                            lacunarity=self.lacunarity, 
                                            repeatx=self.nx, 
                                            repeaty=self.ny, 
                                            base=0)
       
        lowestValue = 0
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.grid[i][j].population = self.grid[i][j].population * 1000
                if( self.grid[i][j].population < lowestValue):
                    lowestValue = self.grid[i][j].population
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.grid[i][j].population += lowestValue*(-1) #shift all cell values by lowest value so none are negative

            self.numzeroed = 0                                    
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if(self.new_map[i][j] == False):#if the generated map is uninhabitable set the population to 0
                    self.grid[i][j].population = 0
                    self.numzeroed +=1
                    #print('number of uninhabited tiles',self.numzeroed)
        """"""

    def init(self):
        self.im.set_data(np.zeros((self.nx, self.ny)))
    
    def anim(self,day):
        self.InfectedCells = []#reset infected cells
        self.numInfected = 0 #reset nuInfected
        
        spreadRate = 1.5

        for i,j in np.ndindex(self.grid.shape):
            if(self.grid[i,j].population > self.maxPopulation and day == 0):
                self.maxPopulation= self.grid[i][j].population
            if(self.grid[j,i].infected == True):
                self.grid[i,j].daysInfected +=1
                self.grid[i][j].infectedPopulation = int(spreadRate**self.grid[i][j].daysInfected)#spreadrate to the power of the days infected
                if(self.grid[i][j].infectedPopulation > self.grid[i][j].population):
                    self.grid[i][j].infectedPopulation = self.grid[i][j].population
                self.numInfected += self.grid[i,j].infectedPopulation#if infected population is larger than the actual population, set it to the population of the cell
                self.InfectedCells.append(self.grid[i,j])
                #self.todaysInfected += self.grid[i][j].population#this was added from old code but might change
                
        self.todaysInfected.append(self.numInfected)

        self.spreadReduction = 0.4
        self.count =0
        for cell in self.InfectedCells:#loop through infected cells in the current day

            currentInfectedPos = cell.position#returns a touple
            x,y = currentInfectedPos#breaking up a touple(x,y) to int values
            if(x+1 < len(self.grid)):#check if at right bound
                chance = (self.InfectedCells[self.count].population + self.grid[x+1][y].population)/(2*self.maxPopulation)  #this is average of 2 populations normalized to max pop
            randomNumber = random.random()#coinflip
            if (chance > randomNumber and x+1 < len(self.grid)):
                self.grid[x+1][y].infected=True#spread Right
            if (x-1 >= 0):#check if at left bound
                chance = (self.InfectedCells[self.count].population + self.grid[x-1][y].population)/(2*self.maxPopulation)  #this is average of 2 populations normalized to max pop
            randomNumber = random.random()#coinflip
            if (chance > randomNumber and x-1 >= 0):
                self.grid[x-1][y].infected=True#spread Left
            if (y+1 < len(self.grid)):#check if at top bound
                chance = (self.InfectedCells[self.count].population + self.grid[x][y+1].population)/(2*self.maxPopulation)  #this is average of 2 populations normalized to max pop
            randomNumber = random.random()#coinflip
            if (chance > randomNumber and y+1 < len(self.grid)):
                self.grid[x][y+1].infected=True#spread Up
            if (y-1 >= len(self.grid)):#check if at bottom bound
                chance = (self.InfectedCells[self.count].population + self.grid[x][y-1].population)/(2*self.maxPopulation)  #this is average of 2 populations normalized to max pop
            randomNumber = random.random()#coinflip
            if (chance > randomNumber and y-1 >= 0):
                self.grid[x][y-1].infected=True#spread Down
            self.count+=1
        for i,j in np.ndindex(self.grid.shape):
            if(self.grid[i,j].population == 0):
                self.grid[i,j].infected = False
            
        self.im.set_data([[self.grid[x][y].infected for x in range(self.nx)] for y in range(self.ny)])
        return self.im



CV = CVirus()

#fig = plt.figure()
#ax1 = fig.add_subplot(221)
#ax2 = fig.add_subplot(222)


#im1 = plt.imshow([[CV.new_map[y][x] for x in range(CV.nx)] for y in range(CV.ny)] ,cmap = 'Blues')
#im1 = plt.imshow([[CV.grid[y][x].inhabitable for x in range(CV.nx)] for y in range(CV.ny)] ,cmap = 'Blues')#plot population
plt.imshow([[CV.grid[y][x].population for x in range(CV.nx)] for y in range(CV.ny)] ,cmap = 'Blues')#plot population
#plt.plot()


#im2 = plt.imshow([[CV.grid[y][x].infected for x in range(CV.nx)] for y in range(CV.ny)] ,cmap = 'Blues')#plot population
#plt.plot()
#anim = animation.FuncAnimation(CV.fig, CV.anim, init_func=CV.init, frames=CV.nx * CV.ny, interval=250)
plt.show()