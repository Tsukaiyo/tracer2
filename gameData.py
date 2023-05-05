from gameStates import *
from style import colours
import pygame
from maze import Maze

pygame.init


class GameData(object):
    infoObject = pygame.display.Info()
    width = infoObject.current_w
    height = infoObject.current_h
    currentState = MainMenu
    rockets = []
    team = False
    players = 0
    speed = 5
    winner = 0
    maze = None
    mazeMode = False

    def __init__(self):
        self.team = False
        self.maze = False
        self.currentState = MainMenu
        self.players = 0
        self.keys = 0
        self.startTime = 0
        self.speed = 5
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.rockets = []
        self.winner = 0

    def generateRockets(self):
        # Creates rocket objects
        del self.rockets[:]
        if not self.team:
            self.rockets.append(Rocket(colours["purple"], 1, self.width * 0.25, self.height * 0.25, self.speed, self.width, self.height))
            self.rockets.append(Rocket(colours["teal"], 2, self.width * 0.5, self.height * 0.25,  self.speed, self.width, self.height))
            if self.players >= 3:
                if self.maze:
                    self.rockets.append(Rocket(colours["green"], 3, self.width * 0.25, self.height * 0.75, self.speed, self.width, self.height))
                else:
                    self.rockets.append(Rocket(colours["green"], 3,  self.width * 0.4, self.height * 0.75,  self.speed, self.width, self.height))
            if self.players == 4:
                self.rockets.append(Rocket(colours["pink"], 4, self.width * 0.5, self.height * 0.75,  self.speed, self.width, self.height))
        else:
            self.rockets.append(Rocket(team_colours["green1"], 1, self.width * 0.25, self.height * 0.25,  self.speed, self.width, self.height))
            self.rockets.append(Rocket(team_colours["green2"], 2, self.width * 0.5, self.height * 0.25,  self.speed, self.width, self.height))
            self.rockets.append(Rocket(team_colours["red1"], 3, self.width * 0.25, self.height * 0.75,  self.speed, self.width, self.height))
            self.rockets.append(Rocket(team_colours["red2"], 4, self.width * 0.5, self.height * 0.75,  self.speed, self.width, self.height))

    def clear(self):
        self.team = False
        self.mazeMode = False
        self.players = 0
        self.keys = 0
        self.startTime = 0
        self.rockets = []

    def changeState(self, newState):
        # For any changes that need to be made once when changing states
        if newState == MainMenu:
            self.clear(self)
            self.currentState = MainMenu
        if newState == Instructions:
            self.currentState = Instructions
        if newState == ViewHighScores:
            self.currentState = ViewHighScores
        if newState == ToggleMaze:
            self.currentState = ToggleMaze
        if newState == ToggleTeam:
            self.currentState = ToggleTeam
        if newState == Play:
            self.generateRockets(self)
            self.currentState = Play
        if newState == PlayMaze:
            self.generateRockets(self)
            self.maze = Maze(10, 10)
            self.currentState = PlayMaze
        if newState == End:
            self.currentState = End

        self.currentState.selection = 0
