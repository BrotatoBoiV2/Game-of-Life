### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~ Programmer: Aaron "A.J." Cassell. (@BrotatoBoi) ~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Program Name: Game of Life. ~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~ Description: A recreation of Conway's Game of Life using ~~~~~~~~ ###
### ~~~~~~~~~ Quantum Computing for selection of the state of the Cell. ~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ File: World.py ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Date: 2025/10/09 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~ Version: 2.1-2025.10.12 ~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~ Copyright (C) 2025 BrotatoBoi ~~~~~~~~~~~~~~~~~~~~~ ###
### ~ This program is free software: you can redistribute it and/or modify ~~~ ###
### ~ it under the terms of the GNU General Public License as  published by: ~ ###
### ~ the Free Software Foundation, either the version 3 of the License, or ~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~ any later version. ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###


# ~ Import needed libraries. ~ #
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from threading import Thread
from queue import Queue

# ~ Import custom Modules. ~ #
# from Core import Cell
from Core import Quantum as q


# ~ Initialize GLOBAL Variables. ~ #
PATTERNS = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "block": [(0, 0), (1, 0), (0, 1), (1, 1)]
}


import random
from colorama import Fore, Style, init

# ~ Initialize colorama with color reset. ~ #
init(autoreset=True)


# ~ Handles a Cell. ~ #
class Cell:
    """
        Handles the functions of the Cell.

        Functions:
            __init__  : Initialize the Cell.
            set_state : Returns a 50/50 chance using a Quantum Hadamard Gate.
            render    : Render the Cell.
    """

    def __init__(self, x, y, state=None):
        """
            Initialize the Cell and its variables.

            Arguments:
                x     : The X coordinate of the Cell.
                y     : The Y coordinate of the Cell.
                state : The state of the Cell. (for double-buffered matrix)

            Variables:
                self.pos   : The position of the Cell in the world.
                self.state : The state of the Cell. (1 = Alive, 0 = Dead)
        """

        self.pos = (x, y)
        self.state = state

    def render(self):
        """
            Render the Cell with its color to the screen.

            Variables:
                color : The color based on the state of the Cell.
                char  : The character to display based on the state of the Cell.
        """

        if self.state:
            color = Fore.MAGENTA
            char = "█"
        else:
            color = Fore.RED
            char = "."

        return f"{color}{char}"

# ~ Handles the entire world. ~ #
class World:
    """
        This class handles the world and it's properties.

        Functions:
            __init__        : Initialize the world.
            render          : Render the world.
            seed_pattern    : Seed a pattern into the world.
            check_neighbors : Check the neighbors of each cell.
            update          : Update the world.
    """

    def __init__(self, width=10, height=10):
        """
            Initialize the world.

            Arguments:
                width  : The width of the world. (Default: 10)
                height : The height of the world. (Default: 10)

            Variables:
                self.width    : The width of the world.
                self.height   : The height of the world.
                self.cells    : The matrix for the entire world.
                self.newCells : The matrix for double-buffering the world.
        """

        self.qm = q.QuantumMechanics()
        self.width = width
        self.height = height
        self.isLoaded = False
        self.cells = [[Cell(x, y, 0) for x in range(self.width)] for y in range(self.height)]
        self.newCells = [[Cell(x, y, 0) for x in range(self.width)] for y in range(self.height)]
        self.q = Queue()

        for _ in range(6):
            for pattern in PATTERNS:
                x = self.qm.q_randint(self.width)
                y = self.qm.q_randint(self.height)
                self.seed_pattern(PATTERNS[pattern], x, y)

        Thread(target=self.pattern_select, daemon=True).start()

    def pattern_select(self):
        while True:
            pattern = PATTERNS[self.qm.q_choice(list(PATTERNS.keys()))]
            x = self.qm.q_randint(self.width-1, 0)
            y = self.qm.q_randint(self.height-1, 0)

            self.q.put((pattern, x, y))

    def render(self):
        """
            Render the cells in the world.
        """

        world = ""

        for y in range(self.height):
            for x in range(self.width):
                world += self.cells[y][x].render()

            world += "\n"

        print(world)

    def seed_pattern(self, pattern, topLeftX, topLeftY):
        """
            Seed a pattern into the world.

            Arguments:
                pattern  : The pattern to seed into the world.
                topLeftX : The X coordinate for the pattern.
                topLeftY : The Y coordinate of the pattern.

            Variables:
                pos : Each coordinate in the pattern.
                x   : The X coordinate of the position.
                y   : The Y coordinate of the position.
        """

        for pos in pattern:
            x = (topLeftX+pos[0])%self.width
            y = (topLeftY+pos[1])%self.height

            self.cells[y][x].state = 1

    def check_neighbors(self, cell):
        """
            Check all of the neighbors of a cell.

            Arguments:
                cell : The cell to check the neighbors of.

            Variables:
                neighbors : All of the found neighbors
                x         : The X coordinate of the cell.
                y         : The Y coordinate of the cell.
                pos       : The positions to check for neighbors.
                posY      : The Y position of the neighbor.
                posX      : The X position of the neighbor.
                neighX    : The X coordinate of the neighbor.
                neighY    : The Y coordinate of the neighbor.

            Returns:
                The value of the variable neighbors
        """

        neighbors = []
        x, y = cell.pos
        pos = (-1, 0, 1)

        for posY in pos:
            for posX in pos:
                if posX == 0 and posY == 0:
                    continue

                neighX, neighY = (x+posX)%self.width, (y+posY)%self.height

                if 0 <= neighX < self.width and 0 <= neighY < self.height:
                    neighbors.append(self.cells[neighY][neighX])

        return neighbors

    def update(self):
        """
            Update the cells in the world with a double-buffer.

            Variables:
                y         : The Y index of the cells in the world.
                x         : The X index of the cells in the world.
                cell      : The cell to check surrounding neighbors.
                liveCells : The amount of alive neighboring cells.
                newState  : The new state of the cell.
        """

        while not self.q.empty():
            pattern, x, y = self.q.get()

            self.seed_pattern(pattern, x, y)

        for y in range(self.height):
            for x in  range(self.width):
                cell = self.cells[y][x]
                liveCells = sum(1 for neighbor in self.check_neighbors(cell) if neighbor.state)
                newState = cell.state

                if cell.state and (liveCells < 2 or liveCells > 3):
                        newState = 0
                elif not cell.state and liveCells == 3:
                        newState = 1

                self.newCells[y][x].state = newState
        
        self.cells, self.newCells = self.newCells, self.cells

