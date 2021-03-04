
import numpy as np
import matplotlib.pyplot as plt
import os

import time
import functools


def timer(func):
    """Print the elapsed time of running the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Running {func.__name__} takes {run_time:.4f} seconds")
        return value

    return wrapper_timer


# cast the hamiltonian copy into a function
def copy_hamiltonian(H):

    if not isinstance(H, sisl.physics.Hamiltonian):
        raise TypeError("H must be a Hamiltonian object")
    a, b, c = H.shape
    h = np.empty([a, b, c])
    for i in range(a):
        for j in range(b):
            for k in range(c):
                h[i, j, k] = H[i, j, k]
    return h


def move_to_origo(gnr):
    """
    Move the geometry center to origin
    """

    gnr = gnr.translate([-gnr.center()[0], -gnr.center()[1], 0])
    plot(gnr)
    plt.axis("equal")

    return gnr

