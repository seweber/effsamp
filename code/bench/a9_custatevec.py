"""A9: noisy trajectories with cuStateVec Ex's state-vector updater (delayed lower-bound sampling).

cuStateVec Ex (cuQuantum 26.9, Python bindings `cuquantum.bindings.custatevecEx`) applies a queue of
matrices and channels to a state vector with `SVUpdater`, which fuses dense and diagonal matrices and,
for a general channel, samples the Kraus operator with probability lower bounds from their
eigenvalues and computes expectation values only when a random number falls above the bounds
(the delayed inner-product algorithm of qsim, Isakov et al. 2021). It simulates one trajectory per
apply: a shot is: reset to |0...0>, apply the queue with fresh random numbers, sample one bit string.

The circuit's gates go in as matrices (diagonal ones as diagonal), and after every gate a general
channel of the noise on each of its targets (single-qubit channels, equivalent to their tensor
product). Single precision. Prints one JSON line per point. Run with the cuQuantum side environment:
gpurun -p /local/venv-cuq/bin/python a9_custatevec.py ...
"""

import argparse
import json
import sys
import time

import cupy as cp
import numpy as np
from qiskit.quantum_info import Operator

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402

from cuquantum.bindings import custatevec as cs  # noqa: E402
from cuquantum.bindings import custatevecEx as ex  # noqa: E402

C_32F = 4  # cudaDataType CUDA_C_32F


class Updater:
    def __init__(self, qc, kind, p, dense_fusion=None, diagonal_fusion=None):
        n = qc.num_qubits
        self.n = n
        config = ex.configure_state_vector_single_device(C_32F, n, n, 0, 0)
        self.sv = ex.state_vector_create_single_process(config, [0], 1, 0)
        ex.dictionary_destroy(config)
        items = []
        if dense_fusion is not None:
            items.append(ex.SVUpdaterConfigItem(ex.SVUpdaterConfigName.DENSE_FUSION_SIZE, dense_fusion))
        if diagonal_fusion is not None:
            items.append(ex.SVUpdaterConfigItem(ex.SVUpdaterConfigName.DIAGONAL_FUSION_SIZE, diagonal_fusion))
        uconfig = ex.configure_sv_updater(C_32F, items)
        self.updater = ex.sv_updater_create(uconfig, 0)
        ex.dictionary_destroy(uconfig)
        self.keep = []  # host buffers must outlive the enqueue calls
        local = [np.ascontiguousarray(np.asarray(k, dtype=np.complex64)) for k in noise.kraus(kind, p)] if kind else []
        layout = cs.MatrixLayout.ROW
        for instruction in qc.data:
            targets = [qc.find_bit(q).index for q in instruction.qubits]
            matrix = Operator(instruction.operation).data
            if np.allclose(matrix, np.diag(np.diag(matrix))):
                data = np.ascontiguousarray(np.diag(matrix).astype(np.complex64))
                mtype = ex.MatrixType.DIAGONAL
            else:
                data = np.ascontiguousarray(matrix.astype(np.complex64))
                mtype = ex.MatrixType.DENSE
            self.keep.append(data)
            ex.sv_updater_enqueue_matrix(self.updater, data.ctypes.data, C_32F, mtype, layout, 0, targets,
                                         len(targets), [], [], 0)
            for q in targets if local else []:
                ptrs = [k.ctypes.data for k in local]
                types = [ex.MatrixType.DENSE] * len(local)
                ex.sv_updater_enqueue_general_channel(self.updater, ptrs, C_32F, types, len(local), layout, [q], 1)
        self.keep.append(local)
        self.randnums = ex.sv_updater_get_max_num_required_randnums(self.updater)
        self.bits = np.zeros(1, dtype=np.int64)

    def shot(self, rng) -> int:
        ex.state_vector_set_zero_state(self.sv)
        r = rng.random(max(self.randnums, 1)).tolist()
        ex.sv_updater_apply(self.updater, self.sv, r, self.randnums)
        ex.sample(self.sv, self.bits.ctypes.data, list(range(self.n)), self.n, [float(rng.random())], 1,
                  cs.SamplerOutput.RANDNUM_ORDER, 0)
        return int(self.bits[0])

    def close(self):
        ex.sv_updater_destroy(self.updater)
        ex.state_vector_destroy(self.sv)


def exact_distribution(qc, kind, p) -> np.ndarray:
    """The circuit's outcome distribution with noise ``kind`` after every gate, by density matrix (small n)."""
    n = qc.num_qubits
    rho = np.zeros((2**n, 2**n), dtype=complex)
    rho[0, 0] = 1
    local = [np.asarray(k, dtype=complex) for k in noise.kraus(kind, p)]

    def embed(matrix, targets):
        full = np.zeros((2**n, 2**n), dtype=complex)
        for i in range(2**n):
            sub_i = sum(((i >> q) & 1) << j for j, q in enumerate(targets))
            rest = i & ~sum(1 << q for q in targets)
            for sub_o in range(2 ** len(targets)):
                o = rest | sum(((sub_o >> j) & 1) << q for j, q in enumerate(targets))
                full[o, i] = matrix[sub_o, sub_i]
        return full

    for instruction in qc.data:
        targets = [qc.find_bit(q).index for q in instruction.qubits]
        u = embed(Operator(instruction.operation).data, targets)
        rho = u @ rho @ u.conj().T
        for q in targets:
            ks = [embed(k, [q]) for k in local]
            rho = sum(k @ rho @ k.conj().T for k in ks)
    return np.real(np.diag(rho))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuit", default="brickwork")
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--ps", default="0.001")
    parser.add_argument("--shots", type=int, default=100)
    parser.add_argument("--dense-fusion", type=int, default=None)
    parser.add_argument("--diagonal-fusion", type=int, default=None)
    parser.add_argument("--check", action="store_true", help="compare sampled outcomes with the exact distribution")
    args = parser.parse_args()
    qc = circuits.make(args.circuit, args.qubits)
    for p in [float(x) for x in args.ps.split(",")]:
        kind = None if args.noise == "none" else args.noise
        u = Updater(qc, kind, p, args.dense_fusion, args.diagonal_fusion)
        rng = np.random.default_rng(1)
        if args.check:
            counts = np.bincount([u.shot(rng) for _ in range(args.shots)], minlength=2**args.qubits) / args.shots
            exact = exact_distribution(qc, kind, p)
            sigma = np.sqrt(exact * (1 - exact) / args.shots)
            print(json.dumps({"kind": "check", "circuit": args.circuit, "n": args.qubits, "p": p, "shots": args.shots,
                              "tvd": float(0.5 * np.abs(counts - exact).sum()),
                              "max_z": float(np.max(np.abs(counts - exact) / np.maximum(sigma, 1e-12)))}), flush=True)
            u.close()
            continue
        u.shot(rng)  # warm-up
        ex.state_vector_synchronize(u.sv)
        start = time.perf_counter()
        outcomes = [u.shot(rng) for _ in range(args.shots)]
        ex.state_vector_synchronize(u.sv)
        elapsed = time.perf_counter() - start
        print(json.dumps({"kind": "run", "sim": "custatevec_ex", "circuit": args.circuit, "n": args.qubits,
                          "noise": args.noise, "p": p, "shots": args.shots, "time": elapsed,
                          "randnums": u.randnums, "gates": len(qc.data), "channels": circuits.channels(qc),
                          "dense_fusion": args.dense_fusion, "diagonal_fusion": args.diagonal_fusion,
                          "distinct_outcomes": len(set(outcomes))}), flush=True)
        u.close()
        cp.get_default_memory_pool().free_all_blocks()


if __name__ == "__main__":
    main()
