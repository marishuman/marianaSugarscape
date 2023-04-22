#! /usr/bin/python

import agent
import cell
import environment
import gui

import math
import random
import time

class Sugarscape:
    def __init__(self, environmentOptions, agentOptions):
        self.__environment = environment.Environment(environmentOptions["height"], environmentOptions["width"], environmentOptions["maxSugar"], environmentOptions["sugarRegrowRate"])
        self.__EnvironmentHeight = environmentOptions["height"]
        self.__EnvironmentWidth = environmentOptions["width"]
        self.configureEnvironment(environmentOptions["maxSugar"])
        self.__agents = []
        self.configureAgents(agentOptions["initialAgents"], agentOptions["vision"], agentOptions["metabolism"], agentOptions["endowment"])
        self.__gui = gui.GUI(self)
        self.__run = False # Simulation start flag
        self.__end = False # Simulation end flag
        self.__timestep = 0

    def addSugarPeak(self, startX, startY, radius, maxCapacity):
        height = self.__environment.getHeight()
        width = self.__environment.getWidth()
        radialDispersion = math.sqrt(max(startX, width - startX)**2 + max(startY, height - startY)**2) * (radius / width)
        for i in range(height):
            for j in range(width):
                if self.__environment.getCell(i, j) == None:
                    self.__environment.setCell(cell.Cell(i, j, self.__environment), i, j)
                currDispersion = 1 + maxCapacity * (1 - math.sqrt((startX - i)**2 +  (startY - j)**2) / radialDispersion)
                cellMaxCapacity = min(currDispersion, maxCapacity)
                cellMaxCapacity = math.ceil(cellMaxCapacity)
                if cellMaxCapacity > self.__environment.getCell(i, j).getMaxSugar():
                    self.__environment.getCell(i, j).setMaxSugar(cellMaxCapacity)
                    self.__environment.getCell(i, j).setCurrSugar(cellMaxCapacity)

    def configureAgents(self, initialAgents, agentVision, agentMetabolism, agentEndowment):
        if self.__environment == None:
            return
        for i in range(initialAgents):
            randX = random.randrange(self.__environment.getHeight())
            randY = random.randrange(self.__environment.getWidth())
            while self.__environment.getCell(randX, randY).getAgent() != None:
                randX = random.randrange(self.__environment.getHeight())
                randY = random.randrange(self.__environment.getWidth())
            c = self.__environment.getCell(randX, randY)
            a = agent.Agent(c, agentMetabolism, agentVision, agentEndowment)
            c.setAgent(a)
            self.__agents.append(a)

    def configureEnvironment(self, maxCapacity):
        height = self.__environment.getHeight()
        width = self.__environment.getWidth()
        startX1 = math.ceil(height * 0.7)
        startX2 = math.ceil(height * 0.3)
        startY1 = math.ceil(width * 0.3)
        startY2 = math.ceil(width * 0.7)
        radius = math.ceil(math.sqrt(1.25 * (height + width)))
        self.addSugarPeak(startX1, startY1, radius, maxCapacity)
        self.addSugarPeak(startX2, startY2, radius, maxCapacity)

    def doTimestep(self):
        if self.__end == True:
            self.endSimulation()
        self.__environment.doTimestep()
        for a in self.__agents:
            if a.isAlive() == False:
                self.__agents.remove(a)
        self.__gui.doTimestep()
        print("Timestep: {0}".format(self.__timestep))
        self.__timestep += 1

    def endSimulation(self):
        exit(0)

    def getAgents(self):
        return self.__agents

    def getEnd(self):
        return self.__end

    def getEnvironment(self):
        return self.__environment
 
    def getEnvironmentHeight(self):
        return self.__EnvironmentHeight

    def getEnvironmentWidth(self):
        return self.__EnvironmentWidth

    def getGUI(self):
        return self.__gui

    def getRun(self):
        return self.__run
  
    def getTimestep(self):
        return self.__timestep

    def pauseSimulation(self):
        while self.__run == False:
            if self.__end == True:
                self.endSimulation()
            self.__gui.getWindow().update()

    def runSimulation(self, timesteps=5):
        self.pauseSimulation() # Simulation begins paused until start button in GUI pressed
        t = 0
        timesteps = timesteps - self.__timestep
        while t < timesteps and self.__end == False and len(self.__agents) != 0:
            self.doTimestep()
            t += 1
            if self.__run == False:
                self.pauseSimulation()

    def setAgents(self, agents):
        self.__agents = agents

    def setEnd(self):
        self.__end = not self.__end

    def setEnvironment(self, environment):
        self.__environment = environment

    def setEnvironmentHeight(self, EnvironmentHeight):
        self.__EnvironmentHeight = EnvironmentHeight

    def setEnvironmentWidth(self, EnvironmentWidth):
        self.__EnvironmentWidth = EnvironmentWidth

    def setGUI(self, gui):
        self.__gui = gui

    def setTimestep(self, timestep):
        self.__timestep = timestep
  
    def setRun(self):
        self.__run = not self.__run
  
    def __str__(self):
        string = "{0}Timestep: {1}\nLiving Agents: {2}".format(str(self.__environment), self.__timestep, len(self.__agents))
        return string

if __name__ == "__main__":
    agentOptions = {"vision": 10, "metabolism": 1, "endowment": 3, "initialAgents": 500}
    environmentOptions = {"height": 50, "width": 50, "maxSugar": 4, "sugarRegrowRate": 1}
    S = Sugarscape(environmentOptions, agentOptions)
    print(str(S))
    S.runSimulation(10000)
    print(str(S))
    exit(0)