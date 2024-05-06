import random
import copy

''' Maze Generator '''
class Level(object):
    def __init__(self, rowMin, rowMax):
        self.rowMin = rowMin
        self.rowMax = rowMax
        self.rows = self.cols = random.randint(self.rowMin, self.rowMax)
        self.maze = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.baseRow = -1
        self.baseCol = -1
        self.enemyStartRow = -1
        self.enemyStartCol = -1

        self.mazeGen()


    def placeBase(self):
        baseRow = random.randint(0, self.rows - 1)
        if baseRow == 0:
            baseCol = random.randint(1, self.cols - 1)
        elif baseRow == self.rows - 1:
            baseCol = random.randint(0, self.cols - 2)
        else:
            baseCol = random.randint(0, self.cols - 1)
        dirs = [(1,0), (0,1), (0,-1), (-1,0)]
        counts = 0
        if self.maze[baseRow][baseCol] == None:
            for drow, dcol in dirs:
                if 0 <= baseRow+drow < self.rows and 0 <= baseCol+dcol < self.cols:
                    if self.maze[baseRow+drow][baseCol+dcol] == False:
                        counts += 1
            if counts == 1:
                self.maze[baseRow][baseCol] = "Base"
                self.baseCol = baseCol
                self.baseRow = baseRow
                return
        self.placeBase()

    # checks the exterior of the chamber to see if there are any connections
    def findBlocksToRemove(self, chamber, startRow, startCol):
        blockList = set()
        rows = len(chamber)
        cols = len(chamber[0])
        firstRow = 1 # check above it
        lastRow = -2 + rows # check below it
        firstCol = 1 # check to the left
        lastCol = -2 + cols # check to the right

        for row in range(firstRow, lastRow+1):
            for col in range(firstCol, lastCol+1):
                if chamber[row][col] == False:
                    newChamber = copy.deepcopy(chamber)
                    newChamber[row][col] = None
                    if self.checkNewChamber(newChamber, chamber):
                        blockList.add((row, col))
        return blockList

    def checkNewChamber(self, newChamber, chamber):
        oldCounts = 0
        newSeen = set()

        rows = len(chamber)
        cols = len(chamber[0])

        # gets oldCounts
        for row in range(rows):
            for col in range(cols):
                if chamber[row][col] == False:
                    oldCounts += 1
        
        firstRow, firstCol = self.getFalse(newChamber, -1, -1)
        self.search(firstRow, firstCol, newChamber, newSeen, oldCounts)
        if oldCounts - 1 == len(newSeen): return True
        else: return False


    def search(self, firstRow, firstCol, newChamber, newSeen, oldCounts):
        dirs = [(1,0), (0,1), (0,-1), (-1,0)]
        if 0 <= firstRow < len(newChamber) and 0 <= firstCol < len(newChamber[0]):
            if newChamber[firstRow][firstCol] == False and (firstRow, firstCol) not in newSeen:
                newSeen.add((firstRow, firstCol))
                for drow, dcol in dirs:
                    self.search(firstRow+drow, firstCol+dcol, newChamber, newSeen, oldCounts)
            
    def getFalse(self, newChamber, oldRow, oldCol):
        for row in range(len(newChamber)):
            for col in range(len(newChamber[0])):
                if newChamber[row][col] == False:
                    if oldRow == row and col > oldCol:
                        return row, col
                    elif row > oldRow:
                        return row, col
        return -1, -1                    

    def getMazeBorder(self):
        self.maze[0] = [None for _ in range(self.rows)]
        self.maze[self.rows - 1] = [None for _ in range(self.rows)]
        for line in self.maze:
            line[0] = None
            line[self.cols - 1] = None

    def placeEnemyStart(self, baseRow, baseCol):
        chooseToStart = random.random()
        if chooseToStart < 0.5:
            startRow = random.randint(0, self.rows - 1)
            startCol = random.choice([0, self.cols - 1])
        else:
            startCol = random.randint(0, self.cols - 1)
            startRow = random.choice([0, self.rows - 1])

        dirs = [(1,0), (0,1), (0,-1), (-1,0)]
        for drow, dcol in dirs:
            if 0 <= startRow+drow < self.rows and 0 <= startCol+dcol < self.cols:
                if self.maze[startRow+drow][startCol+dcol] == False and abs(startRow - self.baseRow) > self.rows//2 - 1 and abs(startCol - self.baseCol) > self.cols//2 - 1:
                    self.maze[startRow][startCol] = False
                    self.enemyStartRow = startRow
                    self.enemyStartCol = startCol
                    return
        self.placeEnemyStart(self.baseRow, self.baseCol)

    def mazeGen(self):
        self.getMazeBorder()
        self.mazeGenRecurse(0, 0, self.maze)
        self.placeBase() # for easy, have only one entrance the base can enter through
        # see if this stops crashes
        try: 
            self.placeEnemyStart(self.baseRow, self.baseCol)
        except:
            print("invalid maze")
            self.maze = [[False for _ in range(self.cols)] for _ in range(self.rows)]
            self.mazeGen()

    def getRowBlocksFromSet(self, row, blockSet):
        newList = []
        for block in blockSet:
            if block[0] == row:
                newList.append(block)
        return newList
    
    def getColBlocksFromSet(self, col, blockSet):
        newList = []
        for block in blockSet:
            if block[1] == col:
                newList.append(block)
        return newList

    # using the recursive division method
    # https://en.wikipedia.org/wiki/Maze_generation_algorithm
    def mazeGenRecurse(self, startRow, startCol, chamber):
        if len(chamber) == 3 or len(chamber[0]) == 3: 
            pass

        elif len(chamber) == 4 or len(chamber[0]) == 4:
            if len(chamber) == len(chamber[0]):
                blocksToRemove = list(self.findBlocksToRemove(chamber, startRow, startCol))
                if len(blocksToRemove) != 0:
                    blockRow, blockCol = random.choice(blocksToRemove)
                    self.maze[blockRow + startRow][blockCol + startCol] = None

            elif len(chamber) == 4:
                # remove a random column
                possibleCols = self.getPossibleCols(chamber)
                col = random.choice(possibleCols)
                blocksToRemove = self.findBlocksToRemove(chamber, startRow, startCol)
                blocksToRemove = self.getColBlocksFromSet(col, blocksToRemove)

                if len(blocksToRemove) != 0:
                    i = 1
                    j = random.choice(blocksToRemove)
                    for line in self.maze[startRow+1:]:
                        if (i, col) in blocksToRemove:
                            if i < len(chamber)-1:
                                line[startCol + col] = None
                        i += 1
                    if len(blocksToRemove) != 1:
                        self.maze[startRow + j[0]][startCol + j[1]] = False

                    # recursively call the two broken halves
                    c1 = [[self.maze[startRow + i][startCol + j] for j in range(col+1)] for i in range(len(chamber))]
                    c2 = [[self.maze[startRow + i][startCol + j + col] for j in range(len(chamber[0])-col)] for i in range(len(chamber))]
                    self.mazeGenRecurse(startRow, startCol, c1)
                    self.mazeGenRecurse(startRow, startCol + col, c2)

            elif len(chamber[0]) == 4:
                # remove a random row
                possibleRows = self.getPossibleRows(chamber)
                row = random.choice(possibleRows)
                blocksToRemove = self.findBlocksToRemove(chamber, startRow, startCol)
                blocksToRemove = self.getRowBlocksFromSet(row, blocksToRemove)
                if len(blocksToRemove) != 0: 
                    j = random.choice(blocksToRemove)
                    for i in range(1, len(chamber[0])-1):
                        if (row, i) in blocksToRemove:
                            self.maze[startRow + row][i+startCol] = None
                    if len(blocksToRemove) != 1:
                        self.maze[startRow + j[0]][startCol + j[1]] = False
                
                    # recursively call the two broken halves
                    c1 = [[self.maze[startRow + i][startCol + j] for j in range(len(chamber[0]))] for i in range(row + 1)]
                    c2 = [[self.maze[startRow + i + row][startCol + j] for j in range(len(chamber[0]))] for i in range(len(chamber) - row)]
                    self.mazeGenRecurse(startRow, startCol, c1)
                    self.mazeGenRecurse(startRow + row, startCol, c2)

        else:
            rowOrColDecider = random.random()

            possibleRows = self.getPossibleRows(chamber)
            possibleCols = self.getPossibleCols(chamber)

            if rowOrColDecider > 0.5:
                row = random.choice(possibleRows)
                col = random.choice(possibleCols)
            else: 
                col = random.choice(possibleCols)
                row = random.choice(possibleRows)            

            # turn the row into potential tower location
            for i in range(1,len(chamber[0])-1):
                self.maze[startRow + row][i + startCol] = None

            # turn the col into potential tower location
            i = 1
            for line in self.maze[startRow+1:]:
                if i < len(chamber)-1:
                    line[startCol + col] = None
                else: break
                i += 1


            cellsDeleted = 0
            left = [row + startRow, startCol]
            right = [row + startRow, startCol + len(chamber[0]) - 1]
            top = [startRow, col + startCol]
            bottom = [startRow + len(chamber) - 1, col + startCol]

            leftB = False
            rightB = False
            topB = False
            bottomB = False

            if self.maze[left[0]][left[1]] == False:
                # print('left', left)
                self.maze[left[0]][left[1] + 1] = False
                left = True
                cellsDeleted += 1
            if self.maze[right[0]][right[1]] == False:
                # print('right', right)
                self.maze[right[0]][right[1] - 1] = False
                right = True
                cellsDeleted += 1
            if self.maze[top[0]][top[1]] == False:
                # print('top', top)
                self.maze[top[0] + 1][top[1]] = False
                top = True
                cellsDeleted += 1
            if self.maze[bottom[0]][bottom[1]] == False:
                # print('bottom', bottom)
                self.maze[bottom[0] - 1][bottom[1]] = False
                bottom = True
                cellsDeleted += 1
            
            # choose three sides to remove a square from 
            possiblyDeletedCells = []
            if leftB == False:
                possiblyDeletedCells.append((row, random.randrange(1,col)))            
            if rightB == False:
                possiblyDeletedCells.append((row, random.randrange(col+1, len(chamber[0])-1)))
            if topB == False:
                possiblyDeletedCells.append((random.randrange(1,row), col))
            if bottomB == False:
                possiblyDeletedCells.append((random.randrange(row+1, len(chamber)-1), col))
            
            if cellsDeleted < 3: 
                for i in range(3 - cellsDeleted):
                    cellToDelete = random.choice(possiblyDeletedCells)
                    possiblyDeletedCells.remove(cellToDelete)
                    rowDelete, colDelete = cellToDelete
                    self.maze[rowDelete+startRow][colDelete+startCol] = False

            # now we need to split the chamber into four pieces and recursively call each piece
            chamber1, chamber2, chamber3, chamber4 = self.getNewChamber(chamber, row, col, startRow, startCol)
            
            self.mazeGenRecurse(startRow, startCol, chamber1)
            self.mazeGenRecurse(startRow + row, startCol, chamber2)
            self.mazeGenRecurse(startRow, startCol + col, chamber3)
            self.mazeGenRecurse(startRow + row, startCol + col, chamber4)

    def getPossibleRows(self, chamber):
        possibleRows = []
        for i in range(2, len(chamber) - 2):
            possibleRows.append(i)
        return possibleRows

    def getPossibleCols(self, chamber):
        possibleCols = []
        for i in range(2, len(chamber[0]) - 2):
            possibleCols.append(i)
        return possibleCols

    
    def getColList(self, chamber, col):
        colList = []
        for row in self.maze:
            colList.append(row[col])
        return colList
    
    
    def getNewChamber(self, chamber, row, col, startRow, startCol):
        c1 = [[self.maze[startRow + i][startCol + j] for j in range(col + 1)] for i in range(row + 1)]
        c2 = [[self.maze[startRow + i + row][startCol + j] for j in range(col + 1)] for i in range(len(chamber) - row)]
        c3 = [[self.maze[startRow + i][startCol + j + col] for j in range(len(chamber[0]) - col)] for i in range(row + 1)]
        c4 = [[self.maze[startRow + i + row][startCol + j + col] for j in range(len(chamber[0]) - col)] for i in range(len(chamber) - row)]

        return c1, c2, c3, c4  