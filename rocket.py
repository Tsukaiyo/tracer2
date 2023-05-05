from dot import Dot, Particle
import random
import time


class Rocket(object):
    explosion = []
    # Player object
    def __init__(self, colour, playerNum, x, y, speed, maxX, maxY):
        self.x = x
        self.y = y
        self.colour = colour
        self.playerNum = playerNum
        self.direction = "up"
        self.startX = x
        self.startY = y
        self.timeOfDeath = 0
        self.dots = []
        self.explosion = []
        self.speed = speed
        self.maxX = maxX
        self.maxY = maxY

    def shoot(self):
        # Leaves Dot trails
        self.dots.append(Dot(self.x, self.y, self.colour))
        if len(self.dots) > 250:
            del self.dots[0]

    def moveDown(self):
        if self.y < (self.maxY - self.speed):
            self.y = self.y + self.speed
            self.direction = "down"
            self.shoot()

    def moveUp(self):
        if self.y > self.speed:
            self.y = self.y - self.speed
            self.direction = "up"
            self.shoot()

    def moveLeft(self):
        if self.x > self.speed:
            self.x = self.x - self.speed
            self.direction = "left"
            self.shoot()

    def moveRight(self):
        if self.x < (self.maxX - self.speed):
            self.x = self.x + self.speed
            self.direction = "right"
            self.shoot()

    def reset(self):
        self.x = self.startX
        self.y = self.startY

    def lose(self):
        self.timeOfDeath = time.time()
        self.explode()
        self.reset()

    def explode(self):
        for i in range(8):
            self.explosion.append(Particle(self.x, self.y, self.colour))


class AniRocket(Rocket):
    # Animated rockets
    def __init__(self, colour, playerNum, x, y, speed, maxX, maxY):
        super().__init__(colour, playerNum, x, y, speed, maxX, maxY)
        self.endX = random.randint(max(self.x - 200, 0), min(self.x + 200, self.maxX))
        self.endY = random.randint(max(self.y - 200, 0), min(self.y + 200, self.maxY))

    def newTarget(self):
        self.endX = random.randint(max(self.x - 200, 0), min(self.x + 200, self.maxX))
        self.endY = random.randint(max(self.y - 200, 0), min(self.y + 200, self.maxY))

    def move(self):
        # Decides where the animated rockets move
        if (self.endX + 10 > self.x > self.endX - 10) and (self.endY + 10 > self.y > self.endY - 10):
            self.newTarget()

        if self.endX > self.x + 5:
            self.moveRight()
        elif self.endX < self.x - 5:
            self.moveLeft()
        if self.endY > self.y + 5:
            self.moveDown()
        elif self.endY < self.y - 5:
            self.moveUp()


