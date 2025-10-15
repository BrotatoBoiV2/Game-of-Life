"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Game of Life.
Description: A recreation of Conway's Game of Life using Quantum Computing for
                        more natural randomness.
                              File: world.py
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


# ~ Standard libraries. ~ #
from threading import Thread
import os
import time
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import Queue

# ~ Third-party libraries. ~ #
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from colorama import Fore, Style, init

# ~ Custom modules. ~ #
from Core import Quantum as q


# ~ Initialize GLOBAL Variables. ~ #
PATTERNS = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "block": [(0, 0), (1, 0), (0, 1), (1, 1)]
}

# ~ Initialize colorama with color reset. ~ #
init(autoreset=True)


class Cell:
    """
        ~ Handles the state and rendering of a Cell. ~

        Methods:
            __init__  : Initialize the Cell.
            render    : Render the Cell with color.
    """

    def __init__(self, x, y, state=None):
        """
            ~ Initialize the Cell and its variables. ~

            Arguments:
                x (int)            : The X coordinate of the Cell.
                y (int)            : The Y coordinate of the Cell.
                state (int | None) : The state of the cell.
                                    (1 = Alive, 0 = Dead; Default: None)

            Attributes:
                pos (tuple): Position (x, y) of the cell.
                state (int) : The state of the Cell.
        """

        self.pos = (x, y)
        self.state = state

    def render(self):
        """
            ~ Render the Cell with color and character. ~

            Returns:
                (str) : Colored character representation of the cell.
        """

        if self.state:
            color = Fore.MAGENTA
            char = "█"
        else:
            color = Fore.RED
            char = "."

        return f"{color}{char}"

    
class World:
    """
        ~ Handles the world grid, cell states and updates. ~

        Methods:
            __init__       : Initialize the world.
            init_states    : Initialize cell states.
            pattern_select : Thread to select and queue patterns.
            render         : Render the world.
            seed_pattern   : Seed a pattern into the world.
            check_cells    : Return neighbors of a cell.
            update         : Update world with double-buffering.
    """

    def __init__(self, width=10, height=10):
        """
            ~ Initialize the world. ~

            Arguments:
                width (int)  : Width of the world. (Default: 10)
                height (int) : Height of the world. (Default: 10)

            Variables:
                qm (obj)             : Quantum mechanics handler.
                width (int)          : Width of the world.
                height (int)         : Height of the world.
                states (int)         : Initialized states of the cells.
                is_loaded (bool)     : Whether the world finished loading.
                cells (2D Matrix)    : Matrix of cell objects.
                new_cells (2D Matrix) : Matrix for double-buffering.
                q (obj)              : Queue holding patterns to seed.
        """

        self.qm = q.QuantumMechanics()
        self.width = width
        self.height = height

        self.states = [[0]*self.width for _ in range(self.height)]
        self.is_loaded = False

        # ~ Initialize cell states in the background. ~ #
        Thread(target=self.init_states, daemon=True).start()

        # ~ Loading animation. ~ #
        while not self.is_loaded:
            os.system("clear")

            for y in range(self.height):
                row = "".join("█" if cell else "." for cell in self.states[y])
                print(row)
                
            time.sleep(0.1)

        # ~ Initialize cell objects and buffers. ~ #
        self.cells = [[Cell(x, y, self.states[y][x]) for x in range(width)]
                        for y in range(height)]
        self.new_cells = [[Cell(x, y, 0) for x in range(width)] 
                        for y in range(height)]
        self.q = Queue()

        Thread(target=self.pattern_select, daemon=True).start()

    def init_states(self, chunk=10):
        """
            ~ Initialize cell states in chunks using threads. ~
            
            Arguments:
                chunk : Number of rows per thread. (Default: 10)
        """
        
        cells = self.width*self.height
        self.states = [[0]*self.width for _ in range(self.height)]
        
        def worker(start):
            """
                ~ Worker thread to initialize a chunk of rows. ~

                Arguments:
                    start : Start index of rows for this chunk.
            """

            end = min(start+chunk, self.height)
            for y in range(start, end):
                bits = self.qm.q_flip(self.width)
                self.states[y] = bits

            print(f"Initialized rows {start+1}-{end}/{self.height}")


        threads = []
        for start in range(0, self.height, chunk):
            t = Thread(target=worker, args=(start,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.is_loaded = True

        print("World state initialized!")

    def pattern_select(self):
        """
            ~ Randomly select and queue patterns for the world. ~

            ~ Patterns are biased by weight. ~
        """

        weights = [5, 1, 1]
        while True:
            pattern = self.qm.q_choice(list(PATTERNS.keys()), weights)
            pattern = PATTERNS[pattern]
            x = self.qm.q_randint(self.width-1, 0)
            y = self.qm.q_randint(self.height-1, 0)

            self.q.put((pattern, x, y))

    def render(self):
        """ ~ Render the world to the screen. ~ """

        output = ""

        for y in range(self.height):
            for x in range(self.width):
                output += self.cells[y][x].render()

            output += "\n"

        print(output)

    def seed_pattern(self, pattern, top_left_x, top_left_y):
        """
            ~ Seed a pattern into the world at a specific location. ~

            Arguments:
                pattern (array)  : Positions of the patterns body.
                top_left_x (int) : Patterns top left position of X.
                top_left_y (int) : Patterns top left position of Y.
        """

        for pos in pattern:
            x = (top_left_x+pos[0])%self.width
            y = (top_left_y+pos[1])%self.height

            self.cells[y][x].state = 1

    def check_cells(self, cell):
        """
            ~ Return all neighbors of a cell. ~

            Arguments:
                cell (obj) : The cell to check the neighbors of.

            Returns:
                (array) : All of the cells neighbors.
        """

        neighbors = []
        x, y = cell.pos
        pos = (-1, 0, 1)

        for pos_y in pos:
            for pos_x in pos:
                if pos_x == 0 and pos_y == 0:
                    continue

                neigh_x, neigh_y = (x+pos_x)%self.width, (y+pos_y)%self.height

                if 0 <= neigh_x < self.width and 0 <= neigh_y < self.height:
                    neighbors.append(self.cells[neigh_y][neigh_x])

        return neighbors

    def update(self):
        """ ~ Update the world with a double-buffer and seeded patterns. ~ """

        # ~ Seed patterns from the queue. ~ #
        while not self.q.empty():
            pattern, x, y = self.q.get()

            self.seed_pattern(pattern, x, y)

        # ~ Update cell states based on neighbors. ~ #
        for y in range(self.height):
            for x in  range(self.width):
                cell = self.cells[y][x]
                live = sum(1 for c in self.check_cells(cell) if c.state)
                new_state = cell.state

                if cell.state and (live < 2 or live > 3):
                        new_state = 0
                elif not cell.state and live == 3:
                        new_state = 1

                self.new_cells[y][x].state = new_state
        
        self.cells, self.new_cells = self.new_cells, self.cells

