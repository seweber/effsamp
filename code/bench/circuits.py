"""Benchmark circuits on NoiseCirc's gates ``r``, ``rz`` and ``cp``.

``brickwork``, ``ghz``, ``qft`` and ``qiskit_random`` are copied from noisecirc's
``benchmarks/_circuits.py`` (same seeds, same circuits); ``grid`` and ``qaoa`` are new.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.random import random_circuit
from qiskit.transpiler import CouplingMap


def brickwork(n: int, layers: int) -> QuantumCircuit:
    """Random ``r`` on every qubit and ``cp`` on alternating neighbor pairs, per layer (1D local)."""
    rng = np.random.default_rng(n)
    circuit = QuantumCircuit(n)
    for layer in range(layers):
        for q in range(n):
            circuit.r(rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi), q)
        for q in range(layer % 2, n - 1, 2):
            circuit.cp(rng.uniform(0, np.pi), q, q + 1)
    return circuit


def ghz(n: int) -> QuantumCircuit:
    """GHZ preparation: a chain of ``cp`` gates, each waiting for the one before."""
    circuit = QuantumCircuit(n)
    circuit.r(np.pi / 2, np.pi / 2, 0)
    for target in range(1, n):
        circuit.r(np.pi / 2, np.pi / 2, target)
        circuit.cp(np.pi, target - 1, target)
        circuit.r(-np.pi / 2, np.pi / 2, target)
    return circuit


def qiskit_random(n: int, depth: int, seed: int) -> QuantumCircuit:
    """Qiskit's random circuit transpiled to ``r``, ``rz``, ``cp`` on a line."""
    drawn = random_circuit(n, depth, max_operands=2, seed=seed)
    transpiled = transpile(
        drawn,
        basis_gates=["r", "rz", "cp"],
        coupling_map=CouplingMap.from_line(n),
        initial_layout=list(range(n)),
        optimization_level=1,
        seed_transpiler=seed,
    )
    circuit = QuantumCircuit(n)
    for instruction in transpiled.data:
        circuit.append(instruction.operation, sorted(transpiled.find_bit(q).index for q in instruction.qubits))
    return circuit


def qft(n: int) -> QuantumCircuit:
    """The QFT without final swaps: ``cp`` on every pair of qubits (all-to-all, long range)."""
    from qiskit.synthesis import synth_qft_full

    transpiled = transpile(synth_qft_full(n, do_swaps=False), basis_gates=["r", "rz", "cp"], optimization_level=0)
    circuit = QuantumCircuit(n)
    for instruction in transpiled.data:
        circuit.append(instruction.operation, sorted(transpiled.find_bit(q).index for q in instruction.qubits))
    return circuit


def grid(n: int, cycles: int) -> QuantumCircuit:
    """A 2D random circuit on a ``rows x cols`` grid (row-major qubits), supremacy-like.

    Each cycle applies a random ``r`` (from {sqrt X, sqrt Y, sqrt W}-like axes) on every qubit, then
    ``cp(pi/2)``-like random phases on one of four edge patterns (ABCD), so that vertical edges couple
    qubits ``cols`` apart.
    """
    rows = int(np.floor(np.sqrt(n)))
    while n % rows:
        rows -= 1
    cols = n // rows
    rng = np.random.default_rng(1000 + n)
    edges = {k: [] for k in range(4)}
    for r in range(rows):
        for c in range(cols):
            q = r * cols + c
            if c + 1 < cols:
                edges[(c % 2)].append((q, q + 1))
            if r + 1 < rows:
                edges[2 + (r % 2)].append((q, q + cols))
    circuit = QuantumCircuit(n)
    for cycle in range(cycles):
        for q in range(n):
            circuit.r(np.pi / 2, rng.choice([0, np.pi / 4, np.pi / 2]), q)
        for a, b in edges[[0, 2, 1, 3][cycle % 4]]:
            circuit.cp(rng.uniform(0, np.pi), a, b)
    return circuit


def qaoa(n: int, p: int) -> QuantumCircuit:
    """QAOA MaxCut on a random 3-regular graph: ``cp``-based ZZ phases on random (long-range) edges."""
    import networkx as nx  # qiskit depends on rustworkx; networkx comes with qutip/cirq

    graph = nx.random_regular_graph(3, n, seed=n)
    rng = np.random.default_rng(2000 + n)
    circuit = QuantumCircuit(n)
    for q in range(n):
        circuit.r(np.pi / 2, np.pi / 2, q)
    for _ in range(p):
        gamma, beta = rng.uniform(0, np.pi, 2)
        for a, b in sorted(graph.edges()):
            # exp(-i gamma Z_a Z_b) up to phase: rz on both, cp(-4 gamma) on the pair
            circuit.rz(2 * gamma, a)
            circuit.rz(2 * gamma, b)
            circuit.cp(-4 * gamma, min(a, b), max(a, b))
        for q in range(n):
            circuit.r(2 * beta, 0.0, q)
    return circuit


