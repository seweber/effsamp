"""A13 follow-up: the instructions the compiler really emits for a block's kernel (SASS), by class.

Compiles the dominant kernel of every distinct block of a workload with svpass's code generator and
NVRTC for the H100 (sm_90, no GPU needed: blocks come from the dry run's compilation), disassembles
it with nvdisasm ($NVDISASM, from the pip package nvidia-cuda-nvdisasm), and counts the SASS
instructions per class, see `classify`.

Usage: a13_sass.py --workloads circuit:noise:p,... [--qubits n] [--set key=value ...] [--variant key=value ...] [--dump N]
(local, CPU)
"""

import argparse
import dataclasses
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402
from kernel_ops import block_work  # noqa: E402

from noisecirc import Simulator  # noqa: E402

NVDISASM = os.environ.get("NVDISASM", "nvdisasm")

# H100 PCIe properties that svpass's `CudaDevice._min_blocks` reads from the device.
_SM = {"threads": 2048, "shared": 233472, "reserved": 1024, "registers": 65536}


def min_blocks(config, k: int) -> int:
    """`svpass.cuda.device.CudaDevice._min_blocks` with the H100's properties."""
    from svpass.cuda import codegen

    group = codegen.group(config, k)
    threads = codegen.threads(config, group, k)
    shared = group * config.complex.itemsize + _SM["reserved"]
    return max(1, min(_SM["threads"] // threads, _SM["shared"] // shared,
                      _SM["registers"] // (config.min_registers * threads)))


def cubin(block, config) -> bytes:
    """Compile the block's kernel as svpass does (`svpass.cuda.device._module`) for sm_90 and return the cubin."""
    from cuda import core as cc
    from svpass.cuda import codegen, device

    k = len(block.tile(config))
    defines = [("MIN_BLOCKS", str(min_blocks(config, k)))]
    options = cc.ProgramOptions(std="c++17", arch="sm_90", include_path=[device._include_directory()],
                                define_macro=defines)
    return cc.Program(codegen.kernel_source(block, config), code_type="c++", options=options).compile("cubin").code


def sass(code: bytes) -> list[str]:
    with tempfile.NamedTemporaryFile(suffix=".cubin") as f:
        f.write(code)
        f.flush()
        out = subprocess.run([NVDISASM, "-c", "-hex", f.name], capture_output=True, text=True, check=True).stdout
    return out.splitlines()


_INSTR = re.compile(r"^\s+/\*[0-9a-f]{4,}\*/\s+(?:@!?U?P\w+\s+)?([A-Z][A-Z0-9_.]*)")


def opcodes(lines: list[str]) -> list[str]:
    ops = []
    for line in lines:
        m = _INSTR.match(line)
        if m:
            ops.append(m.group(1))
    return ops


CLASSES = {
    "fp32": ("FFMA", "FMUL", "FADD", "FSEL", "FMNMX", "FSETP"),
    "shared": ("LDS", "STS"),
    "global": ("LDG", "STG"),
    "convert": ("F2F", "F2FP", "HADD2.F32", "I2F", "F2I"),
    "move": ("MOV", "UMOV"),
    "control": ("BRA", "BAR", "BSSY", "BSYNC", "EXIT", "WARPSYNC", "NOP", "ENDCOLLECTIVE", "SHFL", "RET", "CALL"),
    "fp64": ("DADD", "DFMA", "DMUL"),
    "local": ("LDL", "STL"),
}


def classify(op: str) -> str:
    """The class of a SASS opcode: floating point, shared or global memory, conversion, move, control, or integer (the rest)."""
    for name, prefixes in CLASSES.items():
        if any(op == p or op.startswith(p + ".") for p in prefixes):
            return name
    return "integer"


def per_amplitude(ops: list[str], config, k: int) -> dict:
    """Instructions per class divided by the amplitudes a thread holds, 2**R.

    A stage loop's body is counted once and handles 2**R amplitudes per thread; the unrolled loads
    and stores handle group / threads, which `main` makes equal by allowing enough threads (up to
    1024). Where a tile is too large for that (2**14 amplitudes at R = 3), the loads and stores are
    counted group / threads / 2**R times too often; `exact` (below) flags those kernels.
    """
    from svpass.cuda import codegen

    per_thread = 1 << codegen.stage_width(config, k)
    counts = Counter(classify(op) for op in ops)
    return {name: counts.get(name, 0) / per_thread for name in (*CLASSES, "integer")}


def exact(config, k: int) -> bool:
    """Whether `per_amplitude` is exact for a tile of ``k`` qubits: a thread holds 2**R amplitudes of a group."""
    from svpass.cuda import codegen

    group = codegen.group(config, k)
    return group // codegen.threads(config, group, k) == 1 << codegen.stage_width(config, k)


def raw_counts(ops: list[str]) -> dict:
    """Opcode counts of the whole kernel (not per amplitude), so that classes can be redrawn later."""
    return dict(Counter(ops))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--dump", type=int, default=-1)
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    variant = {}
    for item in args.variant:
        key, value = item.split("=")
        variant[key] = bool(int(value)) if key in ("stage_fusion", "rotation_form", "stage_populations") else int(value)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, args.qubits)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = compile_like_simulator(qc, sim)
        # Threads such that each thread holds 2**R amplitudes of a group (see `per_amplitude`).
        cfg = dataclasses.replace(compiled.config, threads=1024, **variant)
        seen = set()
        for b, block in enumerate(compiled.blocks):
            if block in seen:
                continue
            seen.add(block)
            lines = sass(cubin(block.dominant_block, cfg))
            if b == args.dump:
                print("\n".join(lines))
                return
            k = len(block.dominant_block.tile(cfg))
            print(json.dumps({"circuit": name, "block": b, "variant": variant, "dtype": cfg.dtype,
                              "stage_qubits": cfg.stage_qubits, "sass": per_amplitude(opcodes(lines), cfg, k),
                              **block_work(block.dominant_block, cfg)}), flush=True)


if __name__ == "__main__":
    main()
