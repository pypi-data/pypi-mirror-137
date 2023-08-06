import numpy as np
from fantomatic_engine.generic import Sprite, ResourcesManager
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
from fantomatic_engine.generic.feedback import Feedbackable


class CollectibleSprite(Sprite, Feedbackable):
    def __init__(self, resources_manager: ResourcesManager, data):
        Sprite.__init__(self, resources_manager, data["name"])
        Feedbackable.__init__(self, resources_manager, {
            "sfx": "collectible_sfx",
            "message": data.get(
                "feedback", dict()).get("message", data["name"]),
            "image": data["name"]
        })

        self.set_name(data["name"])
        self.init_animation("default")
        self.init_collider_polygon()
        self.inventory_position = 1

        # for hidden object (given by bots) position may not be provided
        self.set_position(*data.get("position", [0, 0]))

        self.set_physics_config(CollidablePhysicsConfiguration({
            "solid": False,
        }))

        self.z_index = data.get("z_index", 1)
        self.collected = False
        self.id = data.get("id", data["name"])
        self.hidden = not not data.get("hidden")

    def set_collected(self, inventory_position):
        self.collected = True
        self.inventory_position = inventory_position

    def get_saved(self):
        return {
            "id": self.id,
            "collected": self.collected,
            "inventory_position": self.inventory_position,
        }

    def restore_saved(self, data):
        self.collected = data["collected"]
        self.inventory_position = data["inventory_position"]
