"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Game of Life.
Description: A recreation of Conway's Game of Life using Quantum Computing for
                        more natural randomness.
                            File: quantum.py
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
import math

# ~ Third-party libraries. ~ #
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class QuantumMechanics:
    """
        ~ Handles Quantum Computing functions for behavior
          approximating true randomness. ~

        Methods:
            __init__       : Initialize the Mechanics System.
            _run_circuit   : Private method to run simulated circuit.
            q_choice       : Select a choice from a list.
            q_flip         : Simulate a coin flip.
            q_randint      : Get a random number in a range.
    """

    def __init__(self):
        """
            ~ Initialize the Quantum System and needed variables. ~

            Attributes:
                simulator : The Simulator to run a Q-Circuit.
        """

        self.simulator = AerSimulator()

    def _run_circuit(self, qbits):
        """
            ~ Measures the qubits placed in superposition using Hadamard gates,
              collapsing them into a 1 or 0 to simulate a 50/50 quantum outcome. ~

            Arguments:
                qbits (int) : How many qubits to process.

            Returns:
                (str) : Bitstring result of measured qubits.
        """
        
        qc = QuantumCircuit(qbits, qbits)
        qc.h(range(qbits))
        qc.measure(range(qbits), range(qbits))

        compiled = transpile(qc, self.simulator)
        job = self.simulator.run(compiled, shots=1, memory=True)
        result = job.result()

        return result.get_memory()[0]

    def q_choice(self, options, weights=None):
        """
            ~ Select a random choice from an array using
              quantum-generated randomness. ~

            Arguments:
                options (list | tuple) : The array of options to choose from.
                weights (list | tuple) : Optional bias weights for weighted selection.

            Returns:
                (any) : A single item from the input array.
        """

        choices = len(options)

        if choices == 0:
            raise ValueError("Choices cannot be empty!")

        if weights is None:
            weights = [1]*choices
        elif len(weights) > choices:
            raise ValueError("Cannot be more weights than choices!")

        total = sum(weights)
        cum_weights = []
        cum_sum = 0

        for weight in weights:
            cum_sum += weight
            cum_weights.append(cum_sum)

        qbits = math.ceil(math.log2(choices))

        result = int(self._run_circuit(qbits), 2)%total
        
        for i, cum in enumerate(cum_weights):
            if result < cum:
                return options[i]
                

    def q_flip(self, amount=1):
        """
            ~ Flip one or more qubits to get a 50/50 random outcome. ~

            Arguments:
                amount (int) : Number of bits to flip. (Default: 1)

            Returns:
                (int | list[int]) : A single bit or list of bits,
                                    depending on amount.
        """

        max_qbits = 29
        bits = []

        while amount > 0:
            batch_size = min(amount, max_qbits)

            result = self._run_circuit(batch_size)
            bits.extend([int(bit) for bit in result])
            amount -= batch_size

        return bits[0] if len(bits) == 1 else bits

    def q_randint(self, end, start=0):
        """
            ~ Randomly select an integer within a specified range using
              quantum randomness. ~

            Arguments:
                end (int)   : The inclusive end of the range.
                start (int) : The start of the range. (Default: 0)

            Returns:
                (int) : A random integer between start and end, inclusive.
        """

        if start > end:
            start, end = end, start

        options = end-start+1
        qbits = math.ceil(math.log2(options))
        result = self._run_circuit(qbits)

        return start + int(result)%options
