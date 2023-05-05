class Dot(object):
    # Make up trails behind rockets
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour


class Particle(Dot):
    # Used to animate explosions in maze-mode collisions
    def __init__(self, x, y, colour, startX, startY):
        self.startX = startX
        self.startY = startY
        super().__init__(x, y, colour)