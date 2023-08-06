import ctypes
import os

# os.system('gcc sleep.c -shared -o sleep.so')
so = ctypes.cdll.LoadLibrary('sleep.so')


def wait(sec):
    so.wait(sec)
