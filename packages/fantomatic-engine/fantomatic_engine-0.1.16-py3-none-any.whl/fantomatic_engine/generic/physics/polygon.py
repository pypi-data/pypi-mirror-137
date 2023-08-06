from itertools import zip_longest
from typing import Tuple, Optional
from ..vectors import vec2
import numpy as np


class Polygon:
    def __init__(self, points: np.array, segments=np.array([])):
        self.points = points

        # There must be a better way to do this with numpy ...
        self.segments = segments if len(segments > 0) else np.array(
            tuple(self.get_segments()))

        sum_points = vec2()
        for pt in points:
            sum_points += pt

        self.center = sum_points * (1 / len(points))

    def get_segments(self):
        pts_len = len(self.points)
        for i in range(0, pts_len):
            yield (self.points[i], self.points[i + 1 if i + 1 < pts_len else 0])

    def copy_translate(self, vec):
        return Polygon(self.points + vec, self.segments + vec)
