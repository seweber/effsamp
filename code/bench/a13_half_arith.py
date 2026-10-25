"""A13 follow-up: accuracy of computing in half precision (packed HFMA2) against storing in it (complex32).

svpass's complex32 stores amplitudes in half precision but computes in single precision, rounding
once per block pass. Computing in half precision as well (two half operations per instruction, which
would halve the floating-point instructions of an arithmetic-bound pass) rounds after every
operation. This emulation applies a circuit gate by gate on n qubits with NumPy, the state scaled by
2**(n/2) as svpass stores it, in four ways:

- complex128 (reference);
- complex64 arithmetic;
- complex32 storage: complex64 arithmetic, rounded to half precision every G gates (G = the circuit's
  gates per block at 26 qubits, about one block pass);
- complex32 tile: as complex32 storage, but rounded every 8 gates, about once per stage, as a tile kept
  in half precision in shared memory would round;
- half arithmetic: every real multiplication and addition rounded to half precision (NumPy float16;
  an FMA rounds once, so this is somewhat pessimistic).

Prints the total variation distance of the outcome probabilities and the relative error of the norm.

Usage: a13_half_arith.py [n] (local, CPU)
"""

import json
import sys
from pathlib import Path

import numpy as np
from qiskit.quantum_info import Operator

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402

GATES_PER_BLOCK = {"ghz": 25, "brickwork": 40, "qft": 30, "qaoa": 45, "grid": 50}


def gates(qc):
    for ci in qc.data:
        yield Operator(ci.operation).data, [qc.find_bit(q).index for q in ci.qubits]


def apply(state_re, state_im, m, qs, n, dtype):
    """Apply matrix m (little-endian qubits qs, as qiskit) to the state given as real arrays, in ``dtype`` arithmetic."""
    k = len(qs)
    axes = [n - 1 - q for q in reversed(qs)]  # qiskit: qs[0] is the least significant bit of m's index
    re = np.moveaxis(state_re.reshape((2,) * n), axes, range(k)).reshape(2**k, -1)
    im = np.moveaxis(state_im.reshape((2,) * n), axes, range(k)).reshape(2**k, -1)
    mr, mi = m.real.astype(dtype), m.imag.astype(dtype)
    out_re = np.zeros_like(re)
    out_im = np.zeros_like(im)
    for i in range(2**k):
        acc_r = np.zeros(re.shape[1], dtype=dtype)
        acc_i = np.zeros(re.shape[1], dtype=dtype)
        for j in range(2**k):
            if abs(m[i, j]) < 1e-15:
                continue
            acc_r = (acc_r + mr[i, j] * re[j] - mi[i, j] * im[j]).astype(dtype)
            acc_i = (acc_i + mr[i, j] * im[j] + mi[i, j] * re[j]).astype(dtype)
        out_re[i], out_im[i] = acc_r, acc_i
    back = lambda a: np.moveaxis(a.reshape([2] * k + [2] * (n - k)), range(k), axes).reshape(-1)  # noqa: E731
    return back(out_re), back(out_im)


def run(qc, n, mode, block):
    if mode == "complex32 tile":
        mode, block = "complex32", 8
    dtype = {"complex128": np.float64, "complex64": np.float32, "complex32": np.float32, "half": np.float16}[mode]
    re = np.zeros(2**n, dtype=dtype)
    im = np.zeros(2**n, dtype=dtype)
    re[0] = 2 ** (n / 2)
    for g, (m, qs) in enumerate(gates(qc)):
        re, im = apply(re, im, m, qs, n, dtype)
        if mode == "complex32" and (g + 1) % block == 0:
            re, im = re.astype(np.float16).astype(np.float32), im.astype(np.float16).astype(np.float32)
    if mode == "complex32":
        re, im = re.astype(np.float16).astype(np.float32), im.astype(np.float16).astype(np.float32)
    return re.astype(np.float64) + 1j * im.astype(np.float64)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    for name in ["ghz", "brickwork", "qft", "qaoa", "grid"]:
        qc = circuits.make(name, n)
        ref = run(qc, n, "complex128", 0)
        p_ref = np.abs(ref) ** 2
        row = {"circuit": name, "n": n, "gates": len(qc.data)}
        for mode in ("complex64", "complex32", "complex32 tile", "half"):
            psi = run(qc, n, mode, GATES_PER_BLOCK[name])
            p = np.abs(psi) ** 2
            row[mode] = {"tvd": float(0.5 * np.abs(p / p.sum() - p_ref / p_ref.sum()).sum()),
                         "norm_error": float(abs(p.sum() / p_ref.sum() - 1))}
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
