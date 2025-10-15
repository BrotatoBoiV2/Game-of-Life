"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Game of Life.
Description: A recreation of Conway's Game of Life using Quantum Computing for
                        more natural randomness.
                            File: gui.py
                            Date: 2025/10/09
                        Version: 2.5-2025.10.14

===============================================================================

                        Copyright (C) 2025 BrotatoBoi 
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published
        by: The Free Software Foundation, either the version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# ~ Third-party libraries. ~ #
import pygame as pg


# ~ Initialize GLOBAL variables. ~ #
COLOR = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "pink": (255, 105, 180)
}

class Window:
    """
        ~ The window to display the program. ~

        Methods:
            __init__      : Initialize the window.
            handle_events : Handle all of the events that go on.
            render        : Render the cells onto the window.
    """
    
    def __init__(self, size, main, color=(0, 0, 0)):
        """
            ~ Initialize the Window and its variables. ~

            Arguments:
                size (tuple)  : The size of the terminal.
                main (obj)    : The instance of Main()
                color (tuple) : The background color. (Default: (0, 0, 0))

            Attributes:
                width (int)       : The width of the screen.
                height (int)      : The height of the screen.
                main (obj)        : The instance of Main().
                cell_size (tuple) : Width and Height of the cells.
                color (tuple)     : Background color of the Window.
                screen (obj)      : Screen to render the cells to.
        """
        
        pg.init()

        info = pg.display.Info()

        self.width = info.current_w
        self.height = info.current_h
        self.main = main
        self.cell_size = (self.width//size[0], self.height//size[1])
        self.color = color
        pos = (self.width, self.height)
        self.screen = pg.display.set_mode(pos, pg.FULLSCREEN)
        self.grid_surface = pg.Surface((self.width, self.height))

    def handle_events(self):
        """ ~ Handle each (relevant) event that happens in the window. ~ """

        for event in pg.event.get():
            ESCAPED = (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
            if event.type == pg.QUIT or ESCAPED:
                self.main.kill()

    def render(self, world):
        """
            ~ Render the cells to the window. ~

            Arguments:
                world (obj) : The world object.
        """

        self.grid_surface.fill(self.color)  # ~ Clear previous frame. ~ #

        for y in range(world.height):
            for x in range(world.width):
                cell = world.cells[y][x]

                color = COLOR['pink'] if cell.state else COLOR['red']

                pos = (x * self.cell_size[0], y * self.cell_size[1])
                size = (self.cell_size[0], self.cell_size[1])
                rect = pg.Rect(pos, size)
                pg.draw.rect(self.grid_surface, color, rect)

        # ~ Copy the surface to the screen. ~ #
        self.screen.blit(self.grid_surface, (0, 0))
        pg.display.flip()

            
