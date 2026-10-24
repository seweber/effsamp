import subprocess
r = subprocess.run(["pytest", "-q", "-m", "statistical", "tests"], cwd="/work/noisecirc", capture_output=True, text=True)
print("statistical ->", r.returncode)
print(r.stdout[-2500:], r.stderr[-1500:])
