"""A14: summarize a14_check.py output: max deviation and per-circuit sums of pass times, base vs variant."""
import json, sys
for path in sys.argv[1:]:
    for line in open(path):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        for kind in ("dom", "mask"):
            b = [x for x in r["blocks"] if x["kind"] == kind]
            if not b:
                continue
            tb = sum(x["t_base"] for x in b); tv = sum(x["t_variant"] for x in b)
            ob = sum(x["work_base"]["fp_ops"] for x in b) / len(b); ov = sum(x["work_variant"]["fp_ops"] for x in b) / len(b)
            print(f"{r['circuit']:10s} {kind:4s} blocks {len(b):3d} dev {max(x['deviation'] for x in b):.1e} "
                  f"time {1e3*tb:7.2f} -> {1e3*tv:7.2f} ms ({tv/tb:.3f})  fp/amp {ob:5.0f} -> {ov:5.0f}")
