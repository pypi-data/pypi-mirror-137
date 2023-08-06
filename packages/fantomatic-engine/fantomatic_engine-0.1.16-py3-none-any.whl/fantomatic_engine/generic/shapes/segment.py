from typing import Tuple
from ..physics import Collidable
import numpy as np
from ..vectors import vec2


@Collidable.register
class Segment(Collidable):
    def __init__(self, point_start: np.array, point_end: np.array):
        super().__init__()
        self.start = point_start
        self.end = point_end
        self.init_collider_polygon()
        self.pre_collision_ray = 0

    def handle_collision_event(self, e) -> np.array:
        return vec2()

    def init_collider_polygon(self):
        super().init_collider_polygon(np.array([self.start, self.end]))
