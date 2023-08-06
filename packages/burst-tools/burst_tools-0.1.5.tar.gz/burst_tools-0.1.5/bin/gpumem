#!/usr/bin/env python3
import sys
import argparse
from pynvml import *

nvmlInit()

#get mem stats
def mem(dev=0):
    h = nvmlDeviceGetHandleByIndex(dev)
    info = nvmlDeviceGetMemoryInfo(h)
    return info.used, info.free, info.total

#opine on least-used aka best to use
def least_used():
    devs = nvmlDeviceGetCount()
    best = None
    freest = -1
    for dev in range(devs):
        used, free, tot = mem(dev)
        if free > freest:
            freest = free
            best = dev
    return best, freest

if __name__ == "__main__":
    best, free = least_used()
    print (f"dev {best} has most free memory: {free/1000000:.3f}mb")
    dev = 0
    if len(sys.argv) > 1:
        dev = int(sys.argv[1])
    devs = nvmlDeviceGetCount()
    if dev >= devs:
        raise Exception(f"No such device; {devs} devices available")
    used, free, tot = mem(dev)
    print (f"stats for device {dev}:")
    print (f"{used/tot:.3%} {used/1000000:.3f}mb out of {tot/1000000:.3f}mb free: {free/1000000:.3f}mb")