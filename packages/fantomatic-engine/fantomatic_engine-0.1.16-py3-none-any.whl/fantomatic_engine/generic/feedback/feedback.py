from ..resources_manager import ResourcesManager
import pygame
from typing import Optional


class Feedback:
    def __init__(self, resource_manager: ResourcesManager, data: dict):
        self.sfx = data.get("sfx", "")
        self.message = data.get("message", "")
        self.image: Optional[pygame.Surface]
        if data.get("image"):
            anim_set = resource_manager.get_animation_set(data["image"])
            self.image = next(
                (anim for anim in anim_set if anim.name == "feedback"), anim_set[0])
        else:
            self.image = None
