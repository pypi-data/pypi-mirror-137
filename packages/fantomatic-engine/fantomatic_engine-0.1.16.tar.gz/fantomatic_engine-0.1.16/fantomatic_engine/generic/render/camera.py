from typing import Tuple
from fantomatic_engine.generic.shapes import Rectangle
from fantomatic_engine.generic.vectors import vec2
import numpy as np


class Camera:
    def __init__(self, state):
        self.state = state
        self.position = vec2()

    def follow(self, position: np.array):
        focus = self.state["get_focus"]()
        bounds = self.state["get_bounds"]()

        cam_pos = position - (focus / 2)

        if cam_pos[0] < 0:
            cam_pos[0] = 0
        elif cam_pos[0] + focus[0] > bounds.right:
            cam_pos[0] = bounds.right - focus[0]

        if cam_pos[1] < 0:
            cam_pos[1] = 0
        elif cam_pos[1] + focus[1] > bounds.bottom:
            cam_pos[1] = bounds.bottom - focus[1]

        self.position = cam_pos
