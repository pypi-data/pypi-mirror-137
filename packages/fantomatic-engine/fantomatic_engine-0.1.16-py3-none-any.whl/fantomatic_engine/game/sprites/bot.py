from fantomatic_engine.generic.automation import BotSprite
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
from fantomatic_engine.generic.sound import Sound
from fantomatic_engine.generic.vectors import vec2, unit
from fantomatic_engine.generic import ResourcesManager
from ..interactable import Interactable
from time import time


class Bot(BotSprite, Interactable):
    def __init__(self, resources_manager: ResourcesManager, data):
        BotSprite.__init__(self, resources_manager, data)
        Interactable.__init__(self, data)

        self.init_collider_polygon()

        self.z_index = data.get("z_index", 1)
        self.flying = data.get("flying", False)
        self.dammage = data.get("dammage", 0)  # a number between 0 and 1

        self.glue_factor = data.get("glue_factor", 0)
        self.follow_factor = data.get("follow_factor", 0)
        self.magnet_factor = data.get("magnet_factor", 0)

        self.fps_factor = data.get("fps_factor", 1)

        physics_config = data.get("physics_config", dict())
        self.set_physics_config(CollidablePhysicsConfiguration(physics_config))

        self.lazy_collides_with = list()
        self.lazy_collision_time_offset = 800 if not self.flying else 0

        self.use_action_strict_collider = data.get(
            "use_action_strict_collider", False)

        self.collision_sfx: Optional[Sound] = resources_manager.get_sfx(
            data.get("collision_sfx", ""))

    def handle_character_maybe_collision(self, character):
        if self.is_colliding_with(character):
            self.move_request -= self.move_request * self.follow_factor

            if self.magnet_factor > 0:
                magnet_vec = unit(self.get_center_position() -
                                  character.get_center_position()) * self.magnet_factor
                character.push_velocity_correction(magnet_vec)

            if self.fps_factor != 1:
                use_fps = self.animation.fps * self.fps_factor
                self.animation.use_fps = use_fps
        else:
            self.animation.use_fps = self.animation.fps

    def is_colliding_with(self, collidable):
        return collidable in self.collides_with or collidable in [it["collidable"] for it in self.lazy_collides_with]

    def flush_collisions(self):
        super().flush_collisions()
        self.flush_lazy_collisions()

    def flush_lazy_collisions(self):
        now = time() * 1000
        to_flush = list()
        items = self.lazy_collides_with
        for item in items:
            if now - item["at"] > self.lazy_collision_time_offset:
                to_flush.append(item)

        self.lazy_collides_with = [it for it in items if it not in to_flush]

    def push_collision_with(self, collidable):
        super().push_collision_with(collidable)

        lazy_collision = {
            "collidable": collidable,
            "at": time() * 1000
        }

        already_colliding = next(
            (item for item in self.lazy_collides_with
             if item["collidable"] is collidable),
            None)

        if already_colliding:
            self.lazy_collides_with.remove(already_colliding)

        self.lazy_collides_with.append(lazy_collision)

    def freeze(self):
        self.push_move_request(vec2())
