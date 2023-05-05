from button import Button
from style import colours, team_colours
from rocket import *
import pygame

pygame.init()


class GameState(object):

    buttons = []
    selection = 0
    animatedRockets = []

    def __init__(self, buttons):
        self.selection = 0
        self.buttons = buttons

    def scrollDown(self):
        if self.selection < len(self.buttons) - 1:
            self.selection = self.selection + 1
        else:
            self.selection = 0

    def scrollUp(self):
        if self.selection == 0 or self.selection == -1:
            self.selection = len(self.buttons) - 1
        else:
            self.selection = self.selection - 1


class MainMenu(GameState):

    buttons = [
        Button("2 Players", 60, colours["pink"], 300),
        Button("3 Players", 60, team_colours["red1"], 375),
        Button("4 Players", 60, colours["green"], 450),
        Button("Instructions", 60, colours["teal"], 525),
        Button("High Scores", 60, colours["purple"], 600)]

    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    speed = 8

    animatedRockets = [AniRocket(colours["purple"], 1, screen_width*0.25, screen_height*0.25, speed, screen_width, screen_height),
                       AniRocket(colours["teal"], 2, screen_width*0.5, screen_height*0.25, speed, screen_width, screen_height),
                       AniRocket(colours["green"], 3, screen_width*0.25, screen_height*0.75, speed, screen_width, screen_height),
                       AniRocket(colours["pink"], 4, screen_width*0.5, screen_height*0.75, speed, screen_width, screen_height)]

    def __init__(self):

        super().__init__(self.buttons)
        self.animatedRockets = [AniRocket(colours["purple"], 1, 200, 200, self.speed, self.width, self.height),
                                AniRocket(colours["teal"], 2, 600, 200, self.speed, self.width, self.height),
                                AniRocket(colours["green"], 3, 200, 600, self.speed, self.width, self.height),
                                AniRocket(colours["pink"], 4, 600, 600, self.speed, self.width, self.height)]


class RecordScore(GameState):

    buttons = [
        Button("2 Players", 60, colours["pink"], 300),
        Button("3 Players", 60, team_colours["red1"], 375),
        Button("4 Players", 60, colours["green"], 450),
        Button("Instructions", 60, colours["teal"], 525),
        Button("High Scores", 60, colours["purple"], 600)]

    def __init__(self):
        self.buttons = [
            Button("2 Players", 60, colours["pink"], 300),
            Button("3 Players", 60, team_colours["red1"], 375),
            Button("4 Players", 60, colours["green"], 450),
            Button("Instructions", 60, colours["teal"], 525),
            Button("High Scores", 60, colours["purple"], 600)]
        super().__init__(self.buttons)



class Play(GameState):
    def __init__(self):
        super().__init__([])


class PlayMaze(Play):
    lives = 5
    def __init__(self):
        super().__init__([])
        self.lives = 5


class ToggleMaze(GameState):

    buttons = [Button("Co-op Maze Mode", 75, team_colours["green2"], 400),
               Button("Competitive Mode", 75, team_colours["red1"], 500)]

    def __init__(self):
        self.buttons = [Button("Co-op Maze Mode", 75, team_colours["green2"], 400),
                        Button("Competitive Mode", 75, team_colours["red1"], 500)]
        super().__init__(self.buttons)


class Instructions(GameState):

    buttons = [Button("Main Menu", 60, colours["pink"], 700)]

    def __init__(self):
        self.buttons = [Button("Main Menu", 60, colours["pink"], 700)]
        super().__init__(self.buttons)


class ViewHighScores(GameState):
    buttons = [Button("Main Menu", 60, colours["pink"], 700)]

    def __init__(self):
        self.buttons = [Button("Main Menu", 60, colours["pink"], 700)]
        super().__init__(self.buttons)


class ToggleTeam(GameState):
    buttons = [Button("Play 2 vs 2", 75, team_colours["green1"], 400),
               Button("Play Free for All", 75, team_colours["red1"], 500)]

    def __init__(self):
        self.buttons = [Button("Play 2 vs 2", 75, team_colours["green1"], 400),
                        Button("Play Free for All", 75, team_colours["red1"], 500)]
        super().__init__(self.buttons)


class End(GameState):
    buttons = [Button("Main Menu", 70, colours["teal"], 600), Button("Replay", 70, colours["purple"], 700)]

    def __init__(self):
        self.buttons = [Button("Main Menu", 70, colours["teal"], 600),
                        Button("Replay", 70, colours["purple"], 700)]
        super().__init__(self.buttons)


class EndMaze(End):

    def __init__(self):
        super().__init__(self)
        self.selectedLetter = 0
        self.name = ""

        #nameInfo = playerNameInput(name, selectedLetter)
        #name = nameInfo[0]
        #selectedLetter = nameInfo[1]
        #if selectedLetter == 3:
        #    gameTime = endTime - startTime
        #    if not scoreWritten:
        #        writeHighScores(points, gameTime, writeName(name))
        #        scoreWritten = True


    def playerNameInput(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.scrollDown()
        elif key[pygame.K_UP]:
            self.scrollUp()
        elif key[pygame.K_SPACE]:
            if self.selectedLetter < 3:
                self.selectedLetter = self.selectedLetter + 1
                self.name = self.name + letters[self.selection]
            # needs an "else" where it exists playerNameInput
