'''
"Tracer"
Author: Maeve Fitzgerald
A remake of my game Tracer (2019) for playability on the CAT6 table, which requires full-screen and only uses keyboard input
Lots of code cleanup done in the update.
'''

import pygame
import math
from gameStates import *
from style import *
from gameData import GameData
from maze import *

# Initializations
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Setup
height = 800
width = 800

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Tracer")
done = False
clock = pygame.time.Clock()

# Colours - temp, remove later since this should only be used in gameStates
BLUE = colours["blue"]
TEAL = colours["teal"]
PURPLE = colours["purple"]
GREEN = colours["green"]
PINK = colours["pink"]
WHITE = colours["white"]
YELLOW = colours["yellow"]
GREEN1 = team_colours["green1"]
GREEN2 = team_colours["green2"]
RED1 = team_colours["red1"]
RED2 = team_colours["red2"]

# Basic variables
turnList = []
currentSquare = 0
size = 10
grid = 0

buttonsMade = False
scoreWritten = False
points = 0

# Game-timing variables
endOfRound = False
timeRecording = True


def animation():
    for rocket in data.currentState.animatedRockets:
        rocket.move()


def keyControls(rocket, left, right, up, down):
    if rocket.timeOfDeath < time.time() - 1:
        # keys = pygame.key.get_pressed()
        if data.keys[left]:
            rocket.moveLeft()
        if data.keys[right]:
            rocket.moveRight()
        if data.keys[up]:
            rocket.moveUp()
        if data.keys[down]:
            rocket.moveDown()


