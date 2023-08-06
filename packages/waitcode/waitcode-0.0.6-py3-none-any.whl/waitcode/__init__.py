from ctypes import *
import os

path = os.path.dirname(os.path.realpath(__file__))
path_lib = path + "/sleep.so"
so = CDLL(path_lib)


def wait(sec):
    so.wait(sec)
