### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~ Programmer: Aaron "A.J." Cassell. (@BrotatoBoi) ~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Program Name: Game of Life. ~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~ Description: A recreation of Conway's Game of Life using ~~~~~~ ###
### ~~~~~~~ Quantum Computing for selection of the state of the Cell. ~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ File: GUI.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~ Date: 2025/10/09 ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~ Version: 2.3-2025.10.13 ~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Copyright (C) 2025 BrotatoBoi ~~~~~~~~~~~~~~~~~~ ###
### ~~~~ This program is free software: you can redistribute it and/or ~~~~ ###
### ~~ it under the terms of the GNU General Public License as published ~~ ###
### ~~~~ by: The Free Software Foundation, either the version 3 of the ~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~ License, or any later version. ~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###


import pygame as pg


class Window:
    def __init__(self, size, main, color=(0, 0, 0)):
        pg.init()

        info = pg.display.Info()

        self.width = info.current_w
        self.height = info.current_h
        self.main = main
        self.cellSize = (self.width//size[0], self.height//size[1])
        print(self.cellSize)
        exit
        self.color = color
        self.screen = pg.display.set_mode((self.width, self.height))

    def handle_events(self):
        for event in pg.event.get():
            ESCAPED = (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
            if event.type == pg.QUIT or ESCAPED:
                self.main.kill()

    def render(self, world):
        self.screen.fill(self.color)

        for y in range(world.height):
            for x in range(world.width):
                if world.cells[y][x].state:
                    color = (255, 105, 180)
                else:
                    color = (255, 0, 0)

                pos = (x*self.cellSize[0], y*self.cellSize[1])
                size = (self.cellSize[0], self.cellSize[1])

                rect = pg.Rect(pos[0], pos[1], size[0], size[1])
                pg.draw.rect(self.screen, color, rect)
            
        pg.display.flip()

