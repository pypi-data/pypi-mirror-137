import pygame
import numpy as np
from typing import Tuple
from .shapes import Rectangle
from .vectors import vec_is_nul, vec2
from .image.animation import Animation
from .physics.collidable_physics_configuration import CollidablePhysicsConfiguration
from .physics import Collidable
from .control import Controllable
from .resources_manager import ResourcesManager


@Collidable.register
class Sprite(Collidable, Controllable):
    """
    A sprite abstraction holding data for animation, position, physics configuration, etc.
    Sprite is an abstract class and must be extended in order to create a real sprite.
    """

    def __init__(self, resources_manager: ResourcesManager, anim_name: str):
        """
        All the field are declared with their type but not initialized.
        They must be initialized in the extended class.
        """
        super().__init__()

        # A reference of the set of animations available for this sprite.
        self.animation_set = resources_manager.get_animation_set(anim_name)
        self.animation: Animation  # Must be set in child class
        self.z_index = 1  # Rendering priority index, should be customized in child class

    def init_animation(self, key):
        """
        Initialize the current animation.
        """
        anim = next((a for a in self.animation_set if a.name == key), None)
        if anim:
            self.animation = anim
        else:
            print("[WARNING] Animation " + key +
                  " was not found for sprite " + self.name)

            self.animation = (self.animation if hasattr(self, "animation")
                              else self.animation_set[0])

    def set_animation(self, key):
        """
        Updates the current animation and changes collider if needed
        """
        if ((key == self.animation.name
             and not self.animation.finished)
                or (self.animation.play_once
                    and not self.animation.finished)):
            return

        anim = next((a for a in self.animation_set if a.name == key), None)

        if not anim:
            return

        anim.reset()

        prev_collider = np.copy(self.animation.collider)
        prev_alpha = self.animation.alpha

        if prev_alpha < 255:
            anim.set_alpha(prev_alpha)

        self.animation = anim

        if not np.array_equal(prev_collider, self.animation.collider):
            super().init_collider_polygon(self.animation.collider)

    def init_collider_polygon(self):
        if not hasattr(self, "animation"):
            raise AttributeError(
                "Animation field must be initialized before collider_polygon")

        super().init_collider_polygon(self.animation.collider)

    def update_position(self):
        """
        Applys velocity vector state on position.
        """

        self.fix_min_speed_threshold()

        super().update_position()

    def get_motor(self):
        return self.move_request * self.physics_config.motor_power

    def apply_move_request(self, scale_motor=1):
        """
        Updates velocity by adding a calculated moving motor force
        """
        motor = self.get_motor() * scale_motor
        self.prev_move_request = self.move_request
        if not vec_is_nul(motor):
            self.set_velocity(self.velocity + motor)
            self.move_request = vec2()

    def fix_min_speed_threshold(self):
        v = self.velocity
        if vec_is_nul(self.move_request) and v.dot(v) < self.physics_config.min_speed ** 2:
            self.velocity = vec2()

    def update_animation(self):
        """
        Updates the current animation frame
        """
        self.animation.update_frame()
