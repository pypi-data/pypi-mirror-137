import functools
import time

import healpy as hp
from math import radians
import numpy as np


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer


def simulate_hitmap(theta1, theta2):
    nside=32
    npix = hp.nside2npix(nside)
    
    m = np.ones(npix)
    _, lat = hp.pix2ang(nside, np.arange(npix))
    m[lat < radians(theta1)] = 0
    m[lat > radians(theta2)] = 0

    m *= np.random.randint(1, 100, size=len(m))

    return m