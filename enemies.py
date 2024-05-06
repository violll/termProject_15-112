import random 
from PIL import ImageTk, Image


class BasicAnt(object):
    health = 20
    def __init__(self, cx, cy, cellW, healths=20):
        self.front = []
        self.back = []
        self.cx = cx
        self.cy = cy
        self.health = healths
        self.speed = 2
        self.dx = 0
        self.dy = 1
        self.backDx = self.dx
        self.backDy = self.dy
        self.coinWorth = 5
        self.visitedSquares = set()
        self.width = cellW // 9
        self.height = cellW // 4
        self.image = Image.open("ant.png")
        self.path = []
        self.row = -1
        self.col = -1
        self.cellW = cellW
        self.randomTurnPoint = random.randint(int(cellW * 1 / 4), int(cellW * 3 / 4))
    

    def getCenterCell(self, row, col, margin):
        x = margin + col * self.cellW + self.cellW // 2
        y = margin + row * self.cellW + self.cellW // 2
        return x, y
    
    def getRowCol(self, x, y, margin):
        row = (y - margin) // self.cellW
        col = (x - margin) // self.cellW
        return int(row), int(col)


    def move(self, margin):
        x, y = self.getCenterCell(self.row, self.col, margin)
        i = self.path.index((int(self.row), int(self.col)))

        # the ant starts turning in its front half
        if ((self.dx != 0 and self.randomTurnPoint - 6 <= abs(x + self.cellW//2 - self.front[0]) <= 6 + self.randomTurnPoint) or 
            (self.dy != 0 and self.randomTurnPoint - 6 <= abs(y + self.cellW//2 - self.front[1]) <= 6 + self.randomTurnPoint)):
            self.dx = self.path[i+1][1] - self.path[i][1]
            self.dy = self.path[i+1][0] - self.path[i][0]

        if ((self.backDx != 0 and self.randomTurnPoint - 6 <= abs(x + self.cellW//2 - self.back[0]) <= 6 + self.randomTurnPoint) or 
            (self.backDy != 0 and self.randomTurnPoint - 6 <= abs(y + self.cellW//2 - self.back[1]) <= 6 + self.randomTurnPoint)):
            self.backDx = self.dx
            self.backDy = self.dy

        # adjust the front coordinate
        self.front[0] += self.dx * self.speed
        self.front[1] += self.dy * self.speed

        # adjust the back relative to the front
        self.back[0] += self.backDx * self.speed
        self.back[1] += self.backDy * self.speed

        # cx and cy will be the average of of the two endpoints
        self.cx = (self.front[0] + self.back[0]) // 2
        self.cy = (self.front[1] + self.back[1]) // 2

        self.row, self.col = self.getRowCol(self.cx, self.cy, margin)

class StupidAnt(BasicAnt):
    health = 15
    def __init__(self, cx, cy, cellW, healths=15):
        super().__init__(cx, cy, cellW)
        self.front = []
        self.back = []
        self.health = healths
        self.speed = 5
        self.dx = 0
        self.dy = 1
        self.backDx = self.dx
        self.backDy = self.dy
        self.coinWorth = 10
        self.width = cellW // 9
        self.height = cellW // 4
        self.image = Image.open("stupidAnt.png")
        self.path = []
        self.row = -1
        self.col = -1
        self.cellW = cellW
        self.randomTurnPoint = random.randint(int(cellW * 1 / 4), int(cellW * 3 / 4))