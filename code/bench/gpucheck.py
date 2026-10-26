"""Check that CUDA initialises on the visible GPU and report the device (environment check)."""
import ctypes

lib = ctypes.CDLL("libcuda.so.1")
print("cuInit", lib.cuInit(0))
import cupy as cp

print(cp.cuda.runtime.getDeviceProperties(0)["name"].decode(), cp.cuda.runtime.runtimeGetVersion())