def scramble(n: int, layers: int) -> QuantumCircuit:
    """Random ``r`` on every qubit, then ``cp`` on a random perfect matching of all qubits, per layer.

    The pairs are long-ranged and change every layer, so a block of a few qubits holds few gates: the
    least fusable of the circuits here.
    """
    rng = np.random.default_rng(3000 + n)
    circuit = QuantumCircuit(n)
    for _ in range(layers):
        for q in range(n):
            circuit.r(rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi), q)
        order = rng.permutation(n)
        for a, b in zip(order[0::2], order[1::2]):
            circuit.cp(rng.uniform(0, np.pi), int(min(a, b)), int(max(a, b)))
    return circuit


def su4_brickwork(n: int, layers: int) -> QuantumCircuit:
    """Generic dense two-qubit gates (`gates.su4`, random coefficients) on alternating neighbor pairs (A18, A19)."""
    from qiskit.circuit import Gate

    rng = np.random.default_rng(4000 + n)
    circuit = QuantumCircuit(n)
    for layer in range(layers):
        for q in range(layer % 2, n - 1, 2):
            circuit.append(Gate("su4", 2, list(rng.uniform(-np.pi / 2, np.pi / 2, 15))), [q, q + 1])
    return circuit


def fsim_grid(n: int, cycles: int) -> QuantumCircuit:
    """`grid` with fSim gates (`gates.fsim`, theta near pi/2, phi near pi/6) instead of ``cp``, Sycamore-like (A19)."""
    from qiskit.circuit import Gate

    base = grid(n, cycles)
    rng = np.random.default_rng(5000 + n)
    circuit = QuantumCircuit(n)
    for instruction in base.data:
        qubits = [base.find_bit(q).index for q in instruction.qubits]
        if instruction.operation.name == "cp":
            theta, phi = np.pi / 2 + rng.normal(0, 0.1), np.pi / 6 + rng.normal(0, 0.05)
            circuit.append(Gate("fsim", 2, [theta, phi]), qubits)
        else:
            circuit.append(instruction.operation, qubits)
    return circuit


def heisenberg(n: int, steps: int) -> QuantumCircuit:
    """Trotterized 1D Heisenberg chain in a random field: ``rxx``, ``ryy``, ``rzz`` per bond, ``rz`` per site (A19)."""
    from qiskit.circuit import Gate

    rng = np.random.default_rng(6000 + n)
    fields = rng.uniform(-1, 1, n)
    dt = 0.1
    circuit = QuantumCircuit(n)
    for q in range(0, n, 2):
        circuit.r(np.pi, 0.0, q)  # Neel state
    for _ in range(steps):
        for parity in (0, 1):
            for q in range(parity, n - 1, 2):
                for name in ("rxx", "ryy", "rzz"):
                    circuit.append(Gate(name, 2, [2 * dt]), [q, q + 1])
        for q in range(n):
            circuit.rz(2 * dt * fields[q], q)
    return circuit


def cry_ladder(n: int, layers: int) -> QuantumCircuit:
    """Controlled-RY on alternating neighbor pairs between random ``r`` layers (A19)."""
    from qiskit.circuit import Gate

    rng = np.random.default_rng(7000 + n)
    circuit = QuantumCircuit(n)
    for layer in range(layers):
        for q in range(n):
            circuit.r(rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi), q)
        for q in range(layer % 2, n - 1, 2):
            circuit.append(Gate("cry", 2, [rng.uniform(0, np.pi)]), [q, q + 1])
    return circuit


def channels(circuit: QuantumCircuit) -> int:
    """Gate-qubit pairs, i.e. noise channels when every gate is followed by noise on its targets."""
    return sum(len(instruction.qubits) for instruction in circuit.data)


def make(name: str, n: int) -> QuantumCircuit:
    """Return the benchmark circuit ``name`` at its standard depth for ``n`` qubits."""
    if name == "ghz":
        return ghz(n)
    if name == "brickwork":
        return brickwork(n, n // 2 + 1)
    if name == "brickwork_deep":
        return brickwork(n, 2 * n)
    if name == "qft":
        return qft(n)
    if name == "random":
        return qiskit_random(n, n, seed=n)
    if name == "grid":
        return grid(n, n)
    if name == "qaoa":
        return qaoa(n, 2)
    if name == "scramble":
        return scramble(n, n // 2 + 1)
    if name == "su4":
        return su4_brickwork(n, n // 2 + 1)
    if name == "fsim":
        return fsim_grid(n, n)
    if name == "heisenberg":
        return heisenberg(n, n // 2)
    if name == "cry":
        return cry_ladder(n, n // 2 + 1)
    raise ValueError(name)
