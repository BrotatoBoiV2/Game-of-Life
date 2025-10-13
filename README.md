# The Game of Life: Quantum Edition.
A recreation of Conway's Game of Life that utilizes quantum randomness to determine each cell's initial state!

# Requirements:
  * python==3.13.7
  * qiskit==2.2.1
  * qiskit-aer==0.17.2
  * colorama==0.4.6

# Installation:
  In the project file run the following commands:

  ```
    python3 -m venv ./venv
    . ./venv/bin/activate
    pip install -r requirements.txt
  ```


# This project demonstrates:
  * Quantum-based randomness for cell initialization using Qiskit and AerSimulator.
  * A double-buffered, terminal-rendered Game of Life that ensures smooth updates.
  * Edge wrapping (toroidal grid) for infinite-looping patterns.
  * Additional seeding of classic patterns (gliders, blinkers, blocks, more to come) to explore dynamic behaviors.
  * Colored terminal visualization for clear alive/dead cell distinction.

# Features:
  * Randomized initial states using quantum circuits.
  * Double-buffered update system for accurate neighbor calculation.
  * Support for oscillators, gliders, and still lifes.
  * Toroidal grid wrapping to prevent edge stagnation.
  * Extensible for custom patterns or "immortal" cells.

Why Quantum Randomness Instead of Classical?
    I figured it would be interesting to rewrite an old project with a newer concept! Each cell uses a single-qubit Hadamard gate to determine its initial state (alive or dead). This introduces true quantum randomness rather than relying on classical pseudorandom generators.

To see project updates check the [CHANGELOG](Docs/CHANGELOG.md)

# License
This project is under the **GNU General Public License v3.0 (GPLv3)**. to see more visit the [LICENSE](LICENSE.md)