"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Game of Life.
Description: A recreation of Conway's Game of Life using Quantum Computing for
                        more natural randomness.
                              File: main.py
                            Date: 2025/10/09
                        Version: 2.5-2025.10.14

===============================================================================

                        Copyright (C) 2025 BrotatoBoi 
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as published
        by the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.

        You should have received a copy of the GNU Affero General Public License
        along with this program. If not, see <https://www.gnu.org/licenses/>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# ~ Standard libraries. ~ #
import time
import os

# ~ Custom modules. ~ #
from core import world
from core import gui


class Main:
    """
        ~ Handles the main loop of the Game of Life program. ~

        Methods:
            __init__    : Initialize the main loop.
            init_gui    : Initialize the graphical GUI Window.
            kill        : Stop the main loop.
            render_text : Render simulation as a text-based terminal display.
            render_gui  : Render simulation as a pygame GUI
            execute     : Execute the main loop.
    """

    def __init__(self, render_type='text'):
        """
            ~ Initialize program variables. ~

            Arguments:
                render_type (str) : Determines how the program will be rendered
                                    (Default is 'text')
        
            Attributes:
                width (int)      : Terminal width in columns.
                height (int)     : Terminal height in lines.
                world (World)    : Instance of the World class.
                _running (bool)  : Tracks if the program is running.
                _gui_init (bool) : Tracks if the GUI has been initialized.
        """

        term_size = os.get_terminal_size()
        self.width, self.height = term_size.columns, term_size.lines

        self.render_type = render_type
        self.world = world.World(self.width, self.height)
        self._running = True
        self._gui_init = False

    def init_gui(self):
        """ ~ Initialize the pygame GUI window. ~ """

        import pygame as pg
        
        pg.init()

        self.window = gui.Window((self.width, self.height), self)
        self._gui_init = True

    def kill(self):
        """ ~ Stop the main loop. ~ """
        self._running = False

    def render_text(self):
        """
            ~ Render the simulation as text in the terminal. ~

            The world is rendered and then updated.
        """

        self.world.render()
        self.world.update()

        os.system('clear')  # ~ Clear the terminal for the next frame. ~ #
        #time.sleep(1)      # ~ Uncomment to slow down text rendering. ~ #

    def render_gui(self):
        """
            ~ Render the simulation as a graphical pygame GUI ~

            Handles window rendering, events, and world updates.
        """

        self.window.render(self.world)
        self.window.handle_events()
        self.world.update()

    def execute(self):
        """
            ~ Run the main game loop. ~

            Checks if the world is loaded and renders depending
            on the selected type.

            Initializes the GUI if needed.
        """

        while self._running:
            if self.world.is_loaded:
                if self.render_type == "text":
                    self.render_text()
                elif self.render_type == "gui":
                    if not self._gui_init:
                        self.init_gui()
                    self.render_gui()


if __name__ == '__main__':
    os.system('clear') # TODO: Make a helper function for cross-platform.
    # TODO: Consider adding a menu function  for cleaner input handling.
    print("""
Welcome to The Game of Life: Quantum Edition!
How do you want it to be rendered?
    1) Text-Based
    2) Graphical G.U.I
""")
    
    attempts = 3

    while attempts > 0:
        render = input(">>> ")

        if render and render[0] in ["1", "T", "t"]:
            main = Main("text")
            break
        elif render and render[0] in ["2", "G", "g"]:
            main = Main("gui")
            break
        else:
            print("Sorry, I did not get that!")

            attempts -= 1
            suffix = 's' if attempts != 1 else ''

            print(f"{attempts} more attempt{suffix} to answer correctly!")

    if attempts == 0:
        # ~ Kill program or set default rendering type. ~ #
        exit()

    try:
        main.execute()
    except KeyboardInterrupt:
        print("Ctrl+C pressed!")
