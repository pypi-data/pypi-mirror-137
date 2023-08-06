import ctypes
so = ctypes.CDLL('sleep.so')
wait = so.wait
