2025/10/09  - Created the Cell and World classes.
            ~ Started to re-write the program.

            ~ Created the Cell class.
                ~ Sets its state by putting a qubit into superposition then
                    measuring it.
                ~ Renders the cell with its color.
 
            ~ World was created.
                ~ Updates each cell appropriately for the next generation
                    of the world.
                ~ Checks each cell's neighbor for the state updating.
                ~ Allows for adding patterns into the world.
                ~ Renders each cell properly.
                ~ Has toroidal wrapping around the world.

            *** Initial version; 1.0-2025.10.09 ***

2025/10/10 - Program optimization and automatic fullscreen. 
            ~ Optimized entire program.
                ~ Quicker initial states.
                ~ Renders entire "world" instead of each line.
                ~ World now handles quantum logic instead of the Cell itself.

            ~ Incorporated automatic terminal fill display.

            *** Minor update to version; 1.3-2025.10.10 ***

2025/10/13 - Created menu, made Cell and World into one file,
                GUI option, weights and live loading.
            ~ Created initial menu for selecting the rendering type.
                ~ Allows for text-based rendering.
                ~ Starting work on GUI rendering.
                ~ Allows for three attempts to get user input.
                ~ Currently exits if proper user input was not given. 
                    (Maybe set to text-based as default)

            ~ Fused Cell class into World.py and removed the original file.

            ~ GUI option has been added, and it works as intended.
                ~ The cell sizes are programmatically set for the screen.

            ~ Added weights to quantum choices.
                ~ Gliders now get chosen 5x more often than other patterns.

            ~ Added live loading function so you can see what is happening
                instead of wondering if it has crashed.

            * Increase frequency of pattern seeding.
            * Add patterns like different positioned gliders to be seeded.
            * Implement a save function to avoid re-initialization on launch.
            * Add command-line argument support for menu bypass.
            * Allow for manual pattern seeding.

            ** Clean the code and add comments/docstrings.

            *** Updated to version; 2.4-2025.10.13 ***

2025/10/14 - Code cleanup.
            ~ Some code cleanup with A.I. assistance.

            *** Updated to version; 2.5-2025.10.14 ***
