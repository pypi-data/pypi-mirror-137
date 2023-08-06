import numpy as np
from fantomatic_engine.generic import Sprite, ResourcesManager
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration


class DecorSprite(Sprite):
    def __init__(self, resources_manager: ResourcesManager, data):
        super().__init__(resources_manager, data["name"])
        self.set_name(data["name"])
        self.init_animation(data.get("animation", "default"))
        self.set_position(*data["position"])
        self.set_physics_config(CollidablePhysicsConfiguration({
            "solid": False,
        }))

        self.z_index = data.get("z_index", 1)
