import numpy as np
from fantomatic_engine.generic import Sprite, ResourcesManager
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
from fantomatic_engine.generic.feedback import Feedbackable


class LifeBonus(Sprite, Feedbackable):
    def __init__(self, resource_manager: ResourcesManager, data):
        Sprite.__init__(self, resource_manager, data["name"])
        Feedbackable.__init__(self, resource_manager, {
            "sfx": "life_bonus_sfx",
            "message": "Bonus vie +" + str(int(data["value"] * 100)) + "%",
            "image": data["name"]
        })

        self.set_name(data["name"])
        self.init_animation("default")
        self.init_collider_polygon()
        self.set_position(*data["position"])
        self.set_physics_config(CollidablePhysicsConfiguration({
            "solid": False,
        }))

        self.z_index = data.get("z_index", 1)

        self.value = data["value"]
        self.used = False

    def use(self):
        self.used = True

    def get_saved(self):
        return {
            "name": self.name,
            "position": [int(n) for n in self.position],
            "used": self.used,
        }

    def restore_saved(self, data):
        self.used = data["used"]
