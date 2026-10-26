"""A16: where the time of a tensor-core pass goes, by ablation of the generated source.

Times the dominant kernels of a workload's distinct blocks with `tensor_cores` = --mode, with the
generated source changed by one ablation at a time (results are wrong, only times count):
  full    : unchanged;
  noload  : the per-lane fragment tables are not loaded (registers set from the lane instead);
  nomma   : no mma instruction (accumulators stay zero);
  noshared: the tensor-core loops neither load nor store shared memory;
  cuda    : tensor_cores off (the base Config, e.g. stage_contraction).
Prints per workload the sum over the distinct blocks of pass time over bandwidth time.

Usage: a16_ablate.py --workloads circuit:noise:p,... --qubits n --mode f16 [--set key=value ...]
"""

import argparse
import dataclasses
import json
import re
import sys

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a7_blocks import timed  # noqa: E402
from a13_blocks import bandwidth_time  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402
from svpass import Engine  # noqa: E402
from svpass import engine as svpass_engine  # noqa: E402
from svpass.cuda import codegen  # noqa: E402

_ORIGINAL = codegen.kernel_source
ABLATIONS = {
    "full": [],
    "noload": [(r"= tc\d+[hl]\[\d+u \+ lane\];", "= lane * 2654435761u;")],
    "notable": [(r"const uint2 tp = tp\d+\[threadIdx\.x\];", "const uint2 tp = make_uint2(threadIdx.x * 3u, threadIdx.x * 5u);")],
    "nomma": [(r"mma_(f16|tf32)\(([a-z]\d+(_\d+)?|p), [^;]*\);", ";")],
    # No tensor-core stage at all: the kernel only loads, stores, and synchronizes per stage.
    "nostage": [(r"\n    \{\n        const unsigned int lane = threadIdx\.x & 31u;\n(?:        .*\n)*?    \}\n    __syncthreads", "\n    __syncthreads")],
    # The fast path's shared-memory loads and stores of the tensor-core stages removed.
    "noshared": [(r"(x\d+_\d+) = tile\[tp\.x \^ (\d+u)\];", r"\1 = make_float2(__uint_as_float(tp.x ^ \2), 1.0f);"),
                 (r"tile\[tp\.y \^ (\d+u)\] = (make_float2\([^;]*\));", r"if (tp.y == \1) tile[0] = \2;")],
    # The conversions of the amplitudes to the tensor cores' types replaced by reinterpretation.
    "noconvert": [(r"split_tf32\(([^,]+), (bh[\d_]+), (bl[\d_]+)\);", r"\2 = __float_as_uint(\1); \3 = \2 >> 13;"),
                  (r"= to_f16x2\(([^,]+), ([^)]+)\);", r"= __float_as_uint(\1) ^ __float_as_uint(\2);")],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--mode", required=True)
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    itemsize = 4 if options.get("dtype") == "complex32" else 8
    t_bw = bandwidth_time(n, itemsize)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = sim._compiled(qc)
        blocks = list(dict.fromkeys(compiled.blocks))
        result = {}
        noswizzle = [(r"(unsigned int slot\(unsigned int e\) \{\n    return e)[^;]*;", r"\1;")]
        ABLATIONS["empty"] = ABLATIONS["noload"] + ABLATIONS["notable"] + ABLATIONS["nomma"] + ABLATIONS["noshared"]
        for ablation in [*ABLATIONS, "cuda"]:
            cfg = compiled.config if ablation.startswith("cuda") else dataclasses.replace(compiled.config, tensor_cores=args.mode)
            rules = ABLATIONS.get(ablation, noswizzle if ablation == "cuda_noswizzle" else [])

            def source(block, c, rules=rules):
                text = _ORIGINAL(block, c)
                for pattern, replacement in rules:
                    text, count = re.subn(pattern, replacement, text)
                    assert count or (ablation == "noconvert" and "to_f16x2(" not in pattern and "split_tf32" not in text)\
                        or (ablation == "noconvert" and "split_tf32" in pattern and "split_tf32(" not in text.split("apply_stages")[1])\
                        or (ablation == "noconvert" and "to_f16x2" in pattern and "to_f16x2(" not in text.split("apply_stages")[1]), (ablation, pattern)
                return text

            codegen.kernel_source = source
            # svpass caches kernels in memory by block and config, not by source.
            svpass_engine._compiled.clear()
            engine = Engine(cfg)
            kernels = [engine.compile(b.dominant_block).result() for b in blocks]
            state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
            result[ablation] = sum(timed(lambda: k.apply(state), engine.synchronize) for k in kernels) / (len(blocks) * t_bw)
            del state, kernels, engine
            release_device_memory()
        codegen.kernel_source = _ORIGINAL
        print(json.dumps({"circuit": name, "mode": args.mode, "config": config, "options": options,
                          "blocks": len(blocks), "mean_t_over_tbw": result}), flush=True)


if __name__ == "__main__":
    main()
