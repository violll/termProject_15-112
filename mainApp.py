from cmu_112_graphics import *
from copiedCode import *
from towers import *
from enemies import *
from projectiles import *
from mazeGenerator import *
from PIL import ImageTk, Image
import random
import string
import math
import copy
from enemyListGenerator import *

class Button(object):
    buttons = []

    def __init__(self, yScale, message, xScale=1/2):
        self.xScale = xScale
        self.yScale = yScale
        self.message = message
        self.buttons.append(self)
        self.fill = "Yellow"
    
    # app here refers to MainScreen
    def getCoords(self, app):
        x0 = app.width * self.xScale - app.buttonW
        y0 = app.height * self.yScale - app.buttonH
        x1 = app.width * self.xScale + app.buttonW
        y1 = app.height * self.yScale + app.buttonH
        return x0, y0, x1, y1

class Icon(object):
    icons = []

    def __init__(self, towerType, message, price, imageLocation, padding=20):
        self.towerType = towerType
        self.message = message
        self.paddingText = padding
        self.price = price
        self.isSelected = False
        self.image = Image.open(imageLocation)
        self.icons.append(self)
        self.index = Icon.icons.index(self)

    def getCoords(self, app):
        x0 = app.height + app.margin
        y0 = app.margin * 4 + self.index * self.paddingText//2
        x1 = x0 + (app.width - app.height) // 5
        y1 = y0 + (x1 - x0)

        newPadding = (y1 - y0) + self.paddingText

        y0 += newPadding*(self.index+1)
        y1 += newPadding*(self.index+1)

        return x0, y0, x1, y1


    def drawIcons(self, app, canvas, i):
        icon = Icon.icons[i]
        x0, y0, x1, y1 = Icon.getCoords(self, app)
        if self.isSelected == True:
            outline = "gold"
        else: outline = "black"
        canvas.create_rectangle(x0, y0, x1, y1, outline=outline)
        canvas.create_text((x0+x1)//2, (y0+y1)//2, text=f"\t\t\t\t\t\t\t{icon.towerType.cost}")
        canvas.create_text(x1+self.paddingText, (y0+y1)//2, anchor="w", text=self.message)
        return x0, y0, x1, y1


'''Main Screen'''
class MainScreen(Mode):
    def isInButton(self, x, y):
        for button in self.buttons:
            x0, y0, x1, y1 = button.getCoords(self)
            if x0 <= x <= x1 and y0 <= y <= y1:
                return button
        return None

    def appStarted(self):
        self.margin = 15
        self.buttonH = self.height // 12
        self.buttonW = self.width // 5
        self.yScaleTitle = 1 / 8

        self.buttons = []
        self.button1 = Button(1/3, "Play Tutorial!")
        self.button2 = Button(1/2, "Generate Level!")
        self.button3 = Button(2/3, "View High Scores!")

        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)


    def mousePressed(self, event):
        selected = self.isInButton(event.x, event.y)
        # here the mode will be changed to the approproate one
        if selected == self.button1: 
            self.app.setActiveMode(TutorialScreen())
        elif selected == self.button2:
            self.app.setActiveMode(GenerateScreen())
        elif selected == self.button3:
            self.app.setActiveMode(HighScorePage())


    def drawButtons(self, canvas):
        for button in self.buttons:
            x0, y0, x1, y1 = button.getCoords(self)
            canvas.create_rectangle(x0, y0, x1, y1, fill = button.fill)
            canvas.create_text(self.width // 2, self.height * button.yScale,
                text = button.message)


    def redrawAll(self, canvas):
        canvas.create_text(self.width // 2, self.height * self.yScaleTitle, 
            text="Ants at the Picnic")
        self.drawButtons(canvas)
    

class GenerateScreen(Mode):
    def appStarted(self):
        self.margin = 15
        self.buttonH = self.height // 15
        self.buttonW = self.width // 7
        self.yScaleTitle = 1 / 8
        self.userInput = ""
        self.canType = False

        self.buttons = []
        self.buttonEasy = Button(1/6, "Easy", 1/3)
        self.buttonMedium = Button(2/6, "Medium", 1/3)
        self.buttonHard = Button(3/6, "Hard", 1/3)
        self.buttons.append(self.buttonEasy)
        self.buttons.append(self.buttonMedium)
        self.buttons.append(self.buttonHard)

        self.selectedButton = None
    
    def drawButtons(self, canvas):
        for button in self.buttons:
            x0, y0, x1, y1 = button.getCoords(self)
            y0 += self.margin * 2
            y1 += self.margin * 2
            canvas.create_rectangle(x0, y0, x1, y1, fill = button.fill)
            canvas.create_text(self.width * button.xScale, self.margin * 2 + self.height * button.yScale,
                text = button.message)

    def isInButton(self, x, y):
        for button in self.buttons:
            x0, y0, x1, y1 = button.getCoords(self)
            if x0 <= x <= x1 and y0 <= y - 2*self.margin <= y1:
                return button
        return None

    def mousePressed(self, event):
        if self.isInButton(event.x, event.y) != None:
            self.canType = False
            button = self.isInButton(event.x, event.y)
            if self.selectedButton == None:
                button.fill = "Red"
                self.selectedButton = button
            elif button == self.selectedButton:
                button.fill = "Yellow"
                self.selectedButton = None
            else:
                oldButton = self.selectedButton
                oldButton.fill = "Yellow"
                button.fill = "Red"
                self.selectedButton = button

        elif self.isInTextbox(event.x, event.y):
                self.canType = not self.canType
        
        else:
            self.canType = False
            if self.isInGenerateButton(event.x, event.y) and int(self.userInput) >= 2 and self.selectedButton != None:
                if int(self.userInput) > 50: # this is some arbitrary number for now
                    pass
                else: 
                    self.app.numWaves = int(self.userInput)
                    self.app.difficulty = self.selectedButton.message
                    self.app.setActiveMode(NewLevel())

    def isInTextbox(self, x, y):
        x0 = self.width * 2 // 3 - self.buttonW // 2
        x1 = x0 + self.buttonW
        y0 = self.height * 1 // 6 - self.buttonH // 2 + self.margin * 2
        y1 = y0 + self.buttonH
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
        else: return False

    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setActiveMode(self.app.homeScreen)
        elif self.canType:
            if event.key in string.digits:
                self.userInput += event.key
            elif event.key == "Backspace":
                self.userInput = self.userInput[:-1]


    def drawTextInput(self, canvas):
        x0 = self.width * 2 / 3 - self.buttonW / 2
        x1 = x0 + self.buttonW
        y0 = self.height * 1 / 6 - self.buttonH / 2 + self.margin * 2
        y1 = y0 + self.buttonH
        canvas.create_rectangle(x0,y0,x1,y1)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=self.userInput)
        if self.canType:
            canvas.create_text((x0+x1)/2, y0 - self.margin, text="Type how many waves you'd like!")

    def isInGenerateButton(self, x, y):
        generateW = 0.8 * self.width
        x0 = self.width//2 - generateW/2
        x1 = x0 + generateW
        y0 = 3 / 4 * self.height
        y1 = y0 + 1/6 * self.height
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
        else: return False

    def drawGenerateButton(self, canvas):
        generateW = 0.8 * self.width
        x0 = self.width//2 - generateW/2
        x1 = x0 + generateW
        y0 = 3 / 4 * self.height
        y1 = y0 + 1/6 * self.height
        canvas.create_rectangle(x0,y0,x1,y1,fill="light gray")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text="Generate Me!")


    def redrawAll(self, canvas):
        canvas.create_text(self.width // 3, self.margin * 4, text="Select Difficulty")
        self.drawButtons(canvas) 
        canvas.create_text(self.width * 2 // 3, self.margin * 4, text="How many waves would you like? (5-49)")
        self.drawTextInput(canvas)
        self.drawGenerateButton(canvas)

class NewLevel(Mode):
    def appStarted(self): 
        self.numWaves = self.app.numWaves
        self.margin = 10
        self.canType = False
        self.userName = ""
        self.pressedEnter = False

        if self.app.difficulty == "Easy":
            self.lives = 25 
            self.coins = 100
            self.level = Level(6, 8)
            self.scoreMultiplier = 0
            
        elif self.app.difficulty ==  "Medium":
            self.lives = 20
            self.coins = 75
            self.level = Level(9, 11)
            self.scoreMultiplier = 1
        
        elif self.app.difficulty == "Hard":
            self.lives = 15
            self.coins = 50
            self.level = Level(12, 14)
            self.scoreMultiplier = 2

        self.levelGrid = self.level.maze
        self.enemyStartRow = self.level.enemyStartRow
        self.enemyStartCol = self.level.enemyStartCol
        self.rows = self.cols = len(self.levelGrid)
        self.defaultSize = max(self.rows, self.cols)
        self.colW = self.rowH = (self.height - 2 * self.margin) / self.defaultSize
        
        if self.app.difficulty == "Easy":
            self.waves = EasyEnemyList(self.numWaves, self.enemyStartRow, 
                self.enemyStartCol, self.margin, self.rowH, self.colW)
            
        elif self.app.difficulty ==  "Medium":
            self.waves = MediumEnemyList(self.numWaves, self.enemyStartRow, 
                self.enemyStartCol, self.margin, self.rowH, self.colW)
        
        elif self.app.difficulty == "Hard":
            self.waves = HardEnemyList(self.numWaves, self.enemyStartRow, 
                self.enemyStartCol, self.margin, self.rowH, self.colW)

        self.waves.generateAllWaves()
        self.allEnemies = self.waves.enemyList
        self.wave = 1
        self.enemies = self.allEnemies[self.wave - 1]
        self.towerList = []
        self.enemiesOnScreen = []
        self.pathColor = rgbString(230, 199, 114)
        self.textSize = int(self.rowH // 4)
        self.timerCounts = 0
        self.gamePlaying = False
        self.gameOver = False
        self.gameWon = False
        self.towerToPlace = None
        self.enemyPath = []
        self.stupidEnemyPath = []
        self.basePic = Image.open("basicTower.png")
        self.getEnemyPath(self.enemyStartRow, self.enemyStartCol, [], [False])
        self.getStupidEnemyPath(self.enemyStartRow, self.enemyStartCol, [], [False])
        self.mousePosition = [-1,-1]
        self.score = 0
        self.enemiesKilled = [0, 0]


        if len(self.enemyPath) == 0: 
            self.appStarted()

        else: 
            self.setEnemyPathdXdY()
            Icon.icons = []
            Icon(BasicTower, "Basic Tower", 20, "basicTower.png")
            Icon(ShootingTower, "Shooting Tower", 30, "shootingTower.png")
            self.adjustImages()
    
    def adjustImages(self):
        BasicTower.image = Image.open("basicTower.png")
        BasicTower.image = self.scaleImage(BasicTower.image, 1/self.rows)
        ShootingTower.image = Image.open("shootingTower.png")
        ShootingTower.image = self.scaleImage(ShootingTower.image, 1/self.rows)

        self.basePic = Image.open("base.png")
        self.basePic = self.scaleImage(self.basePic, 1/(self.rows*4))


    def getEnemyPath(self, startRow, startCol, currPath, isDone):
        dirs = [(1,0), (0,1), (0,-1), (-1,0)]
        if not isDone[0] and 0 <= startRow < len(self.levelGrid) and 0 <= startCol < len(self.levelGrid[0]):
            if self.levelGrid[startRow][startCol] == "Base":
                currPath.append((startRow, startCol))
                self.enemyPath = copy.deepcopy(currPath)
                isDone[0] = True
            elif self.levelGrid[startRow][startCol] == False and (startRow, startCol) not in currPath:
                currPath.append((startRow, startCol))
                for drow, dcol in dirs:
                        self.getEnemyPath(startRow+drow, startCol+dcol, currPath, isDone)
                if not isDone[0]:
                    currPath.remove((startRow, startCol))

    def getStupidEnemyPath(self, startRow, startCol, currPath, isDone):
        dirs = [(1,0), (0,1), (0,-1), (-1,0)]
        if not isDone[0] and 0 <= startRow < len(self.levelGrid) and 0 <= startCol < len(self.levelGrid[0]):
            if self.levelGrid[startRow][startCol] == "Base":
                currPath.append((startRow, startCol))
                self.stupidEnemyPath = copy.deepcopy(currPath)
                isDone[0] = True
            elif self.levelGrid[startRow][startCol] == False and (startRow, startCol) not in currPath:
                currPath.append((startRow, startCol))
                for i in range(len(dirs)):
                    drow, dcol = random.choice(dirs)
                    dirs.remove((drow, dcol))
                    self.getStupidEnemyPath(startRow+drow, startCol+dcol, currPath, isDone)
                currPath.append((startRow, startCol))

    def setEnemyPathdXdY(self):
        for enemy in self.enemies:
            foe = enemy[0]
            if foe.__class__.__name__ == "StupidAnt":
                self.getStupidEnemyPath(self.enemyStartRow, self.enemyStartCol, [], [False])
                foe.path = copy.deepcopy(self.stupidEnemyPath)
            elif foe.__class__.__name__ == "BasicAnt":
                foe.path = copy.deepcopy(self.enemyPath)

            foe.row = self.enemyPath[0][0]
            foe.col = self.enemyPath[0][1]
            foe.cx, foe.cy = getCenterCell(self, foe.row, foe.col)
            foe.dy = self.enemyPath[1][0] - foe.row
            foe.dx = self.enemyPath[1][1] - foe.col
            foe.backDx = foe.dx
            foe.backDy = foe.dy


            foe.image = self.scaleImage(foe.image, 1/(1.5*self.rows))
            
            foe.width, foe.height = foe.image.size
            
            if foe.dy == 1: foe.image = foe.image.rotate(180)

            # it will set the enemies to start at random places on the grid
            randDisplacement = random.randint(-self.colW//4,self.colW//4)
            if foe.dy == 0:
                foe.cy += randDisplacement
                foe.front = [foe.cx + foe.height//2, foe.cy]
                foe.back = [foe.cx - foe.height//2, foe.cy]
                if foe.dx == -1:
                    foe.front, foe.back = foe.back, foe.front
            elif foe.dx == 0: 
                foe.cx += randDisplacement
                foe.front = [foe.cx, foe.cy + foe.height//2]
                foe.back = [foe.cx, foe.cy - foe.height//2]
                if foe.dy == -1:
                    foe.front, foe.back = foe.back, foe.front


    # press escape to go back to the main menu and 2 to pull up the wiki
    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setActiveMode(self.app.homeScreen)
        if event.key == "1":
            self.appStarted()

        if self.gameOver == False or self.gameWon == False:
            if event.key == "p":
                self.gamePlaying = not self.gamePlaying
        
        if self.canType:
            if event.key in string.ascii_letters:
                self.userName += event.key
            elif event.key == "Backspace":
                self.userName = self.userName[:-1]
        if event.key == "Enter" and len(self.userName) > 0:
            updateHighScore(self)
            self.pressedEnter = True

    def drawGameWon(self, canvas):
        boardLength = self.colW * self.cols
        canvas.create_rectangle(self.margin*5, self.height* 1 // 4, 
            self.margin + self.cols * self.colW - self.margin*3, 
            self.height * 3 // 4, fill = "Light Blue", outline="Gold")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 6, 
            text="You Won!", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 12, 
            text="Press escape to go to the menu", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height // 2, 
            text="Press 1 to try a new board", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 12, 
            text=f"You killed: {self.enemiesKilled[0]} Ants and {self.enemiesKilled[1]} Stupid Ants", font=f"Helveltica {self.textSize}")

        if not self.pressedEnter:
            canvas.create_rectangle(self.margin + boardLength//6, self.height*3/4-self.margin*8,
                self.margin+boardLength//2, self.height*3/4-self.margin*2)
            canvas.create_text(self.margin+boardLength/3, self.height*3/4 - self.margin*5,
                text=self.userName)
            canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 7,
                text="\t\t\t\t\t\t\t\tClick the box!")
            if self.canType:
                canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 5,
                    text="\t\t\t\t\t\t\t\tType your name & press enter to add to the high score list")



    def checkGameOver(self):
        if self.lives <= 0: 
            self.gameOver = True
            self.gamePlaying = False

    def moveEnemies(self):
        newEnemies = []
        for enemy in self.enemiesOnScreen:
            if self.levelGrid[enemy.row][enemy.col] == "Base":
                self.lives -= 1
                self.checkGameOver()
            else: 
                newEnemies.append(enemy)
                enemy.move(self.margin)
        self.enemiesOnScreen = newEnemies


    # checks if enemies should appear on-screen yet
    def checkEnemies(self):
        newEnemies = []
        for enemy in self.enemies:
            if enemy[1] <= self.timerCounts:
                self.enemiesOnScreen.append(enemy[0])
            else: 
                newEnemies.append(enemy)
        self.enemies = newEnemies

    def calculateScore(self):
        basicKilled, stupidKilled = self.enemiesKilled
        self.score = (basicKilled + 2 * stupidKilled) * 2 ** self.scoreMultiplier
        if self.gameOver or self.gameWon:
            self.score = (self.coins + basicKilled + 2 * stupidKilled) * 2 ** self.scoreMultiplier

    def timerFired(self):
        if self.gameOver or self.gameWon:
            self.calculateScore()
        if self.gamePlaying == True:
            self.timerCounts += 0.1
            self.moveEnemies()
            self.checkEnemies()
            self.towersAttack()
            self.moveProjectiles()
            self.removeDeadEnemies()
            self.calculateScore()
            if self.checkWaveComplete():
                # load the next wave into the enemyList and start the next wave
                if self.wave < len(self.allEnemies):
                    self.coins += 10 * self.wave
                    self.wave += 1
                    self.enemies = self.allEnemies[self.wave - 1]
                    self.setEnemyPathdXdY()
                    self.timerCounts = 0
                else: 
                    self.gameWon = True
                    self.gamePlaying = False
    

    def moveProjectiles(self):
        boardLength = self.colW * self.cols + self.margin
        for tower in self.towerList:
            newProjectileList = []

            if isinstance(tower, BasicTower):
                for projectile in tower.projectiles:
                    if projectile.enemy.health > 0:
                        projectile.dx, projectile.dy = self.getDirToEnemy(projectile, projectile.enemy)
                    projectile.cx += projectile.dx * projectile.speed
                    projectile.cy += projectile.dy * projectile.speed
                    if (distance(projectile.cx, projectile.cy, projectile.enemy.cx, projectile.enemy.cy) < projectile.enemy.width
                        and projectile.enemy.health > 0):
                        if isinstance(projectile.enemy, StupidAnt): multiplier = 1
                        else: multiplier = 2
                        projectile.enemy.health -= BasicTower.damage * multiplier
                    elif self.collide(projectile) != None:
                        enemy = self.collide(projectile)
                        if isinstance(enemy, StupidAnt): multiplier = 1
                        else: multiplier = 2
                        enemy.health -= BasicTower.damage * multiplier
                    elif projectile.cx < self.margin or projectile.cx > boardLength or projectile.cy < self.margin or projectile.cy > boardLength:
                        pass 
                    else: 
                        newProjectileList.append(projectile)
                tower.projectiles = newProjectileList
            
            elif isinstance(tower, ShootingTower):
                for projectile in tower.projectiles:
                    projectile.cx += projectile.dx * projectile.speed
                    projectile.cy += projectile.dy * projectile.speed   
                    if self.collide(projectile) != None:
                        enemy = self.collide(projectile)   
                        if isinstance(enemy, StupidAnt): multiplier = 2 
                        else: multiplier = 1
                        enemy.health -= ShootingTower.damage * multiplier
                    else:
                        newProjectileList.append(projectile)
                tower.projectiles = newProjectileList            
    
    def collide(self, projectile):
        for enemy in self.enemiesOnScreen:
            if distance(projectile.cx, projectile.cy, enemy.cx, enemy.cy) < enemy.width * 3 / 4:
                return enemy
        return None


    def checkWaveComplete(self):
        if len(self.enemiesOnScreen) == len(self.enemies) == 0:
            return True
        elif len(self.enemies) == 0:
            for enemy in self.enemiesOnScreen:
                if enemy.__class__.__name__ != "StupidAnt":
                    return False
            return True
        else:
            return False

    def removeDeadEnemies(self):
        remainingEnemies = []
        for enemy in self.enemiesOnScreen:
            if enemy.health > 0:
                remainingEnemies.append(enemy)
            else: 
                self.coins += enemy.coinWorth
                if isinstance(enemy, StupidAnt):
                    self.enemiesKilled[1] += 1
                else: 
                    self.enemiesKilled[0] += 1
        self.enemiesOnScreen = remainingEnemies

    def towersAttack(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tower = self.levelGrid[row][col]
                if tower != False and tower != None and tower != "Base":
                    tower.timeOnScreen += 1

                if isinstance(tower, BasicTower) and tower.timeOnScreen % BasicTower.attackSpeed == 0:
                    # this only returns one enemy, for towers that can have multiple targets, this needs to be modified
                    enemyInRange = checkEnemyinRange(self, tower)
                    if enemyInRange != None:
                        cx, cy = getCenterCell(self, tower.row, tower.col)
                        bullet = ProjectileBasic(self, cx, cy, enemyInRange)
                        bullet.dx, bullet.dy = self.getDirToEnemy(bullet, enemyInRange)
                        tower.projectiles.append(bullet)
                
                elif isinstance(tower, ShootingTower) and tower.timeOnScreen % ShootingTower.attackSpeed == 0:
                    cx, cy = getCenterCell(self, tower.row, tower.col) 
                    bullet = ProjectileShooting(self, cx, cy)
                    
                    hypot = distance(self.mousePosition[0], self.mousePosition[1], bullet.cx, bullet.cy)
                    width = self.mousePosition[0] - bullet.cx
                    height = self.mousePosition[1] - bullet.cy
                    angle = math.acos(width/hypot)
                    
                    bullet.dx = math.cos(angle)
                    bullet.dy = math.sin(angle)
                    if height < 0: bullet.dy *= -1

                    tower.projectiles.append(bullet)


    # # returns the location (of 8) that is the closest to the enemy
    def getDirToEnemy(self, bullet, enemy):
        dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        # we want it to hit the closest part of the enemy..... this is not doing that yet
        bestDistance = distance(bullet.cx, bullet.cy, enemy.cx, enemy.cy)
        bestDir = (0,0)
        for direction in dirs:
            dx = direction[0]
            dy = direction[1]
            dist = distance(bullet.cx + dx, bullet.cy + dy, enemy.cx, enemy.cy)
            if dist < bestDistance: 
                bestDistance = dist
                bestDir = direction 
        return bestDir

    def drawGrid(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                color = "Green"
                if self.levelGrid[row][col] == False: 
                    color = self.pathColor
                # eventually this should be filled in as an image of a picnic basket
                elif self.levelGrid[row][col] == "Base":
                    color = "Light Blue"
                x0 = self.margin + self.colW * col
                x1 = x0 + self.colW
                y0 = self.margin + self.rowH * row
                y1 = y0 + self.rowH
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, width="0")
                if self.levelGrid[row][col] == "Base":
                    canvas.create_image((x0+x1)/2, (y0+y1)/2, image=ImageTk.PhotoImage(self.basePic))
                    canvas.create_text(x0 + self.colW / 2, y0 + self.margin*2,
                        text=self.lives, fill="White", font=f"Helveltica {self.textSize}")
                
    def drawTowers(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x0 = self.margin + self.colW * col
                x1 = x0 + self.colW
                y0 = self.margin + self.rowH * row
                y1 = y0 + self.rowH
                if isinstance(self.levelGrid[row][col], ShootingTower):
                    canvas.create_image((x0+x1)//2,(y0+y1)//2, image=ImageTk.PhotoImage(ShootingTower.image))
                if isinstance(self.levelGrid[row][col], BasicTower):
                    canvas.create_image((x0+x1)//2,(y0+y1)//2, image=ImageTk.PhotoImage(BasicTower.image))
                    

    def mousePressed(self, event):
        if self.gameOver or self.gameWon:
            boardLength = self.colW * self.cols
            if (self.margin + boardLength//6 < event.x < self.margin+boardLength//2
                and self.height*3/4-self.margin*8 < event.y < self.height*3/4-self.margin*2):
                self.canType = True
            else: self.canType = False

        if self.gameWon == False and self.gameOver == False:
            if onGrid(self, event.x, event.y):
                row, col = getRowCol(self, event.x, event.y)
                if self.towerToPlace != None and self.levelGrid[row][col] == None:
                    self.coins -= self.towerToPlace.cost
                    newTower = self.towerToPlace(row, col)
                    self.towerList.append(newTower)
                    self.levelGrid[row][col] = newTower
                    self.towerToPlace = None
                    for icon in Icon.icons:
                        if icon.isSelected: icon.isSelected = not icon.isSelected
        
            elif onSidebarIcon(self, event.x, event.y) != None:
                tower = onSidebarIcon(self, event.x, event.y)
                if self.towerToPlace == tower:
                    self.towerToPlace = None
                    
                if tower.cost <= self.coins:
                    self.towerToPlace = onSidebarIcon(self, event.x, event.y)
            

    def drawEnemies(self, canvas):
        for enemy in self.enemiesOnScreen:
            x = enemy.front[0] - enemy.back[0]
            if abs(x) > enemy.height: 
                if x > 0: x = enemy.height
                else: x = - enemy.height

            angle = math.degrees(math.acos((x)/(enemy.height)))
            angle -= 90
            image = enemy.image
            imageRotated = image.rotate(angle)
            canvas.create_image(enemy.cx, enemy.cy, image=ImageTk.PhotoImage(imageRotated))

            if enemy.__class__.__name__ == "StupidAnt": defaultHealth = 15
            else: defaultHealth = 20

            if self.app.difficulty == "Easy":
                fraction = enemy.health /((self.wave - 1) * 2 + defaultHealth)
            elif self.app.difficulty == "Medium":
                fraction = enemy.health /((self.wave - 1) * 4 + defaultHealth)
            elif self.app.difficulty == "Hard":
                fraction = enemy.health /((self.wave - 1) * 6 + defaultHealth)
            left = enemy.cx - enemy.width//2
            right = left + fraction * enemy.width
            top = enemy.cy - enemy.width
            bottom = top + 10
            canvas.create_rectangle(left, top, right, bottom, fill="light green")
            canvas.create_text((left+right)/2, (top+bottom)/2,text=str(enemy.health))

    def drawGameOver(self, canvas):
        boardLength = self.colW * self.cols
        canvas.create_rectangle(self.margin*5, self.height* 1 // 4, 
            self.margin + self.cols * self.colW - self.margin*3, 
            self.height * 3 // 4, fill = "Light Blue", outline="Gold")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 6, 
            text="Game Over!", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 12, 
            text="Press escape to go to the menu", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height // 2, 
            text="Press 1 to try a new board", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 12, 
            text=f"You killed: {self.enemiesKilled[0]} Ants and {self.enemiesKilled[1]} Stupid Ants", font=f"Helveltica {self.textSize}")

        if not self.pressedEnter:
            canvas.create_rectangle(self.margin + boardLength//6, self.height*3/4-self.margin*8,
                self.margin+boardLength//2, self.height*3/4-self.margin*2)
            canvas.create_text(self.margin+boardLength/3, self.height*3/4 - self.margin*5,
                text=self.userName)
            canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 7,
                text="\t\t\t\t\t\t\t\tClick the box!")
            if self.canType:
                canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 5,
                    text="\t\t\t\t\t\t\t\tType your name & press enter to add to the high score list")

    def drawSidebar(self, canvas):
        x0 = self.height
        x1 = self.width
        y0 = 0
        y1 = self.height
        paddingText = 20 

        canvas.create_rectangle(x0, y0, x1, y1, fill="light blue")
        canvas.create_text((x1 + x0)//2, self.margin * 2, text=f"{self.coins} coins")
        canvas.create_text((x1 + x0)//2, self.margin * 4, text=f"Wave {self.wave}")
        canvas.create_text((x1 + x0)//2, y1 - self.margin * 4, text=f"{self.score} points")

        for i in range(len(Icon.icons)):
            icon = Icon.icons[i]
            image = icon.image
            image = self.scaleImage(image, 1/(self.rows*2.75))
            x0, y0, x1, y1 = icon.drawIcons(self, canvas, i)
            canvas.create_image((x0+x1)/2, (y0+y1)/2, image=ImageTk.PhotoImage(image))

    def mouseMoved(self, event):
        self.mousePosition = [event.x, event.y]


    def drawProjectiles(self, canvas):
        for tower in self.towerList:
            for projectile in tower.projectiles:
                projectile.drawProjectile(canvas)


    def redrawAll(self, canvas):
        self.drawGrid(canvas)
        self.drawTowers(canvas)
        self.drawProjectiles(canvas)
        self.drawEnemies(canvas)
        canvas.create_rectangle(0,0,self.width, self.margin, fill="White", width="0")
        self.drawSidebar(canvas)

        if self.gameOver:
            self.drawGameOver(canvas)
        
        if self.gameWon:
            self.drawGameWon(canvas)


def getCenterCell(self, row, col):
    x = self.margin + col * self.colW + self.colW // 2
    y = self.margin + row * self.rowH + self.rowH // 2
    return x, y

def makeEnemies(self):
    res = []
    for i in range(5):
        antX, antY = getCenterCell(self, 0, 3)
        antY -= self.rowH // 2
        timeEntered = random.randint(0,15)
        newHealth = BasicAnt.health + 5 * i
        res.append((BasicAnt(antX, antY, self.colW, newHealth), timeEntered))
    return res

def onGrid(self, x, y):
    if self.margin < x < self.height - self.margin and self.margin < y < self.height - self.margin:
        return True
    else: return False

def getRowCol(self, x, y):
    if onGrid(self, x, y):
        row = (y - self.margin) // self.rowH
        col = (x - self.margin) // self.colW
        return int(row), int(col)
    else: return -1, -1

def getNextRowColDir(self, enemy, row, col):
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    for direction in dirs:
        drow = direction[0]
        dcol = direction[1]
        newRow = row + drow
        newCol = col + dcol
        if 0 <= newRow < self.rows and 0 <= newCol < self.cols:
            if ((newRow, newCol) not in enemy.visitedSquares and 
                (self.levelGrid[newRow][newCol] == False) or self.levelGrid[newRow][newCol] == "Base"):
                return direction

def onSidebarIcon(self, x, y):
    for icon in Icon.icons:
        x0, y0, x1, y1 = icon.getCoords(self)
        if x0 < x < x1 and y0 < y < y1:
            icon.isSelected = not icon.isSelected
            return icon.towerType
    return None

def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

def checkEnemyinRange(self, tower):
    for enemy in self.enemiesOnScreen:
        attackRadius = tower.attackRadius * self.rowH
        towerX, towerY = getCenterCell(self, tower.row, tower.col)
        if distance(towerX, towerY, enemy.cx, enemy.cy) < attackRadius:
            return enemy
    return None

'''Tutorial Screen'''
class TutorialScreen(Mode):
    def appStarted(self): 
        self.levelGrid = [
            [None, None, None, False, None, None],
            [None, None, None, False, False, None],
            [None, "Base", None, None, False, None],
            [None, False, None, False, False, None],
            [None, False, False, False, None, None],
            [None, None, None, None, None, None]
        ]

        self.margin = 10
        self.rows = len(self.levelGrid)
        self.cols = len(self.levelGrid[0])
        self.defaultSize = max(self.rows, self.cols)
        self.colW = self.rowH = (self.height - 2 * self.margin) / self.defaultSize
        
        self.allEnemies = []
        for i in range(5):
            self.allEnemies.append(makeEnemies(self))

        self.wave = 1
        self.enemies = self.allEnemies[self.wave - 1]
        self.towerList = []
        self.enemiesOnScreen = []
        self.lives = 25       
        self.pathColor = rgbString(230, 199, 114)
        self.textSize = int(self.rowH // 4)
        self.timerCounts = 0
        self.gamePlaying = False
        self.gameOver = False
        self.coins = 100
        self.towerToPlace = None
        self.gameWon = False
        Icon.icons = []
        Icon(BasicTower,"Basic Tower", 20, "basicTower.png")


    # press escape to go back to the main menu and w to pull up the wiki
    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setActiveMode(self.app.homeScreen)
        if event.key == "1":
            self.appStarted()

        if self.gameOver == False or self.gameWon == False:
            if event.key == "p":
                self.gamePlaying = not self.gamePlaying


    def checkGameOver(self):
        if self.lives <= 0: 
            self.gameOver = True
            self.gamePlaying = False
        
    def moveEnemies(self):
        newEnemies = []
        for enemy in self.enemiesOnScreen:
            currRow, currCol = getRowCol(self, enemy.cx, enemy.cy)
            if self.levelGrid[currRow][currCol] == "Base":
                self.lives -= 1
                self.checkGameOver()
            else: 
                newEnemies.append(enemy)
            
            enemy.visitedSquares.add((currRow, currCol))
            centerCellX, centerCellY = getCenterCell(self, currRow, currCol)

            if -5 <= (centerCellX - enemy.cx) <= 5 and -5 <= (centerCellY - enemy.cy) <= 5:
                dy, dx = getNextRowColDir(self, enemy, currRow, currCol)
                enemy.dx = dx
                enemy.dy = dy            
            enemy.cx += enemy.speed * enemy.dx
            enemy.cy += enemy.speed * enemy.dy
        self.enemiesOnScreen = newEnemies

    # checks if enemies should appear on-screen yet
    def checkEnemies(self):
        newEnemies = []
        for enemy in self.enemies:
            if enemy[1] <= self.timerCounts:
                self.enemiesOnScreen.append(enemy[0])
            else: 
                newEnemies.append(enemy)
        self.enemies = newEnemies

    def timerFired(self):
        if self.gamePlaying == True:
            self.timerCounts += 0.1
            self.moveEnemies()
            self.checkEnemies()
            self.towersAttack()
            self.moveProjectiles()
            self.removeDeadEnemies()
            if self.checkWaveComplete():
                # load the next wave into the enemyList and start the next wave
                if self.wave < len(self.allEnemies):
                    self.wave += 1
                    self.enemies = self.allEnemies[self.wave - 1]
                    self.timerCounts = 0
                # for the else case this should switch to a "You Won!" screen -- this will be added later
                else: 
                    self.gameWon = True
    
    def collide(self, projectile):
        for enemy in self.enemiesOnScreen:
            if distance(projectile.cx, projectile.cy, enemy.cx, enemy.cy) < enemy.width * 3 / 4:
                return enemy
        return None

    def moveProjectiles(self):
        boardLength = self.colW * self.cols + self.margin
        for tower in self.towerList:
            newProjectileList = []
            for projectile in tower.projectiles:
                if projectile.enemy.health >0: projectile.dx, projectile.dy = self.getDirToEnemy(projectile, projectile.enemy)
                projectile.cx += projectile.dx * projectile.speed
                projectile.cy += projectile.dy * projectile.speed
                if distance(projectile.cx, projectile.cy, projectile.enemy.cx, projectile.enemy.cy) < projectile.enemy.width:
                    projectile.enemy.health -= 1
                elif self.collide(projectile) != None:
                    enemy = self.collide(projectile)
                    enemy.health -= 1
                elif projectile.cx < self.margin or projectile.cx > boardLength or projectile.cy < self.margin or projectile.cy > boardLength:
                    pass
                else: 
                    newProjectileList.append(projectile)
            tower.projectiles = newProjectileList
                    

    def checkWaveComplete(self):
        if len(self.enemiesOnScreen) == len(self.enemies) == 0:
            return True


    def removeDeadEnemies(self):
        remainingEnemies = []
        for enemy in self.enemiesOnScreen:
            if enemy.health > 0:
                remainingEnemies.append(enemy)
            else: self.coins += enemy.coinWorth
        self.enemiesOnScreen = remainingEnemies

    def towersAttack(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.levelGrid[row][col], BasicTower):
                    tower = self.levelGrid[row][col]
                    tower.timeOnScreen += 1
                    # this only returns one enemy, for towers that can have multiple targets, this needs to be modified
                    if tower.timeOnScreen % 5 == 0:
                        enemyInRange = checkEnemyinRange(self, tower)
                        if enemyInRange != None:
                            cx, cy = getCenterCell(self, tower.row, tower.col)
                            bullet = ProjectileBasic(self, cx, cy, enemyInRange)
                            bullet.dx, bullet.dy = self.getDirToEnemy(bullet, enemyInRange)
                            tower.projectiles.append(bullet)

    # returns the location (of 8) that is the closest to the enemy
    def getDirToEnemy(self, bullet, enemy):
        dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        # we want it to hit the closest part of the enemy..... this is not doing that yet
        bestDistance = distance(bullet.cx, bullet.cy, enemy.cx, enemy.cy)
        bestDir = (0,0)
        for direction in dirs:
            dx = direction[0]
            dy = direction[1]
            dist = distance(bullet.cx + dx, bullet.cy + dy, enemy.cx, enemy.cy)
            if dist < bestDistance: 
                bestDistance = dist
                bestDir = direction 
        return bestDir

    def drawGrid(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                color = "Green"
                if self.levelGrid[row][col] == False: 
                    color = self.pathColor
                # eventually this should be filled in as an image of a picnic basket
                elif self.levelGrid[row][col] == "Base":
                    color = "Brown"
                x0 = self.margin + self.colW * col
                x1 = x0 + self.colW
                y0 = self.margin + self.rowH * row
                y1 = y0 + self.rowH
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, width="0")
                if color == "Brown":
                    canvas.create_text(x0 + self.colW / 2, y0 + self.rowH / 2,
                        text=self.lives, fill="White", font=f"Helveltica {self.textSize}")
                

    def drawTowers(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                if isinstance(self.levelGrid[row][col], BasicTower):
                    towerType = self.levelGrid[row][col].__class__.__name__
                    x0 = self.margin + self.colW * col
                    x1 = x0 + self.colW
                    y0 = self.margin + self.rowH * row
                    y1 = y0 + self.rowH
                    canvas.create_rectangle(x0, y0, x1, y1, fill="Red")  
                    

    def mousePressed(self, event):
        if self.gameWon == False and self.gameOver == False:
            if onGrid(self, event.x, event.y):
                row, col = getRowCol(self, event.x, event.y)
                if self.towerToPlace != None and self.levelGrid[row][col] == None:
                    self.coins -= self.towerToPlace.cost
                    newTower = self.towerToPlace(row, col)
                    self.towerList.append(newTower)
                    self.levelGrid[row][col] = newTower
                    self.towerToPlace = None
                    for icon in Icon.icons:
                        if icon.isSelected: icon.isSelected = not icon.isSelected
        
            elif onSidebarIcon(self, event.x, event.y) != None:
                tower = onSidebarIcon(self, event.x, event.y)
                if self.towerToPlace == tower:
                    self.towerToPlace = None
                if tower.cost <= self.coins:
                    self.towerToPlace = onSidebarIcon(self, event.x, event.y)            

    def drawEnemies(self, canvas):
        for enemy in self.enemiesOnScreen:
            x0 = enemy.cx - enemy.width // 2
            x1 = x0 + enemy.width
            y0 = enemy.cy - enemy.height // 2
            y1 = y0 + enemy.height
            canvas.create_oval(x0, y0, x1, y1, fill="Black")

    def drawGameOver(self, canvas):
        boardLength = self.colW * self.cols
        canvas.create_rectangle(self.margin*5, self.height* 1 // 4, 
            self.margin + self.cols * self.colW - self.margin*3, 
            self.height * 3 // 4, fill = "Light Blue", outline="Gold")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 12, 
            text="Game Over!", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height // 2, 
            text="Press escape to go to the menu", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 12, 
            text="Press 1 to try again", font=f"Helveltica {self.textSize}")
    
    def drawGameWon(self, canvas):
        boardLength = self.colW * self.cols
        canvas.create_rectangle(self.margin*5, self.height* 1 // 4, 
            self.margin + self.cols * self.colW - self.margin*3, 
            self.height * 3 // 4, fill = "Light Blue", outline="Gold")
        canvas.create_text(self.margin + boardLength//2, self.height * 1 / 4 + self.margin * 12, 
            text="You Won!", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height // 2, 
            text="Press escape to go to the menu", font=f"Helveltica {self.textSize}")
        canvas.create_text(self.margin + boardLength//2, self.height * 3 / 4 - self.margin * 12, 
            text="Press 1 to play again", font=f"Helveltica {self.textSize}")
    
    def drawSidebar(self, canvas):
        x0 = self.height
        x1 = self.width
        y0 = 0
        y1 = self.height
        paddingText = 20 

        # replace with image!
        canvas.create_rectangle(x0, y0, x1, y1, fill="light blue")
        canvas.create_text((x1 + x0)//2, self.margin * 2, text=f"{self.coins} coins")
        canvas.create_text((x1 + x0)//2, self.margin * 4, text=f"Wave {self.wave}")

        # will be an image of the tower
        for i in range(len(Icon.icons)):
            icon = Icon.icons[i]
            image = icon.image
            image = self.scaleImage(image, 1/(self.rows*2.75))
            x0, y0, x1, y1 = icon.drawIcons(self, canvas, i)
            canvas.create_image((x0+x1)/2, (y0+y1)/2, image=ImageTk.PhotoImage(image))


    def drawProjectiles(self, canvas):
        for tower in self.towerList:
            for projectile in tower.projectiles:
                projectile.drawProjectile(canvas)

    def redrawAll(self, canvas):
        self.drawGrid(canvas)
        self.drawTowers(canvas)
        self.drawProjectiles(canvas)
        self.drawEnemies(canvas)
        canvas.create_rectangle(0,0,self.width, self.margin, fill="White", width="0")
        self.drawSidebar(canvas)

        if self.gameOver:
            self.drawGameOver(canvas)
        
        if self.gameWon:
            self.drawGameWon(canvas)


class HighScorePage(Mode):
    def appStarted(self):
        self.page = HighScoreList()
        self.list = self.page.list
        
    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setActiveMode(MainScreen())
    

    def redrawAll(self, canvas):
        for i in range(15):
            if i < len(self.list):
                x0 = self.app.width * 2/6
                x1 = self.app.width * 4/6
                y0 = 50 + 50 * (i + 1)
                y1 = y0 + 50 
                if i == 0: fill = "gold"
                elif i == 1: fill = "light blue"
                elif i == 2: fill = "light green"
                else: fill = "light gray"
                canvas.create_rectangle(x0,y0,x1,y1, fill=fill)
                name, score = self.list[i]
                canvas.create_text(self.app.width/2 - 50, (y0+y1)/2, anchor="w", text=f"{i+1}\t{name}: {score}")

        



class MainApp(ModalApp):
    def appStarted(app):
        app.numWaves = -1
        app.difficulty = ""

        app.homeScreen = MainScreen()
        app.tutorialScreen = TutorialScreen()
        app.generateScreen = GenerateScreen()
        app.highScorePage = HighScorePage()
        app.setActiveMode(app.homeScreen)


MainApp(width=1125,height=900)