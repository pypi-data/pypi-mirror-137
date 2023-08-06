from math import sqrt
from functools import reduce
import numpy as np
import random

NUL_FLOAT_THRESHOLD = 0.0000001

"""
2D vector operations
All vectors must be numpy arrays of length 2
"""


def unit(vector):
    """
    Returns the unit vector of a vector
    """
    m = magnitude(vector)
    if m == 0:
        return vec2()
    return vector / m


def sign_vec(vector):
    return np.sign(vector).astype(np.float)


def magnitude(vector):
    return np.linalg.norm(vector)


def has_unit_length(vector):
    return abs(1 - magnitude(vector)) < NUL_FLOAT_THRESHOLD


def float_is_nul(number):
    return abs(number) < NUL_FLOAT_THRESHOLD


def vec2(n1=0.0, n2=0.0) -> np.array:
    return np.array([n1, n2])


def vec_is_nul(vector):
    return float_is_nul(vector.dot(vector))


def normal_vecs(v):
    """
    Return 2 vectors for the 2 possible direction of a normal vector to v.
    """
    return (
        vec2(-v[1], v[0]),
        vec2(v[1], -v[0])
    )


def vecs_addition(vectors):
    return reduce(lambda total, vec: total + vec, vectors, vec2())


def vec_is_in_list(vec, vecs_list):
    if (len(vecs_list) == 0):
        return False
    for v in vecs_list:
        if np.array_equal(vec, v):
            return True
    return False


def random_point_in_area(area: np.array) -> np.ndarray:
    x, y, w, h = area
    return vec2(
        random.uniform(x, x+w),
        random.uniform(y, y+h)
    )
