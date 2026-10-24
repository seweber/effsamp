"""Print per-circuit trajectory times (sum of dominant / masked pass times) of a13_blocks.py run directories."""
import json, sys
for d in sys.argv[1:]:
    print("==", d.rstrip("/").split("/")[-1], open(f"{d}/status.txt").read().strip())
    for line in open(f"{d}/stdout.txt"):
        r = json.loads(line); per = r["per_block"]
        t = sum(b["t_dom"] for b in per); tm = sum(b["t_mask"] for b in per)
        print(f"{r['circuit']:10s} B={r['blocks']:3d} traj {1e3*t:7.2f} ms  mask {1e3*tm:7.2f} ms  ratio {t/r['blocks']/r['t_bw']:.2f} "
              f"ops {sum(b['fp_ops'] for b in per)/len(per):5.0f} sh {sum(b['shared'] for b in per)/len(per):5.1f}")
