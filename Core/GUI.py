### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~ Programmer: Aaron "A.J." Cassell. (@BrotatoBoi) ~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Program Name: Game of Life. ~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~ Description: A recreation of Conway's Game of Life using ~~~~~~~~ ###
### ~~~~~~~~~ Quantum Computing for selection of the state of the Cell. ~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ File: GUI.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Date: 2025/10/09 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~ Version: 1.6-2025.10.12 ~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Copyright (C) 2025 BrotatoBoi ~~~~~~~~~~~~~~~~~~~~~ ###
### ~ This program is free software: you can redistribute it and/or modify ~~~ ###
### ~ it under the terms of the GNU General Public License as  published by: ~ ###
### ~ the Free Software Foundation, either the version 3 of the License, or ~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~ any later version. ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###


import pygame as pg


class Window:
    def __init__(self, main, cellSize, color=(0, 0, 0)):
        pg.init()

        info = pg.display.Info()

        self.width = info.current_w
        self.height = info.current_h
        self.main = main
        self.cellSize = cellSize
        self.color = color
        self.screen = pg.display.set_mode((self.width, self.height))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.main.kill()

    def render(self, world):
        self.screen.fill(self.color)

        for y in range(world.height):
            for x in range(world.width):
                if world.cells[y][x].state:
                    color = (255, 105, 180)
                else:
                    color = (255, 0, 0)

                pos = (x*self.cellSize, y*self.cellSize)
                size = (self.cellSize, self.cellSize)

                rect = pg.Rect(pos[0], pos[1], size[0], size[1])
                pg.draw.rect(self.screen, color, rect)

        # for x in range(0, self.width, self.cellSize):
        #     pg.draw.line(self.screen, (0, 255, 0), (x, 0), (x, self.height), 1)

        # for y in range(0, self.height, self.cellSize):
        #     pg.draw.line(self.screen, (0, 255, 0), (0, y), (self.width, y), 1)
            
        pg.display.flip()

