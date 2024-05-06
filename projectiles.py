class ProjectileBasic(object):
    def __init__(self, app, cx, cy, enemy):
        self.speed = 5
        self.cx = cx
        self.cy = cy
        self.dx = 0
        self.dy = 1
        self.r = app.rowH // 20
        self.enemy = enemy
    
    def drawProjectile(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
            self.cx + self.r, self.cy + self.r, fill = "red")

class ProjectileShooting(ProjectileBasic):
    def __init__(self, app, cx, cy):
        self.cx = cx
        self.cy = cy
        self.speed = 5
        self.dx = 0
        self.dy = 0
        self.r = app.rowH // 19
    
    def drawProjectile(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
            self.cx + self.r, self.cy + self.r, fill = "gold")