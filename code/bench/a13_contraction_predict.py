"""A13 follow-up: SASS instructions and predicted dominant-pass times of kernels in the cheapest contraction order.

For the five A13 workloads at n = 26 and a base configuration (default: A14 kernels, 4-qubit stages,
complex32), compiles each block's dominant kernel with and without svpass's `stage_contraction`
(noisecirc branch feature/stage-contraction) for sm_90, counts its SASS instructions per amplitude
(a13_sass.py) and predicts its time with the model "fp+shared+integer" of
data/a13-analysis/refit.json, summed over the blocks (one trajectory). Also reports the generator's
time per block.

Usage: a13_contraction_predict.py [--set key=value ...] (local, CPU; needs $NVDISASM)
"""

import argparse
import dataclasses
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a13_predict import FP_RATE, ROOT, T_BW, features, predict  # noqa: E402
from a13_sass import cubin, opcodes, per_amplitude, sass  # noqa: E402
from a13_stage_estimate import WORKLOADS  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402
from svpass.cuda import codegen  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", action="append", default=["stage_fusion=1", "rotation_form=1", "stage_qubits=4", "dtype=complex32"])
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    model = json.loads((ROOT / "data" / "a13-analysis" / "refit.json").read_text())["fp+shared+integer"]
    for name, p in WORKLOADS:
        qc = circuits.make(name, 26)
        compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), **options))
        base_cfg = dataclasses.replace(compiled.config, threads=1024)
        new_cfg = dataclasses.replace(base_cfg, stage_contraction=True)
        slots = T_BW[base_cfg.dtype] / 2**26 * FP_RATE
        totals = {"base": 0.0, "contraction": 0.0}
        counts = {"base": {"F": 0.0, "L": 0.0, "I": 0.0}, "contraction": {"F": 0.0, "L": 0.0, "I": 0.0}}
        generate = 0.0
        for block in compiled.blocks:
            dom = block.dominant_block
            k = len(dom.tile(base_cfg))
            for key, cfg in (("base", base_cfg), ("contraction", new_cfg)):
                if key == "contraction":
                    t = time.time()
                    codegen.kernel_source(dom, cfg)
                    generate += time.time() - t
                f = features(per_amplitude(opcodes(sass(cubin(dom, cfg))), cfg, k))
                totals[key] += predict(f, slots, model)
                for c in f:
                    counts[key][c] += f[c] / len(compiled.blocks)
        nb = len(compiled.blocks)
        print(json.dumps({"circuit": name, "dtype": base_cfg.dtype, "stage_qubits": base_cfg.stage_qubits, "blocks": nb,
                          "sass_per_amplitude_per_block": counts,
                          "t_over_t_bw_base": totals["base"] / nb, "t_over_t_bw_contraction": totals["contraction"] / nb,
                          "contraction_vs_base": totals["contraction"] / totals["base"],
                          "generator_seconds_per_block": generate / nb}), flush=True)


if __name__ == "__main__":
    main()
