## The Game of Life: Quantum Edition
A recreation of Conway's Game of Life that utilizes quantum randomness to determine each cell's initial state!

## Current Version: V2.5-2025.10.13

## Requirements:
  * python==3.13.7
  * qiskit==2.2.1
  * qiskit-aer==0.17.2
  * colorama==0.4.6
  * pygame==2.6.1

## Installation:
  In the project file run the following commands:

```bash
python3 -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Quickrun:
```bash
git clone https://github.com/BrotatoBoiV2/Game-of-Life
cd Game-of-Life
python3 main.py
```


## This project demonstrates:
  * Quantum-based randomness for cell initialization using Qiskit and AerSimulator.
  * A double-buffered, terminal-rendered Game of Life that ensures smooth updates.
  * Edge wrapping (toroidal grid) for infinite-looping patterns.
  * Additional seeding of classic patterns (gliders, blinkers, blocks, more to come) to explore dynamic behaviors.
  * Colored terminal visualization for clear alive/dead cell distinction.

## Features:
  * Randomized initial states using quantum circuits.
  * Double-buffered update system for accurate neighbor calculation.
  * Support for oscillators, gliders, and still lifes.
  * Toroidal grid wrapping to prevent edge stagnation.
  * Extensible for custom patterns or "immortal" cells.

## Demo:
Demo video in progress.

## Why Quantum Randomness?
    I figured it would be interesting to rewrite an old project with a newer concept! Each cell uses a single-qubit Hadamard gate to determine its initial state (alive or dead), introducing true quantum randomness rather than relying on classical pseudorandom generators.

## Updates:
To see project updates check the [CHANGELOG](docs/CHANGELOG.md)

## License:
This project is protected under the **GNU General Public License v3.0 (GPLv3)**. To see more, visit the [LICENSE](LICENSE)
