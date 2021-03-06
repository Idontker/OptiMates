import numpy as np
from random import random
from geometrics.ikosaeder import ikosaeder

### Generating points on graph ###


def _create_point(r, theta, phi) -> np.ndarray:
    arr = np.array([r, theta, phi, 0, 0, 0])
    arr[3] = r * np.sin(theta) * np.cos(phi)
    arr[4] = r * np.sin(theta) * np.sin(phi)
    arr[5] = r * np.cos(theta)

    return arr


def gen_random_points(N) -> np.ndarray:
    return np.transpose(np.array([_create_random_point() for _ in range(N)]))


def _create_random_point() -> np.array:
    phi = random() * 2 * np.pi
    x = random() * 2 - 1
    theta = np.arccos(x)

    return _create_point(1, theta, phi)


def gen_iko_points(divisions=4):
    iko = ikosaeder()
    iko.subdivide(n=divisions)

    return np.transpose(iko.normalized_points())


def gen_archimedic_spiral(
    speed=100,
    N=1000,
    lower_bound=0,
    upper_bound=1,
) -> np.ndarray:
    """theta in [arccos(lower_bound), arccos(upperbound)]"""

    X = np.linspace(lower_bound, upper_bound, N)
    thetas = np.arccos(X)
    phis = speed * thetas

    # TODO: only cart
    arr = np.array(
        [
            np.ones(len(thetas)),
            thetas,
            phis,
            np.sin(thetas) * np.cos(phis),
            np.sin(thetas) * np.sin(phis),
            np.cos(thetas),
        ]
    )

    return arr


# sieht für mich nach der archimedischen Spirale aus mit speed L = sqrt(N*pi)
def gen_bauer_spiral(N) -> np.ndarray:
    L = np.sqrt(N * np.pi)
    k = np.array(range(1, N + 1))
    z = 1 - (2 * k - 1) / N
    phi = np.arccos(z)
    theta = L * phi
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)

    arr = np.array(
        [
            np.ones(N),
            phi,
            theta,
            np.sin(phi) * np.cos(theta),
            np.sin(phi) * np.sin(theta),
            z,
        ]
    )

    return arr
