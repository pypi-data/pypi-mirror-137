from ctypes import *

# os.system('gcc sleep.c -shared -o sleep.so')
so = CDLL("sleep.so")


def wait(sec):
    so.wait(sec)
