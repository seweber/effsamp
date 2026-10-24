"""A12: minimize E + w mu over all Kraus sets (rank and rank+2 operators) for weights w = 0, 1, 5, 50, against the lower bound; one-qubit channels at p = 0.01. Usage: a12_weights.py kind [kind ...]. Output: data/a12-kraus/weights-p0.01-1q.txt."""
import sys, time; sys.path.insert(0, "/itp3/home/sebastian/effsamp/code/bench")
import numpy as np
from a12_kraus import *
p = 1e-2
for kind in sys.argv[1:]:
    K = channel(kind, p)
    mc = metrics(canonical(K))
    print(f"{kind:13s} canonical: E/p={mc['E']/p:.4f} mu/p={mc['mu']/p:.4f} mu_max/p={mc['mu_max']/p:.4f} n={mc['n']} ||E(I)||-1={(np.linalg.eigvalsh(sum(k@k.conj().T for k in K))[-1]-1)/p:.4f}", flush=True)
    for w in (0.0, 1.0, 5.0, 50.0):
        t=time.time()
        lb = lower_bound(K, w, starts=6)
        ops, m = optimize(K, w, extra=0, starts=8)
        ops1, m1 = optimize(K, w, extra=2, starts=8)
        print(f"   w={w:5.1f}: LB J/p={lb['J']/p:.4f} (E>={lb['E_bound']/p:.4f} mu={lb['mu']/p:.4f}) | opt J/p={(m['E']+w*m['mu'])/p:.4f} E/p={m['E']/p:.4f} mu/p={m['mu']/p:.4f} dom={m['dom']} | +2op J/p={(m1['E']+w*m1['mu'])/p:.4f} E/p={m1['E']/p:.4f} mu/p={m1['mu']/p:.4f} dom={m1['dom']} [{time.time()-t:.0f}s]", flush=True)
