from typing import Tuple
from ..vectors import has_unit_length, unit, vec2


class Controllable:
    def __init__(self):
        self.move_request = vec2()
        self.prev_move_request = vec2()

    def push_move_request(self, reqvec: Tuple[float, float]):
        """
        Updates the move request state if the instance with a 2D unit vector
        """
        self.move_request = unit(reqvec)

    def has_moving_force(self):
        return has_unit_length(self.move_request)
