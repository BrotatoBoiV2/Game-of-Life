2025/10/09 - Started to re-write the program.

            - Created the Cell class.
                - Sets its state by putting a qubit into superposition then
                     measuring it.
                - Renders the cell with its color.
 
            - World was created.
                - Updates each cell appropriately for the next generation
                     of the world.
                - Checks each cells neighbor for the state updating.
                - Allows for adding patterns into the world.
                - Renders each cell properly.
                - Has toroidal wrapping around the world.

            *** Initial version; 1.0-2025.10.09 ***

2025/10/10 - Optimized entire program.
                - Quicker initial states.
                - Renders entire "world" instead of each line.
                - World now handles quantum logic instead of the Cell itself.

            - Incorporated automatic terminal fill display.

            *** Minor update to version; 1.3-2025.10.10 ***

2025/10/13 - Created initial menu for selecting the rendering type.
                - Allows for text-based rendering.
                - Starting work on G.U.I. rendering.
                - Allows for three attempts to get user input.
                - Currently exits if proper user input was  not given. 
                    (Maybe set to text-based as default)

            - Cell class fused with 'World.py'  and removed - Rename file to   
                represent the classification better.

            - G.U.I. option has been added, and it works as intended.
                - The cell sizes are programmatically set for the screen.

            - Added weights to quantum choices.
                - Gliders now get chosen 5x more often than other patterns.

            - Added live loading function so you can see what is happening
                instead of wondering if it has crashed.

            * Make seed patterns more often.
            * Add more patterns like different positioned gliders, etc.
            * Implement a save function so it does not need
                to be re-initialized each launch.

            ** Clean the code and add comments/docstrings.

            *** Updated to version; 2.5-2025.10.13 ***
