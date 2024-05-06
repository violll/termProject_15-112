from PIL import ImageTk, Image

class BasicTower(object):
    attackSpeed = 8
    damage = 1
    attackRadius = 2
    cost = 20
    color = "Red"
    image = Image.open("basicTower.png")
    iconImage = image
    def __init__(self, row, col):
        self.row = row
        self.col = col
        # a value of 10 = 1 second
        self.timeOnScreen = 0
        self.projectiles = []

class ShootingTower(object):
    attackSpeed = 5
    damage = 3
    cost = 30
    image = Image.open("shootingTower.png")
    iconImage = image
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.timeOnScreen = 0
        self.projectiles = []