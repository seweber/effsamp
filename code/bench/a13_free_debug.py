"""A13 debug: GPU error kernels against svpass's NumPy device for single-error choice vectors (GHZ, 10 qubits)."""
import dataclasses
import sys

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator  # noqa: E402
from svpass import testing  # noqa: E402

options, config = configpatch.parse(sys.argv[1:])
configpatch.apply(config)
sim = Simulator(maps=noise.maps("damping", 0.05), **options)
compiled = sim._compiled(circuits.make("ghz", 10))[0]
engine = sim._engine(compiled.config)
ref_engine = testing.engine(dataclasses.replace(compiled.config, dtype="complex128"))
block = [b for b in compiled.blocks if b.has_choices][0]
general = block.engine_block
rng = np.random.default_rng(0)
amps = rng.normal(size=2**10) + 1j * rng.normal(size=2**10)
for flip in [None, 0, 3, 7]:
    host = np.zeros((general.n_operations, 1), dtype=np.int32)
    if flip is not None:
        host[flip, 0] = 1
    ref = ref_engine.states(amps[None, :])
    ref_engine.compile(general).result().apply(ref, ref_engine.upload(host))
    expected = ref.amplitudes[0]
    for label, eb in (("general", general), ("masked", block.masked_block), ("dominant", block.dominant_block)):
        if label == "dominant" and flip is not None:
            continue
        rows = np.concatenate([host, eb.stage_mask(host)]) if label == "masked" else host
        st = engine.states(amps.astype(np.complex64)[None, :])
        k = engine.compile(eb).result()
        k.apply(st) if label == "dominant" else k.apply(st, engine.upload(rows))
        out = st.amplitudes[0]
        print(flip, label, f"|out|={np.linalg.norm(out):.4f} |exp|={np.linalg.norm(expected):.4f} "
              f"err={np.linalg.norm(out - expected) / np.linalg.norm(expected):.2e} overlap={abs(np.vdot(out, expected)) / np.linalg.norm(out) / np.linalg.norm(expected):.4f}")
