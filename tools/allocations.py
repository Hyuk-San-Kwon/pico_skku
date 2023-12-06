import gc
import os
import machine

s = os.statvfs('/')
def print_mem():
    print(f"Free storage: {s[0]*s[3]/1024} KB")
    print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
