from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
from fantomatic_engine.generic import Sprite, ResourcesManager
from ..interactable import Interactable


class InteractableObject(Sprite, Interactable):
    def __init__(self, resource_manager: ResourcesManager, data):
        Sprite.__init__(self, resource_manager, data["name"])
        Interactable.__init__(self, data)

        self.init_animation(data.get("init_animation", "default"))
        self.init_collider_polygon()
        self.set_position(*data["position"])
        self.set_name(data["name"])
        self.z_index = data.get("z_index", 1)

        self.set_physics_config(
            CollidablePhysicsConfiguration({"movable": False}))

    def get_saved(self):
        return {
            "id": self.id,
            "disabled": self.disabled,
            "animation": self.animation.name
        }

    def restore_saved(self, data):
        self.disabled = data["disabled"]
        self.set_animation(data["animation"])
