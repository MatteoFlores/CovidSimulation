import random
import pylab
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import matplotlib.animation as animation
import time
from matplotlib.animation import FuncAnimation
import noise
import matplotlib
from mpl_toolkits.axes_grid1 import host_subplot


class Cell:
    def __init__(self,position,population,infectedPopulation,infected,daysInfected,previouslyInfected):
        self.position = position
        self.population = population
        self.infectedPopulation = infectedPopulation
        self.infected = infected
        self.daysInfected = daysInfected
        self.previouslyInfected = previouslyInfected


class CVirus:
    def __init__(self):

        self.keepRunning = True
        self.MCarloIteration = 0
        self.sumHistogram = []
        self.MCItterations = 0

        #grid x and y size
        self.nx = 100
        self.ny = 100
        self.chance = 0
        self.infectedPopulation = 0#probably dont need
        self.totalInfected = 0
        self.todaysInfected = []
        self.InfectedCells = []
        self.maxPopulation = 0
        self.grid = np.array( [[Cell((x,y) , random.randint(0,500) , 0 , False , 0 , False) for x in range(self.nx)] for y in range(self.ny)] )#randomize a self.grid for the population parameter
        self.randX = random.randint(0,99)
        self.randY = random.randint(0,99)
        self.grid[self.randX,self.randY].infected = True
        self.infectedGrid = np.zeros([self.nx, self.ny], dtype=bool)#i think they all start off true
        self.numInfected = 0
        self.spreadReduction = 0
        self.maxNumInfected = 0
        self.x_values = [] #for the days
        self.fig, ((self.ax01, self.ax02), (self.ax03, self.ax04)) = plt.subplots(2,2) #this figure is for the animation
        self.fig.suptitle("Spread of Coronavirus", fontsize=12)
        self.ax01.set_title('Total Currently Infected')
        self.ax02.set_title('Infection Spread')
        self.ax03.set_title('Population Density')
        self.ax04.set_title('Average Infection')


        self.resetCount = 0
        self.reset = False

        # set y-limits
        self.ax01.set_ylim(0,100)
        self.ax02.set_ylim(0,100)
        self.ax03.set_ylim(0,100)
        self.ax04.set_ylim(0,150000)

        # sex x-limits
        self.ax01.set_xlim(0,100.0)
        self.ax02.set_xlim(0,100)
        self.ax03.set_xlim(0,100)
        self.ax04.set_xlim(0,200)

        # Turn on grids
        self.ax01.grid(True)

        # Data Update
        self.xmin = 0.0
        self.xmax = 5.0
        self.x = 0.0

        self.ymax = 0
        self.y = 0

        self.ax01.set_xlabel("day")
        self.ax01.set_ylabel("# infacted")
        self.yp1=np.zeros(0)
        self.yv1=np.zeros(0)
        self.yp2=np.zeros(0)
        self.yv2=np.zeros(0)
        self.t=np.zeros(0)
        self.p011, = self.ax01.plot(self.x_values,self.yp1,'b-', label="yp1")
        self.p022 = self.ax02.imshow([[self.grid[x][y].infected for x in range(self.nx)] for y in range(self.ny)], cmap='gist_gray_r', vmin=0, vmax=1)
        self.p3 = self.ax03.imshow([[self.grid[x][y].population for x in range(self.nx)] for y in range(self.ny)] ,cmap = 'Blues')#plot population
        self.p4, = self.ax04.plot(self.x_values,self.sumHistogram,'b-', label="yp1")

        

        self.testValue = 0


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
        """-------------------------"""


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
       
        lowestValue = 0 #eliminates values lower than this
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
        """------------------------------------------"""

    def init(self):
        self.p3.set_data(np.zeros((self.nx, self.ny)))

    
    
    """ update frames """
    def anim(self,day):
        if(self.reset == False):
            self.InfectedCells = []#reset infected cells
        if(self.reset == True):
            self.reset = False
        self.numInfected = 0 #reset nuInfected
        spreadRate = 7.5
        if(day == 0):
            for i,j in np.ndindex(self.grid.shape):#normalization value
                if(self.grid[i,j].population > self.maxPopulation):
                    self.maxPopulation = self.grid[i][j].population
        for i,j in np.ndindex(self.grid.shape):
            if(self.grid[j,i].infected == True and self.grid[i][j].daysInfected < 26):#increase spread if less than x days infected
                self.grid[i,j].daysInfected +=1
                self.grid[i][j].infectedPopulation += int(spreadRate*self.grid[i][j].daysInfected)#spreadrate to the power of the days infected
                if(self.grid[i][j].infectedPopulation > self.grid[i][j].population):
                    self.grid[i][j].infectedPopulation = self.grid[i][j].population
                self.numInfected += self.grid[i,j].infectedPopulation#if infected population is larger than the actual population, set it to the population of the cell
                self.InfectedCells.append(self.grid[i,j])
                """uninfects after a number of days"""
            if(self.grid[i][j].daysInfected > 25 and self.grid[i][j].previouslyInfected == False):
                self.grid[i][j].infectedPopulation -= int((self.grid[i][j].population / self.maxPopulation) * spreadRate**(self.grid[i][j].daysInfected - 25))#subtract 25 from days infected to reset to 1
                if(self.grid[i][j].infectedPopulation <= 0):
                    self.grid[i][j].infectedPopulation = 0
                    self.grid[i][j].infected = False
                    self.grid[i][j].previouslyInfected = True
                
                

        
        self.yp1=np.append(self.yp1,self.numInfected)
        self.todaysInfected.append(self.numInfected)#seems to be the same as above line
        self.x_values.append(day)#days
        print(self.numInfected)

        self.testValue = int((self.grid[i][j].population / self.maxPopulation) * spreadRate*self.grid[i][j].daysInfected)

        self.spreadReduction = 0.4
        self.count =0

        
        """RESET ALL"""
        if(self.numInfected == 0):
            self.resetCount += 1

        i = 0   
        if(self.resetCount == 10):#RESET THE INFECTED POPULATION
            self.resetCount = 0 #reset
            print('HELLO')
            if(len(self.yp1) > 10):
                self.sumHistogram = [0] * len(self.x_values)
                for y in self.yp1:
                    self.sumHistogram[i] += self.yp1[i]
                    i+=1
                self.MCItterations += 1
                if(self.MCItterations > 1):
                    i = 0
                    for y in self.sumHistogram:
                        self.sumHistogram[i] = self.sumHistogram[i]/2 #average over 100 trials
                        i+=1
                    self.p4.set_data(list(range(0, len(self.sumHistogram))), self.sumHistogram)
                    print('YOYOYOYO')

                    


            for i,j in np.ndindex(self.grid.shape):
                self.grid[i][j].infected = False
                self.grid[i][j].infectedPopulation = 0
                self.grid[i][j].daysInfected = 0
            self.randX = random.randint(0,99)
            self.randY = random.randint(0,99)
            self.grid[self.randX][self.randY].Infected = True
            self.grid[self.randX][self.randY].infectedPopulation = 1
            self.InfectedCells.append(self.grid[self.randX,self.randY]) #THIS IS GETTING RESET
            self.p3.set_data([[self.grid[x][y].population for x in range(self.nx)] for y in range(self.ny)])

            self.yp1=np.zeros(0)
            self.x_values = []
            self.p011.set_data(self.x_values, self.yp1)

            self.reset = True
            
                


        chance = 0
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


        self.x +=1
        self.y = self.numInfected
        #update window of num infected plot
        if(self.numInfected > self.maxNumInfected):
            self.maxNumInfected = self.numInfected
            if(self.x >= self.xmax-1.00):
                self.p011.axes.set_ylim(0 ,self.maxNumInfected + int(self.numInfected/10))
        if(self.x >= self.xmax-1.00):
            self.p011.axes.set_xlim(0,self.x+ 20)


        self.p3.set_data([[self.grid[x][y].population for x in range(self.nx)] for y in range(self.ny)])
        self.p011.set_data(self.x_values, self.yp1)
        self.p022.set_data([[self.grid[x][y].infected for x in range(self.nx)] for y in range(self.ny)])            
        #self.im2 = plt.plot(self.x_values , self.ax03)
        #self.im.set_data([[self.grid[x][y].infected for x in range(self.nx)] for y in range(self.ny)])
        return self.p011 , self.p022 , self.p3 , self.p4
"""-----------------------------------------"""



CV = CVirus()
if(CV.keepRunning):
    anim = animation.FuncAnimation(CV.fig, CV.anim, init_func=CV.init, frames=CV.nx * CV.ny, interval=100)
    plt.show()