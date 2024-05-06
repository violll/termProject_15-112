import random
from enemies import *


# this will generate the random list of enemies that appear on the screen
class EasyEnemyList(object): 
    def __init__(self, numWaves, startRow, startCol, margin, rowH, colW):
        self.numWaves = numWaves
        self.enemyList = [[None] for i in range(self.numWaves)]
        self.minEnemies = 5
        self.maxEnemies = 8
        self.startRow = startRow
        self.startCol = startCol
        self.margin = margin
        self.rowH = rowH
        self.colW = colW
    
    def getCenterCell(self, row, col):
        x = self.margin + col * self.colW + self.colW // 2
        y = self.margin + row * self.rowH + self.rowH // 2
        return x, y

    def generateOneWave(self, healthToAdd):
        res = []
        numEnemies = random.randint(self.minEnemies, self.maxEnemies)
        for i in range(numEnemies):
            antType = random.choice([BasicAnt, StupidAnt])
            antX, antY = self.getCenterCell(self.startRow, self.startCol)
            newHealth = antType.health + healthToAdd
            newAnt = antType(antX, antY, self.colW, newHealth)
            timeEntered = random.random() + random.randint(0, 20)
            res.append((newAnt, timeEntered))
        return res
    
    def generateAllWaves(self):
        for i in range(self.numWaves):
            self.minEnemies += 1
            self.maxEnemies += 1
            self.enemyList[i] = self.generateOneWave(i * 2)


class MediumEnemyList(EasyEnemyList): 
    def __init__(self, numWaves, startRow, startCol, margin, rowH, colW):
        super().__init__(numWaves, startRow, startCol, margin, rowH, colW)
        self.enemyList = [[None] for i in range(self.numWaves)]
        self.minEnemies = 9
        self.maxEnemies = 12

    def generateOneWave(self, healthToAdd):
        res = []
        numEnemies = random.randint(self.minEnemies, self.maxEnemies)
        for i in range(numEnemies):
            antType = random.choice([BasicAnt, StupidAnt])
            antX, antY = self.getCenterCell(self.startRow, self.startCol)
            newHealth = antType.health + healthToAdd
            newAnt = antType(antX, antY, self.colW, newHealth)
            timeEntered = random.random() + random.randint(0, 20)
            res.append((newAnt, timeEntered))
        return res
    
    def generateAllWaves(self):
        for i in range(self.numWaves):
            self.minEnemies += 1
            self.maxEnemies += 2
            self.enemyList[i] = self.generateOneWave(i * 4)


class HardEnemyList(EasyEnemyList): 
    def __init__(self, numWaves, startRow, startCol, margin, rowH, colW):
        super().__init__(numWaves, startRow, startCol, margin, rowH, colW)
        self.enemyList = [[None] for i in range(self.numWaves)]
        self.minEnemies = 13
        self.maxEnemies = 15
    
    def generateOneWave(self, healthToAdd):
        res = []
        numEnemies = random.randint(self.minEnemies, self.maxEnemies)
        for i in range(numEnemies):
            antType = random.choice([BasicAnt, StupidAnt])
            antX, antY = self.getCenterCell(self.startRow, self.startCol)
            newHealth = antType.health + healthToAdd
            newAnt = antType(antX, antY, self.colW, newHealth)
            timeEntered = random.random() + random.randint(0, 25)
            res.append((newAnt, timeEntered))
        return res
    
    def generateAllWaves(self):
        for i in range(self.numWaves):
            self.minEnemies += 2
            self.maxEnemies += 2
            self.enemyList[i] = self.generateOneWave(i * 6)