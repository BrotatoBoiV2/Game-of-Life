### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~ Programmer: Aaron "A.J." Cassell. (@BrotatoBoi) ~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Program Name: Game of Life. ~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~ Description: A recreation of Conway's Game of Life using ~~~~~~ ###
### ~~~~~~~ Quantum Computing for selection of the state of the Cell. ~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ File: Main.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
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


# ~ Import Needed Libraries. ~ #
import time, os, random

# ~ Import custom Modules. ~ #
from Core import World as w
from Core import GUI


# ~ Handle the main program loop. ~ #
class Main:
    """
        This class handles the entire main loop of the program.

        Functions:
            __init__    : Initialize the main loop.
            add_pattern : Add a pattern to the world.
            execute     : Execute the main loop.
    """

    def __init__(self, renderType='text'):
        """
            Initialize all of the programs variables.

            Variables:
                self.world        : The object for the world class.
                self._isRunning   :  Boolean to check the state of the program.
        """

        termSize = os.get_terminal_size()
        self.width, self.height = (termSize.columns, termSize.lines)

        self.renderType = renderType
        self.world = w.World(self.width, self.height)
        self._isRunning = True
        self._guiIsInit = False

    def init_gui(self):
        import pygame as pg
        
        pg.init()
        # Handle this error

        self.window = GUI.Window((self.width, self.height), self)

        self._guiIsInit = True

    def kill(self):
        self._isRunning = False

    def add_pattern(self):
        """
            Add a random pattern to the world.

            Select a random pattern and seed it into the world
              at random locations.

            Variables:
                pattern : The random pattern that was selected.
                x       : The X coordinate of the pattern.
                y       : The Y coordinate of the pattern.
        """

        pattern = PATTERNS[random.choice(list(PATTERNS.keys()))]

        x = random.randint(0, self.world.width)
        y = random.randint(0, self.world.height)

        self.world.seed_pattern(pattern, x, y)

    def render_text(self):
        self.world.render()
        self.world.update()

        # time.sleep(1)
        os.system('clear')

    def render_gui(self):
        self.window.render(self.world)
        self.window.handle_events()
        self.world.update()

    def execute(self):
        """
            Execution of the main game loop.

            Keep adding patterns so the world stays alive.
            Render and Update the world.
        """

        while self._isRunning:
            if self.world.isLoaded:
                if self.renderType == "text":
                    self.render_text()
                elif self.renderType == "gui":
                    if not self._guiIsInit:
                        self.init_gui()
                    self.render_gui()


# ~ Check if this is the main program. ~ #
if __name__ == '__main__':
    print("""
            Welcome to The Game of Life: Quantum Edition!
            How do you want it to be rendered?
                1) Text-Based
                2) Graphical G.U.I""")
    
    attempts = 3

    while attempts > 0:
        render = input(">>> ")

        if render[0] in ["1", "T", "t"]:
            main = Main("text")
            break
        elif render[0] in ["2", "G", "g"]:
            main = Main("gui")
            break
        else:
            print("Sorry, I did not get that!")

            attempts -= 1

            print(f"You now have {attempts} more times to answer correctly!")

    if attempts == 0:
        # Kill program, or set to text as default.
        exit()

    try:
        main.execute()
    except KeyboardInterrupt:
        print("Ctrl+C pressed!")
