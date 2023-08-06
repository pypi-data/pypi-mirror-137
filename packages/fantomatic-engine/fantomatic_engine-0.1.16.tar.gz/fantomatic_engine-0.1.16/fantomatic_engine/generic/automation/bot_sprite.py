from .. import Sprite, ResourcesManager
from ..numbers import MAX_FLOAT
from ..vectors import (
    unit,
    vec2,
    random_point_in_area,
    vec_is_nul,
    sign_vec
)
from ..physics import CollidablePhysicsConfiguration
import numpy as np
import sys
import random


class PatternPlayerOptions:
    def __init__(self, data):
        self.positioning = data.get("positioning", "default")
        self.wait_frame_interval = data.get("wait_frame_interval", [0, 0])
        self.randomize_interval = data.get("randomize_interval", False)

        # x y width height
        self.area = np.array(data.get("area", [0, 0, 0, 0]))

    def get_wait_interval(self):
        if self.randomize_interval:
            return random.randint(*self.wait_frame_interval)
        else:
            return self.wait_frame_interval[1]


class BotSprite(Sprite):
    def __init__(self, resources_manager: ResourcesManager, data):
        super().__init__(resources_manager, data["name"])

        self.target_index = 0
        self.target_point = vec2()
        # will be dot product of velocity and moving direction.
        # Sign will change if target is reached
        self.direction_request = vec2()

        self.must_change_target = False

        self.set_pattern(data["pattern"])

        self.wait_frames = 0
        self.is_waiting = False
        self.set_name(data["name"])
        self.init_animation(data.get("init_animation", "default"))
        self.set_physics_config(CollidablePhysicsConfiguration(
            data.get("physics_config", dict())))

        # If True, animations named up down right and left must be provided
        self.use_directional_animations = data.get(
            "use_directional_animations", False)

        # If true, animation_stop and animation_move must be provided
        self.use_move_stop_animations = data.get(
            "use_move_stop_animations", False)

        self.animation_move: str = data.get("animation_move", "")
        self.animation_stop: str = data.get("animation_stop", "")

        # verif
        if self.use_directional_animations:
            assert all(anim_name in [
                anim.name for anim in self.animation_set
            ] for anim_name in [
                "up", "down", "right", "left"
            ]), "[ERROR] Directional animations not provided for bot sprite " + self.name

        self.combine_directional_animations = data.get(
            "combine_directional_animations", False)

        if self.combine_directional_animations:
            assert all(
                anim_name in [
                    "up_right", "up_left", "down_right", "down_left"
                ] for anim_name in [
                    anim.name for anim in self.animation_set
                ]
            ), "[ERROR] Combined directional animations not provided for bot sprite " + self.name

        self.freeze_animation_if_stopped = data.get(
            "freeze_animation_if_stopped", False)

    def set_pattern(self, pattern_data):
        self.initialized = False
        self.player_options = PatternPlayerOptions(
            pattern_data.get("options", dict()))

        assert pattern_data.get(
            "sequence") or pattern_data["options"]["area"], "Either pattern.sequence or pattern.options.area must be provided"

        sequence_data = pattern_data.get(
            "sequence") or [random_point_in_area(pattern_data["options"]["area"])]

        self.sequence = np.array(sequence_data)

        if vec_is_nul(self.position):  # set position only if not already set
            self.set_position(*self.sequence[0])

        self.pattern_type = pattern_data.get("type", "stand")

    def get_position_option(self):
        switcher = {
            "default": self.position,
            "center": self.get_center_position(),
        }
        return switcher[self.player_options.positioning]

    def get_sequence_closest_point_index(self):
        min_dist = MAX_FLOAT
        closest_point_index = 0
        position = self.get_position_option() + self.velocity
        for (i, pt) in enumerate(self.sequence):
            # If pattern changes, choose the closest point as a starting point
            pos_pt = position - pt
            dist = pos_pt.dot(pos_pt)
            if dist < min_dist:
                min_dist = dist
                closest_point_index = i
        return closest_point_index

    def update_direction_request(self):
        target_pt = self.target_point
        pos = self.get_position_option()
        self.direction_request = unit(target_pt - pos)
        self.direction_sign = (-1 if (pos - target_pt).dot(self.direction_request) < 0
                               else 1)

    def play_pattern(self):
        if not self.initialized:
            self.target_index = self.get_sequence_closest_point_index()
            self.target_point = self.sequence[self.target_index]
            self.update_direction_request()
            self.initialized = True

        self.move_to_target()

    def update_target_point(self):
        def get_sequence_next_point():
            prev_i = self.target_index
            seq = self.sequence

            self.target_index = prev_i + 1 if prev_i + 1 <= len(seq) - 1 else 0
            self.target_point = seq[self.target_index]

        def get_next_random_point():
            area = self.player_options.area
            self.target_point = random_point_in_area(area)

        def get_go_to_next_point():
            prev_i = self.target_index
            seq = self.sequence
            if prev_i == len(seq) - 1:
                return
            self.target_index = prev_i + 1
            self.target_point = seq[self.target_index]

        def get_random_in_loop():
            self.target_index = random.choice(
                [i for i in range(len(self.sequence)) if i != self.target_index])
            self.target_point = self.sequence[self.target_index]

        switcher = {
            "loop": get_sequence_next_point,
            "random": get_next_random_point,
            "stand": None,
            "go_to": get_go_to_next_point,
            "random_in_loop": get_random_in_loop,
        }

        update = switcher.get(self.pattern_type)

        if update:
            update()

    def move_to_target(self):
        target = self.target_point
        pos = self.get_position_option() + self.velocity
        dif = target - pos if self.direction_sign < 0 else pos - target
        if dif.dot(self.direction_request) <= 0:
            self.is_waiting = False
            wait_interval = self.player_options.get_wait_interval()
            if wait_interval > 0:
                if self.wait_frames < wait_interval:
                    self.wait_frames += 1
                    self.is_waiting = True
                else:
                    self.wait_frames = 0
                    self.is_waiting = False

            self.velocity = vec2()

            if self.is_waiting:
                self.push_move_request(vec2())
            else:
                self.update_target_point()
                self.update_direction_request()
        else:
            self.push_move_request(self.direction_request)

    def update_animation(self):
        if self.use_directional_animations and not vec_is_nul(self.velocity):
            anim_name = self.animation.name

            v = self.velocity
            sign_v = sign_vec(v)

            views = {
                "up": lambda:         np.array_equal(sign_v, (0,  -1)),
                "down": lambda:       np.array_equal(sign_v, (0,   1)),
                "right": lambda:      np.array_equal(sign_v, (1,   0)),
                "left": lambda:       np.array_equal(sign_v, (0,  -1)),
                "up_right": lambda:   np.array_equal(sign_v, (1,  -1)),
                "up_left": lambda:    np.array_equal(sign_v, (-1, -1)),
                "down_right": lambda: np.array_equal(sign_v, (1,   1)),
                "down_left": lambda:  np.array_equal(sign_v, (1,  -1)),
            } if self.combine_directional_animations else {
                "up": lambda:    v[1] < 0 and abs(v[1]) > abs(v[0]),
                "down": lambda:  v[1] > 0 and abs(v[1]) > abs(v[0]),
                "right": lambda: v[0] > 0 and abs(v[0]) > abs(v[1]),
                "left": lambda:  v[0] < 0 and abs(v[0]) > abs(v[1]),
            }

            for key in views:
                if views[key]():
                    anim_name = key
                    break

            self.set_animation(anim_name)
        elif self.use_move_stop_animations:
            if self.is_waiting:
                if self.animation.name != self.animation_stop:
                    self.set_animation(self.animation_stop)
            else:
                self.set_animation(self.animation_move)

        if not (vec_is_nul(self.velocity) and self.freeze_animation_if_stopped):
            super().update_animation()
