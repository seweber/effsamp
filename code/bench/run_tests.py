import subprocess, sys
for args in (["pytest", "-q", "-x", "packages/svpass/tests"], ["pytest", "-q", "-x", "tests"]):
    r = subprocess.run(args, cwd="/work/noisecirc", capture_output=True, text=True)
    print(" ".join(args), "->", r.returncode)
    print(r.stdout[-1500:], r.stderr[-1500:])
