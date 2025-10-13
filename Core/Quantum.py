from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import math

class QuantumMechanics:
    def __init__(self):
        self.simulator = AerSimulator()

    def _run_circuit(self, qbits):
        """
            A function that "flips a Quantum coin" using a Hadamard Gate to
            set a qubit into superposition and have it get measured so it
            collapses into a 1 or 0 giving the Cell a 50/50 chance of living.

            Variables:
                qc
                simulator        : The simulator to run the circuit.
                compiled_circuit : The compiled quantum circuit
                job              : The running job of the circuit.
                result           : The result of that job.
                bits             : The order of the bits chosen.
                bitMatrix        : The matrix of the bits for easy setting.
                row              : The row of bits to add to the bitMatrix.
                bit              : The bit to add to the row.

            Returns:
                A bit matrix deciding the initial state of the Cells.
        """
        
        qc = QuantumCircuit(qbits, qbits)
        qc.h(range(qbits))
        qc.measure(range(qbits), range(qbits))

        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1, memory=True)
        result = job.result()

        return result.get_memory()[0]

    def q_choice(self, options):
        choices = len(options)

        if choices == 0:
            raise ValueError("Choices can not be empty!")

        qbits = math.ceil(math.log2(choices))

        result = self._run_circuit(qbits)
        
        return options[int(result)%choices]

    def q_flip(self, amount=1):
        maxQbits = 29
        bits = []

        while amount > 0:
            batchSize = min(amount, maxQbits)

            result = self._run_circuit(batchSize)
            bits.extend([int(bit) for bit in result])
            amount -= batchSize


        if len(bits) == 1:
            return int(bits[0])
        else:
            return bits

    def q_randint(self, end, start=0):
        if start > end:
            start, end = end, start

        options = end-start+1
        qbits = math.ceil(math.log2(options))
        result = self._run_circuit(qbits)

        return start + int(result)%options