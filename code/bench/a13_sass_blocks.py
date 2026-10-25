"""A13 follow-up: SASS instruction classes of the blocks timed in the A13 sweeps, for a refit of the pass-time model.

For each given run directory of a13_blocks.py (data/*-a13-block-times-*), recompiles the workloads
locally with the run's settings (its --set items), as the dry run compiles them (the blocks are the
same as on the GPU), counts each distinct block's SASS instructions per amplitude (a13_sass.py), and
writes one JSON line per block with the measured pass time, t_bw and the counts.

Usage: a13_sass_blocks.py RUN_DIR... (local, CPU; needs $NVDISASM)
"""

import dataclasses
import json
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a13_sass import cubin, exact, opcodes, per_amplitude, raw_counts, sass  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402


def main() -> None:
    for run in sys.argv[1:]:
        run = Path(run)
        argv = shlex.split((run / "command.txt").read_text())
        argv = argv[argv.index("a13_blocks.py") + 1:]
        sets = [argv[i + 1] for i, a in enumerate(argv) if a == "--set"]
        qubits = int(argv[argv.index("--qubits") + 1])
        options, config = configpatch.parse(sets)
        configpatch.apply(config)
        records = [json.loads(line) for line in open(run / "stdout.txt")]
        for rec in records:
            qc = circuits.make(rec["circuit"], qubits)
            sim = Simulator(maps=noise.maps(None if rec["noise"] == "none" else rec["noise"], rec["p"]), **options)
            compiled, _, _ = compile_like_simulator(qc, sim)
            assert len(compiled.blocks) == rec["blocks"], (run.name, rec["circuit"])
            cfg = dataclasses.replace(compiled.config, threads=1024)
            counts = {}
            for b, (block, measured) in enumerate(zip(compiled.blocks, rec["per_block"])):
                if block not in counts:
                    dom = block.dominant_block
                    ops = opcodes(sass(cubin(dom, cfg)))
                    counts[block] = (per_amplitude(ops, cfg, len(dom.tile(cfg))), raw_counts(ops),
                                     1 << __import__("svpass.cuda.codegen", fromlist=["x"]).stage_width(cfg, len(dom.tile(cfg))))
                assert abs(measured["shared"] - __import__("kernel_ops").block_work(block.dominant_block, compiled.config)["shared"]) < 1e-9
                print(json.dumps({"run": run.name, "circuit": rec["circuit"], "block": b, "dtype": compiled.config.dtype,
                                  "t_dom": measured["t_dom"], "t_bw": rec["t_bw"], "fp_ops": measured["fp_ops"],
                                  "shared": measured["shared"], "stages": measured["stages"], "sass": counts[block][0],
                                  "opcodes": counts[block][1], "per_thread": counts[block][2],
                                  "exact": exact(cfg, len(block.dominant_block.tile(cfg)))}), flush=True)
        configpatch.apply({})


if __name__ == "__main__":
    main()
