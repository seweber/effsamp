"""Override fields of svpass's kernel `Config` for every circuit noisecirc compiles in this process.

`noisecirc.circuit.CompiledCircuit` builds its `Config` (precision, pinned bytes) and passes its
`stage_qubits` to the fusion, so replacing the name `Config` there changes both the stages and the
kernels. Fields: stage_qubits, group_amplitudes, threads, min_registers (see svpass/config.py).
"""

from functools import partial

import noisecirc.circuit
from svpass import Config

_ORIGINAL = noisecirc.circuit.Config


def apply(overrides: dict) -> None:
    """Make every compiled circuit's `Config` take ``overrides``; an empty dict restores the defaults."""
    noisecirc.circuit.Config = partial(_ORIGINAL, **overrides) if overrides else _ORIGINAL
    # `Config.pinned_bytes` is read as a class attribute for the Simulator's default; keep it available.
    noisecirc.circuit.Config.pinned_bytes = Config.pinned_bytes  # type: ignore[attr-defined]


def parse(items: list[str]) -> tuple[dict, dict]:
    """Split ``key=value`` items into Simulator options and Config overrides."""
    # stage_qubits is a Simulator option since noisecirc's feature/autotune (CompiledCircuit passes it
    # explicitly, which would override a patched default), so it goes to the options.
    config_fields = {"group_amplitudes", "threads", "min_registers"}
    options, config = {}, {}
    for item in items:
        key, value = item.split("=")
        number = float(value) if ("." in value or value == "inf") else int(value)
        (config if key in config_fields else options)[key] = number
    return options, config