def moveRockets():
    keyControls(data.rockets[0], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
    keyControls(data.rockets[1], pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
    if data.players > 2:
        keyControls(data.rockets[2], pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_g)
    if data.players == 4:
        keyControls(data.rockets[3], pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k)


def checkDotCollision():
    for rocketA in data.rockets:
        for rocketB in data.rockets:
            if rocketA == rocketB:
                continue
            if data.team:
                if (rocketA.playerNum in {1, 2} and rocketB.playerNum in {1, 2}) or \
                   (rocketA.playerNum in {3, 4} and rocketB.playerNum in {3, 4}):
                    continue
            for dot in rocketB.dots:
                if dist(dot, rocketA) < 5:
                    if data.currentState == PlayMaze:
                        rocketA.reset()
                        data.currentState.lives -= 1
                    else:
                        data.winner = rocketB
                        data.changeState(data, End)


def checkWallCollision():
    for x in range(data.maze.width):
        for y in range(data.maze.height):
            for rocket in data.rockets:
                if data.maze.grid[x][y].nWall:
                    if (y * height / size) - 5 < rocket.y < (
                            y * height / size) + 5 > rocket.x > x * width / size:
                        rocket.lose()
                if data.maze.grid[x][y].eWall:
                    if ((x + 1) * width / size) - 5 < rocket.x < (
                            (x + 1) * width / size) + 5 > rocket.y > y * height / size:
                        rocket.lose()
                if data.maze.grid[x][y].sWall:
                    if ((y + 1) * height / size) - 5 < rocket.y < (
                            (y + 1) * height / size) + 5 > rocket.x > x * width / size:
                        rocket.lose()
                if data.maze.grid[x][y].wWall:
                    if (x * width / size) - 5 < rocket.x < (
                            x * width / size) + 5 > rocket.y > y * height / size:
                        rocket.lose()
                if rocket.y > height - 9:
                    rocket.lose()


# Buttons
def drawButtons():
    # Put the buttons on screen with an arrow pointing to the selected button
    for button in data.currentState.buttons:
        centreText(button.text, button.size, button.colour, button.y)
    if len(data.currentState.buttons) > 0:
        drawButtonPointer()


def drawButtonPointer():
    currentButton = data.currentState.buttons[data.currentState.selection]
    xOffset = len(currentButton.text) * (currentButton.size / 4.5)
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    x = screen_width / 2 - xOffset
    arrowPos = (
        (x - 15,
         currentButton.y),
        (x - 45,
         currentButton.y + 10),
        (x - 45,
         currentButton.y - 10))
    pygame.draw.polygon(screen, WHITE, arrowPos)


def buttonSound():
    pygame.mixer.music.load('button.mp3')
    pygame.mixer.music.play()


def playMusic():
    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.play(-1)


# Text
def text(words, font, size, colour, x, y):
    # create text
    myfont = pygame.font.SysFont(font, size)
    textA = myfont.render(words, False, colour)
    screen.blit(textA, (x, y))


def centreText(words, size, colour, y):
    # create centred text
    myfont = pygame.font.SysFont('impact', size)
    textA = myfont.render(words, False, colour)
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    text_rect = textA.get_rect(center=(screen_width / 2, y))
    screen.blit(textA, text_rect)


def titleText(words, size, y):
    # create centred text
    myfont = pygame.font.SysFont('impact', size)
    textA = myfont.render(words, False, colours["purple"])
    textB = myfont.render(words, False, colours["teal"])
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    text_rectA = textA.get_rect(center=(screen_width / 2, y))
    text_rectB = textB.get_rect(center=(screen_width / 2 + 10, y + 5))
    screen.blit(textA, text_rectA)
    screen.blit(textB, text_rectB)


# Files
def sortScores(file):
    # sort Scoreboard.txt by score, then by time
    with open(file, "r") as file1:
        f_list = [str(i) for line in file1 for i in line.split('\n') if i.strip()]

    # separate out scores and times
    gameData = []
    scores = []
    times = []
    names = []
    highScoreList = []
    for i in range(len(f_list)):
        gameData.append(f_list[i].split(","))
    for i in range(len(gameData)):
        scores.append(int(gameData[i][0]))
        times.append(float(gameData[i][1]))
        names.append(gameData[i][2])
    while len(scores) > 0:
        # sort by highest scores, then find the lowest times
        highScore = 0
        lowestTime = 2147483647
        highScoreTimes = []
        bestScoreIndex = []

        # get the highest score
        for i in range(len(scores)):
            if scores[i] > highScore:
                highScore = scores[i]

        # get the indices of the highest scores
        for i in range(len(scores)):
            if scores[i] == highScore:
                highScoreTimes.append(times[i])

        # find the lowest time with that scoreS
        for i in range(len(highScoreTimes)):
            if highScoreTimes[i] < lowestTime:
                lowestTime = highScoreTimes[i]

        # Find the index of the best score
        for i in range(len(times)):
            if times[i] == lowestTime and scores[i] == highScore:
                bestScoreIndex.append(i)

        # writing top scores
        counter = 0
        for i in range(len(bestScoreIndex)):
            highScoreList.append(
                str(scores[bestScoreIndex[i] - counter]) + "," + str(times[bestScoreIndex[i] - counter]) + "," + names[
                    bestScoreIndex[i]] + "\n")
            del scores[bestScoreIndex[i] - counter]
            del times[bestScoreIndex[i] - counter]
            del names[bestScoreIndex[i] - counter]
            counter = counter + 1

    f = open("gameFiles/Scoreboard.txt", 'w').close()
    f = open("gameFiles/Scoreboard.txt", "a+")
    for i in range(len(highScoreList)):
        f.write(highScoreList[i])
    f.close()


def writeHighScores(score, gameTime, playerName):
    # Add a new score to the scoreboard
    f = open("gameFiles/Scoreboard.txt", "a+")
    scoreTEXT = str(score) + "," + str(gameTime) + "," + playerName + "\n"
    f.write(scoreTEXT)
    f.close()
    sortScores("gameFiles/Scoreboard.txt")
    # Edited to be CAT6-Compatible
    f = open("gameFiles/tracerAllHighscores.txt", "a+")
    f.write(str(score) + "\n")
    f.close


def printHighScores():
    # Write out the top 7 scores to the screen
    f = open("gameFiles/Scoreboard.txt", "a+")
    with open("gameFiles/Scoreboard.txt", "r") as file1:
        f_list = [str(i) for line in file1 for i in line.split('\n') if i.strip()]
    # seperate out scores and times
    gameData = []
    scores = []
    times = []
    names = []
    colour = 0
    for i in range(len(f_list)):
        gameData.append(f_list[i].split(","))
    for i in range(len(gameData)):
        scores.append(int(gameData[i][0]))
        times.append(float(gameData[i][1]))
        names.append(gameData[i][2])
    numScores = 7
    if len(scores) < 7:
        numScores = len(scores)
    for i in range(numScores):
        mins = int(times[i] / 60)
        secs = int(times[i] % 60)
        secs = str(secs)
        while len(secs) < 2:
            secs = "0" + secs
        txt = str(i + 1) + ". " + names[i] + ": " + str(scores[i]) + " Pts, " + str(mins) + ":" + str(secs)
        if i == 0:
            colour = RED2
        if i == 1:
            colour = RED1
        if i == 2:
            colour = YELLOW
        if i == 3:
            colour = GREEN
        if i == 4:
            colour = GREEN1
        if i == 5:
            colour = TEAL
        if i == 6:
            colour = PURPLE

        centreText(txt, 50, colour, (i * 70) + 250)


def write(words):
    # Append line to a text file
    f = open("Log.txt", "a+")
    f.write(words + "\n")
    f.close()


# Maze
def collectBloops():
    for bloop in data.maze.bloops:
        for rocket in data.rockets:
            if dist(rocket, bloop) < 15 and bloop.visible:
                data.currentState.points = data.currentState.points + 25
                data.maze.bloops.remove(bloop)


def dist(objA, objB):
    # calc distance between two objects
    return math.hypot(objA.x - objB.x, objA.y - objB.y)


def exploding():
    # When a player crashes, animate particles
    rate = 5
    for rocket in data.rockets:
        if rocket.timeOfDeath > time.time() - 1:
            rocket.explosion[0].x = rocket.explosion[0].x + rate
            rocket.explosion[1].x = rocket.explosion[1].x + 0.70714285 * rate
            rocket.explosion[1].y = rocket.explosion[1].y + 0.70714285 * rate
            rocket.explosion[2].y = rocket.explosion[2].y + rate
            rocket.explosion[3].x = rocket.explosion[3].x - 0.70714285 * rate
            rocket.explosion[3].y = rocket.explosion[3].y + 0.70714285 * rate
            rocket.explosion[4].x = rocket.explosion[4].x - 0.70714285 * rate
            rocket.explosion[5].x = rocket.explosion[5].x - 0.70714285 * rate
            rocket.explosion[5].y = rocket.explosion[5].y - 0.70714285 * rate
            rocket.explosion[6].y = rocket.explosion[6].y - rate
            rocket.explosion[7].x = rocket.explosion[7].x + 0.70714285 * rate
            rocket.explosion[7].y = rocket.explosion[7].y - 0.70714285 * rate
        else:
            del rocket.explosion[:]


def drawRockets():
    for rocket in data.rockets:
        if rocket.direction == "up":
            rocketPos = ((rocket.x, rocket.y - 15), (rocket.x - 10, rocket.y + 15), (rocket.x + 10, rocket.y + 15))
        if rocket.direction == "down":
            rocketPos = ((rocket.x, rocket.y + 15), (rocket.x - 10, rocket.y - 15), (rocket.x + 10, rocket.y - 15))
        if rocket.direction == "left":
            rocketPos = ((rocket.x - 15, rocket.y), (rocket.x + 15, rocket.y - 10), (rocket.x + 15, rocket.y + 10))
        if rocket.direction == "right":
            rocketPos = ((rocket.x + 15, rocket.y), (rocket.x - 15, rocket.y - 10), (rocket.x - 15, rocket.y + 10))
        if rocket.timeOfDeath < time.time() - 1:
            pygame.draw.polygon(screen, rocket.colour, rocketPos)
            for dot in rocket.dots:
                dotPos = (dot.x, dot.y)
                pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)


def drawExplosion():
    for rocket in data.rockets:
        for particle in rocket.explosion:
            particlePos = (int(particle.x), int(particle.y))
            pygame.draw.circle(screen, particle.colour, particlePos, 3, 0)


def drawMaze():
    # Walls
    for x in range(data.maze.width):
        for y in range(data.maze.height):
            if y == 0:
                pygame.draw.line(screen, WHITE, (x * width / size, y * height / size),
                                 ((x + 1) * width / size, y * height / size), 2)
                pygame.draw.line(screen, WHITE, (x * width / size, (y + 1) * height / size),
                                 ((x + 1) * width / size, (y + 1) * height / size), 2)
            else:
                if data.maze.grid[x][y].nWall:
                    pygame.draw.line(screen, WHITE, (x * width / size, y * height / size),
                                     ((x + 1) * width / size, y * height / size), 2)
                if data.maze.grid[x][y].eWall:
                    pygame.draw.line(screen, WHITE, ((x + 1) * width / size, y * height / size),
                                     ((x + 1) * width / size, (y + 1) * height / size), 2)
                if data.maze.grid[x][y].sWall:
                    pygame.draw.line(screen, WHITE, (x * width / size, (y + 1) * height / size),
                                     ((x + 1) * width / size, (y + 1) * height / size), 2)
                if data.maze.grid[x][y].wWall:
                    pygame.draw.line(screen, WHITE, (x * width / size, y * height / size),
                                     (x * width / size, (y + 1) * height / size), 2)
    # Bloops
    for bloop in data.maze.bloops:
        pygame.draw.circle(screen, WHITE, (bloop.x, bloop.y), 8, 0)


def drawMazeInfo():
    timeLimit = 300 / data.players
    gameTime = time.time() - data.startTime
    timeRemaining = timeLimit - gameTime
    minsLeft = int(timeRemaining / 60)
    secsLeft = str(int(timeRemaining % 60))
    text("Points: " + str(points), 'impact', 40, WHITE, 80, 20)
    text("Lives: " + str(data.currentState.lives), 'impact', 40, WHITE, 600, 20)
    if len(secsLeft) == 1:
        secsLeft = "0" + secsLeft
    timeText = "Time Left: " + str(minsLeft) + ":" + secsLeft
    text(timeText, 'impact', 40, RED1, 300, 20)


# Core methods
def render():
    # All the calculations are here
    if data.currentState == MainMenu:
        if data.keys[pygame.K_SPACE]:
            if data.currentState.selection < 3:
                data.players = data.currentState.selection + 2
                if data.players == 4:
                    data.changeState(data, ToggleTeam)
                else:
                    data.changeState(data, Play)
                #data.changeState(data, ToggleMaze)
            elif data.currentState.selection == 3:
                data.changeState(data, Instructions)
            elif data.currentState.selection == 4:
                data.changeState(data, ViewHighScores)
            # buttonSound()
        elif data.keys[pygame.K_UP]:
            data.currentState.scrollUp(data.currentState)
        elif data.keys[pygame.K_DOWN]:
            data.currentState.scrollDown(data.currentState)

    elif data.currentState == Instructions or data.currentState == ViewHighScores:
        if data.keys[pygame.K_SPACE]:
            data.changeState(data, MainMenu)

    elif data.currentState == ToggleMaze:
        if data.keys[pygame.K_SPACE]:
            data.mazeMode = (data.currentState.selection == 0)
            if not data.mazeMode and data.players == 4:
                data.changeState(data, ToggleTeam)
            elif data.mazeMode:
                data.changeState(data, PlayMaze)
            else:
                data.changeState(data, Play)
            # playMusic()
        elif data.keys[pygame.K_UP]:
            data.currentState.scrollUp(data.currentState)
        elif data.keys[pygame.K_DOWN]:
            data.currentState.scrollDown(data.currentState)

    elif data.currentState == ToggleTeam:  # toggle team mode
        if data.keys[pygame.K_SPACE]:
            data.team = (data.currentState.selection == 0)
            data.changeState(data, Play)
            # playMusic()
        elif data.keys[pygame.K_UP]:
            data.currentState.scrollUp(data.currentState)
        elif data.keys[pygame.K_DOWN]:
            data.currentState.scrollDown(data.currentState)

    elif data.currentState == Play or data.currentState == PlayMaze:
        moveRockets()
        checkDotCollision()
        if data.currentState == PlayMaze:  # main play state, not yet started
            collectBloops()
            checkWallCollision()
            exploding()

            # end of game detection
            gameFinished = (len(data.maze.bloops) == 0)
            if data.currentState.lives <= 0:
                gameFinished = True
                # time up
            timeLimit = 300 / data.players
            gameTime = time.time() - data.startTime
            timeRemaining = timeLimit - gameTime
            if timeRemaining < 0:
                gameFinished = True
            if gameFinished:
                gameState = "End"
                winner = 5
                endOfRound = True
                endTime = time.time()
                scoreWritten = False
                name = [0, 0, 0, 0]
                selectedLetter = 0

    elif data.currentState == RecordScore:  # not yet started
        if maze:
            nameInfo = playerNameInput(name, selectedLetter)
            name = nameInfo[0]
            selectedLetter = nameInfo[1]
            if selectedLetter == 3:
                gameTime = endTime - startTime
                if not scoreWritten:
                    writeHighScores(points, gameTime, writeName(name))
                    scoreWritten = True
                if data.keys[pygame.K_SPACE]:
                    if data.currentState.selection == 0:
                        data.changeState(data, MainMenu)
                    else:
                        data.changeState(data, Play)
        else:
            if data.keys[pygame.K_SPACE]:
                if data.currentState.selection == 0:
                    data.changeState(data, MainMenu)
                else:
                    data.changeState(data, Play)

    elif data.currentState == End or data.currentState == EndMaze:
        if data.keys[pygame.K_SPACE]:
            if data.currentState.selection == 0:
                data.changeState(data, MainMenu)
            else:
                data.changeState(data, Play)
        elif data.keys[pygame.K_UP]:
            data.currentState.scrollUp(data.currentState)
        elif data.keys[pygame.K_DOWN]:
            data.currentState.scrollDown(data.currentState)


def draw():  # Display on screen
    # Putting stuff on the screen
    screen.fill(BLUE)
    drawButtons()
    if data.currentState == MainMenu:
        # animate rockets, draw dots
        animation()
        for aniRocket in data.currentState.animatedRockets:
            if aniRocket.direction == "up":
                rocketPos = ((aniRocket.x, aniRocket.y - 15), (aniRocket.x - 10, aniRocket.y + 15),
                             (aniRocket.x + 10, aniRocket.y + 15))
            if aniRocket.direction == "down":
                rocketPos = ((aniRocket.x, aniRocket.y + 15), (aniRocket.x - 10, aniRocket.y - 15),
                             (aniRocket.x + 10, aniRocket.y - 15))
            if aniRocket.direction == "left":
                rocketPos = ((aniRocket.x - 15, aniRocket.y), (aniRocket.x + 15, aniRocket.y - 10),
                             (aniRocket.x + 15, aniRocket.y + 10))
            if aniRocket.direction == "right":
                rocketPos = ((aniRocket.x + 15, aniRocket.y), (aniRocket.x - 15, aniRocket.y - 10),
                             (aniRocket.x - 15, aniRocket.y + 10))
            pygame.draw.polygon(screen, aniRocket.colour, rocketPos)
            for dot in aniRocket.dots:
                dotPos = (dot.x, dot.y)
                pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)

        titleText("TRACER", 100, 145)
        drawButtons()

    if data.currentState == Instructions:
        titleText("INSTRUCTIONS", 100, 105)
        centreText("As you move your rocket, you leave behind a trail.", 30, GREEN2, 225)
        centreText("You can pass through your own trail, but other", 30, GREEN2, 275)
        centreText("players can't.",30, GREEN2, 325)
        centreText("Competitive mode: Use your trail to cut off another player", 30, RED2,  375)
        centreText("Team mode: You and your teammate can cross each", 30, PURPLE, 425)
        centreText("other's paths. Cut off another team's player to win!", 30, PURPLE, 475)
        centreText("Maze mode: Navigate a maze and collect points.", 30, TEAL, 525)
        centreText("Be careful not to run into walls or other players' paths!", 30, TEAL, 575)
        centreText("You all win when all points are collected", 30, TEAL, 625)

    if data.currentState == ViewHighScores:
        text("HIGH SCORES", 'impact', 100, PURPLE, 125, 75)
        text("HIGH SCORES", 'impact', 100, TEAL, 130, 80)
        printHighScores()

    if data.currentState == ToggleTeam:
        titleText("Team Mode", 100, 245)

    if data.currentState == ToggleMaze:
        titleText("Select Game Mode", 100, 245)

    if data.currentState == Play or data.currentState == PlayMaze:
        drawRockets()
        drawExplosion()
        if data.currentState == PlayMaze:
            drawMaze()
            drawMazeInfo()

    if data.currentState == End:
        drawButtons()
        if not data.team:
            centreText("Player " + str(data.winner.playerNum) + " wins!", 100, data.winner.colour, 350)
        else:
            if data.winner.playerNum == 1 or data.winner.playerNum == 2:
                centreText("Green Team wins!", 90, team_colours["green1"], 300)
            else:
                centreText("Red Team wins!", 90, team_colours["red1"], 300)

    if data.currentState == EndMaze:  # displays endgame text
        if data.lives > 0:
            centreText("YOU WIN!", 70, colours["teal"], 150)
        else:
            centreText("GAME OVER", 70, team_colours["red1"], 150)

        ###########Not yet done:
        centreText("Your name: " + writeName(name), 80, colour, 350)
        if selectedLetter == 0:
            x = 545
            y = 395
        if selectedLetter == 1:
            x = 590
            y = 395
        if selectedLetter == 2:
            x = 635
            y = 395
        if selectedLetter == 3:
            x = 850
            y = 850
            letterArrowPos = ((x, y - 5), (x - 15, y + 10), (x + 15, y + 10))
            pygame.draw.polygon(screen, WHITE, letterArrowPos)
            if points == 2250:
                centreText("You win!", 100, PURPLE, 250)
                centreText("Your time: " + str(int(gameTime / 60)) + "mins, " + str(int(gameTime % 60)) + " secs", 50,
                           GREEN, 450)
                centreText(str(points) + " Points", 50, PINK, 550)
            else:
                centreText("You lose...", 100, colour, 250)
                centreText("Your time: " + str(int(gameTime / 60)) + "mins, " + str(int(gameTime % 60)) + " secs", 50,
                           colour, 450)
                centreText(str(points) + " Points", 50, colour, 550)


# Ready a new log
# f = open("Log.txt", "a+")
# f = open('Log.txt', 'w').close()

# Main method
data = GameData
while not done:
    if data.currentState == Play:
        clock.tick(120)
    else:
        clock.tick(8)

    # quit if window is closed or q is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    data.keys = pygame.key.get_pressed()
    if data.keys[pygame.K_SPACE]:
        time.sleep(0.3)
    if data.keys[pygame.K_q]:
        done = True

    # update game info
    render()
    draw()

    pygame.display.flip()

pygame.quit()
