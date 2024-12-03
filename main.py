# Quantum Info Sci Final Project
# Harris Ransom, Gavin Young
# BB84 Quantum Cryptography Algorithm

# Sources:
# https://github.com/qmunitytech/Tutorials/blob/main/intermediate/The%20BB84%20Quantum%20Cryptography%20algorithm.ipynb
# https://qiskit.github.io/qiskit-aer/index.html
# https://docs.quantum.ibm.com/guides
# https://en.wikipedia.org/wiki/BB84

# Imports
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator#, QasmSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
#%matplotlib inline

# Load IBM Quantum API key from .env file
load_dotenv()
api_key = os.environ.get('IBM_QUANTUM_TOKEN')

# Generate Binary Strings
N = 32
alice_basis = np.random.randint(2, size=N)
alice_state = np.random.randint(2, size=N)
bob_basis = np.random.randint(2, size=N)
print(f"Alice's State:\t {np.array2string(alice_state)}")
print(f"Alice's Bases:\t {np.array2string(alice_basis)}")
print(f"Bob's Bases:\t {np.array2string(bob_basis)}")

# Create BB84 Quantum Circuit
def bb84_circ(N, state, alice_basis, bob_basis):
    # Create a quantum circuit with N qubits and N classical bits
    qc = QuantumCircuit(N)

    # Add X gates to encode Alice's state
    for i in range(0, len(state)):
        if (state[i] == 1):
            qc.x(i)
    
    # Add Hadamard gates to encode Alice's basis
    for i in range(0, len(alice_basis)):
        if (alice_basis[i] == 1):
            qc.h(i)

    # Alice sends state Phi to Bob
    # Bob then measures in his randomly selected basis vector
    for i in range(0, len(bob_basis)):
        if (bob_basis[i] == 1):
            qc.h(i) # Hadamard basis
    qc.measure_all()
    return qc

# Initialize quantum circuit and backend
qc = bb84_circ(N, alice_state, alice_basis, bob_basis)
print(qc) # Plots circuit
#qc.draw(output='mpl').savefig('bb84_circuit.png')
#plt.show()
#service = QiskitRuntimeService(channel="ibm_quantum", token=api_key)
#backend = service.least_busy(simulator=False, operational=True)

# Transpile circuit for simulator
simulator = AerSimulator(method='matrix_product_state')
qc = transpile(qc, simulator)

# Perform qubit exchange via quantum circuit simulation
result = simulator.run(qc.reverse_bits(), shots=1).result()
counts = result.get_counts(qc).most_frequent()
print(f"Qubit exchange result: {counts}")

# Exchange measurement bases
# Alice and Bob compare their bases and keep the bits where they agree
key = []
for i in range(0, len(counts)):
    if (alice_basis[i] == bob_basis[i]):
        key.append(counts[i])
print(f"Shared key: {key}")
