"""A13: static work (FP instructions, shared accesses) of measured blocks, against their measured pass times.

Recompiles the circuits of an A7 block-time run without a GPU (dryrun.compile_like_simulator), counts
each block's work with kernel_ops, and prints one JSON line per block with the measured dominant time.

Usage: a13_static.py RUN_DIR [--set key=value ...]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402
from kernel_ops import block_work  # noqa: E402

from noisecirc import Simulator  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("run")
parser.add_argument("--set", action="append", default=[])
args = parser.parse_args()
options, config = configpatch.parse(args.set)
configpatch.apply(config)
for line in open(Path(args.run) / "stdout.txt"):
    rec = json.loads(line)
    qc = circuits.make(rec["circuit"], rec["n"])
    sim = Simulator(maps=noise.maps(rec["noise"], rec["p"]), **options)
    compiled, _, _ = compile_like_simulator(qc, sim)
    assert len(compiled.blocks) == rec["blocks"], (len(compiled.blocks), rec["blocks"])
    for i, block in enumerate(compiled.blocks):
        w = block_work(block.dominant_block, compiled.config)
        print(json.dumps({"circuit": rec["circuit"], "p": rec["p"], "n": rec["n"], "block": i, "t_bw": rec["t_bw"],
                          "t_dom": rec["t_dom"][i], "t_mask": rec["t_mask"][i], **w}), flush=True)
