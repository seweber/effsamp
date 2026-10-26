"""Run svpass's and noisecirc's test suites on the GPU without stopping at the first failure; print the failures."""
import subprocess

for args in (["pytest", "-q", "-rf", "packages/svpass/tests"], ["pytest", "-q", "-rf", "tests"]):
    r = subprocess.run(args, cwd="/work/noisecirc", capture_output=True, text=True)
    print(" ".join(args), "->", r.returncode)
    lines = r.stdout.splitlines()
    print("\n".join(line for line in lines if line.startswith(("FAILED", "ERROR"))))
    print("\n".join(lines[-3:]), r.stderr[-800:])
