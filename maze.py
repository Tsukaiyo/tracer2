import random
import pygame


class Maze(object):

    grid = []
    bloops = []
    turnList = []
    height = 0
    width = 0
    currentSquare = 0

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.genGrid()
        self.makeMaze()
        self.makeBloops()

    def genGrid(self):
        # make the grid for the maze
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                if y == 0:
                    self.grid[x].append(Square(True, True, True, True, x, y, True))
                else:
                    self.grid[x].append(Square(True, True, True, True, x, y, False))
        currentX = int(random.random() * self.width)
        currentY = int(random.random() * self.height - 1) + 1
        self.currentSquare = self.grid[currentX][currentY]
        self.currentSquare.visited = True
        self.turnList.append(self.currentSquare)

    def availableDirections(self, square):
        directions = []
        if square.x > 0:
            if not self.grid[square.x - 1][square.y].visited:
                directions.append(0)
        if square.y > 0:
            if not self.grid[square.x][square.y - 1].visited:
                directions.append(1)
        if square.x < self.width - 1:
            if not self.grid[square.x + 1][square.y].visited:
                directions.append(2)
        if square.y > self.height - 1:
            if not self.grid[square.x][square.y + 1].visited:
                directions.append(3)
        return directions

    def moveLeft(self):
        self.currentSquare.wWall = False
        self.currentSquare = self.grid[self.currentSquare.x - 1][self.currentSquare.y]
        self.currentSquare.eWall = False
        self.currentSquare.visited = True
        self.turnList.append(self.currentSquare)

    def moveUp(self):
        self.currentSquare.nWall = False
        self.currentSquare = self.grid[self.currentSquare.x][self.currentSquare.y - 1]
        self.currentSquare.sWall = False
        self.currentSquare.visited = True
        self.turnList.append(self.currentSquare)

    def moveRight(self):
        self.currentSquare.eWall = False
        self.currentSquare = self.grid[self.currentSquare.x - 1][self.currentSquare.y]
        self.currentSquare.wWall = False
        self.currentSquare.visited = True
        self.turnList.append(self.currentSquare)

    def moveDown(self):
        self.currentSquare.wWall = False
        self.currentSquare = self.grid[self.currentSquare.x][self.currentSquare.y - 1]
        self.currentSquare.nWall = False
        self.currentSquare.visited = True
        self.turnList.append(self.currentSquare)

    def backup(self):
        del self.turnList[len(self.turnList) - 1]
        self.currentSquare = self.turnList[len(self.turnList) - 1]

    def allVisited(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].visited:
                    return False
        return True

    def makeMaze(self):
        while not self.allVisited():
            print("making maze check 1")
            print("at coordinates (" + str(self.currentSquare.x)+ ", " + str(self.currentSquare.y) + ")")
            # Making a random path through the squares using a depth-first algorithm
            options = self.availableDirections(self.currentSquare)
            print(options)
            moveFwd = len(options) > 0

            while moveFwd:
                nextSquare = random.choice(options)
                print("moving in direction " + str(nextSquare))
                if nextSquare == 0:  # move left
                    if self.currentSquare.x > 0:
                        if not self.grid[self.currentSquare.x - 1][self.currentSquare.y].visited:
                            self.moveLeft()
                if nextSquare == 1:  # move up
                    if self.currentSquare.y > 0:
                        if not self.grid[self.currentSquare.x][self.currentSquare.y - 1].visited:
                            self.moveUp()
                if nextSquare == 2:  # move right
                    if self.currentSquare.x < self.width - 1:
                        if not self.grid[self.currentSquare.x][self.currentSquare.y + 1].visited:
                            self.moveRight()
                if nextSquare == 3:  # move down
                    if self.currentSquare.y < self.height - 1:
                        if not self.grid[self.currentSquare.x][self.currentSquare.y + 1].visited:
                            self.moveDown()

                # get options for new square
                options = self.availableDirections(self.currentSquare)
                moveFwd = len(options) > 0

            self.backup()

    def makeBloops(self):
        # Fills the maze with points
        infoObject = pygame.display.Info()
        screenwidth = infoObject.current_w
        screenheight = infoObject.current_h
        for x in range(self.width):
            for y in range(self.height):
                self.bloops.append(Bloop(int((x + 0.5) * screenwidth / self.width),
                                         int((y + 1.5) * screenheight / self.height)))


class Wall(object):
    # Maze walls
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Square(object):
    # Blocks that make up the screen in maze mode
    def __init__(self, nWall, eWall, sWall, wWall, x, y, visited):
        self.nWall = nWall
        self.eWall = eWall
        self.sWall = sWall
        self.wWall = wWall
        self.x = x
        self.y = y
        self.visited = visited


class Bloop(object):
    # Point objects in maze mode
    def __init__(self, x, y):
        self.x = x
        self.y = y

