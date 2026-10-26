"""Print a16_check.py output (stdin) as a compact table: per workload and block, errors and pass times."""
import json
import sys

for line in sys.stdin:
    if not line.startswith("{"):
        continue
    r = json.loads(line)
    print(r["circuit"], r["options"], r["config"], f"t_bw={r['t_bw'] * 1e3:.3f} ms", f"compile={r['t_compile']:.1f}s")
    for b in r["blocks"]:
        print("  ", " ".join(f"{k}={v:.2e}" if isinstance(v, float) and "err" in k or "norm" in k
                             else f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}" for k, v in b.items()))
