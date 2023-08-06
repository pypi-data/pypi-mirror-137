from fantomatic_engine.generic import Sprite, ResourcesManager
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
import numpy as np
from fantomatic_engine.generic.vectors import magnitude, vec2, vec_is_nul
from .bot import Bot
from .collectible_sprite import CollectibleSprite
from .life_bonus import LifeBonus
from typing import List


class Character(Sprite):
    def __init__(self, resources_manager: ResourcesManager):
        super().__init__(resources_manager,
                         resources_manager.character_config.get("name", "fantom"))

        config = resources_manager.character_config
        name = config.get("name", "fantom")
        physics_config = config.get("physics_config", dict())
        self.init_animation("face")
        self.set_name(name)

        self.set_physics_config(CollidablePhysicsConfiguration({
            "motor_power": physics_config.get("motor_power", 1),
            "mass": physics_config.get("mass", 1),
        }))

        self.head_collider_calc_height_divisor = config.get(
            "head_collider_calc_height_divisor", 0)

        self.init_collider_polygon()
        self.z_index = 2
        self.state = {
            "pain": False,
            "dead": False,
            "lifebar": 1,
            "auto_play_target": 0,
            "auto_play_sequence": None,
            "auto_play_dir": vec2()
        }

        self.inventory = set()

    def reset(self, hard=False):
        self.state = {
            "pain": False,
            "dead": False,
            "lifebar": 1,
            "auto_play_target": 0,
            "auto_play_sequence": None,
            "auto_play_dir": vec2()
        }
        self.set_animation("face")
        self.push_move_request(vec2())
        self.set_velocity(vec2())

        if hard:
            self.inventory = set()

    def get_saved(self):
        return {
            "lifebar": self.state["lifebar"],
            "position": [int(n) for n in self.position],
            "inventory": [o.id for o in self.inventory]
        }

    def restore_saved(self, data, all_collectibles: List[CollectibleSprite]):
        self.state["lifebar"] = data["lifebar"]
        self.position = vec2(*data["position"])
        for c in all_collectibles:
            if c.id in data["inventory"]:
                self.store_collectible(c)

    def update_animation(self):
        anim_name = "face"

        front_views = {
            "face": lambda vec: abs(vec[0]) < min_vx,
            "right": lambda vec: vec[0] >= min_vx,
            "left": lambda vec: vec[0] <= -min_vx,
        }

        back_views = {
            "back": lambda vec: abs(vec[0]) < min_vx,
            "back_left": lambda vec: vec[0] <= -min_vx,
            "back_right": lambda vec: vec[0] >= min_vx,
        }

        def get_view_name(view_dict, vec):
            for name, cond in view_dict.items():
                if cond(vec):
                    return name

        mv = self.prev_move_request
        v = self.velocity
        min_v = 1.2
        min_vx = .5

        if self.state["dead"]:
            anim_name = "dead"
        elif self.state["pain"]:
            anim_name = "pain"
        elif magnitude(mv) != 0:
            views = back_views if mv[1] < 0 else front_views
            anim_name = get_view_name(views, mv)
        elif magnitude(v) < min_v:
            anim_name = "face"
        else:
            views = back_views if v[1] < 0 else front_views
            anim_name = get_view_name(views, v)

        self.set_animation(anim_name)
        self.update_animation_alpha()
        super().update_animation()

    def update_animation_alpha(self):
        min_alpha = 50

        if self.state["dead"]:
            # Make the dead anim gradually less transparent
            new_alpha = min(255, self.animation.alpha + 7)
        else:
            new_alpha = self.state["lifebar"] * 255

        self.animation.set_alpha(max(new_alpha, min_alpha))

    def get_collider(self, head_or_ground="ground"):
        if head_or_ground == "head" and self.head_collider_calc_height_divisor > 0:
            return self.collider_polygon.copy_translate(vec2(0,
                                                             -self.animation.dimensions[1] / self.head_collider_calc_height_divisor))
        return self.collider_polygon

    def apply_move_request(self, scale_motor=1):
        if not self.state["dead"]:
            super().apply_move_request(scale_motor)

    def apply_dammage(self, dammage):
        lifebar = self.state["lifebar"]
        lifebar -= dammage

        if lifebar <= 0:
            lifebar = 0
            self.state["dead"] = True

        self.state["lifebar"] = lifebar

    def apply_glue(self, glue_factor):
        self.set_velocity(self.velocity - (self.velocity * glue_factor))

    def update_velocity_transfer_priority(self):
        self.physics_config.update_velocity_transfer_priority((0 if vec_is_nul(self.prev_move_request)
                                                               else 2))

    def handle_bot_collisions(self):
        pain = False
        for bot in filter(lambda c: isinstance(c, Bot), self.collides_with):
            self.apply_dammage(bot.dammage)
            pain = bot.dammage > 0
            self.apply_glue(bot.glue_factor)
        self.state["pain"] = pain

    def store_collectible(self, collectible: CollectibleSprite):
        self.inventory.add(collectible)
        collectible.set_collected(len(self.inventory))

    def use_life_bonus(self, bonus: LifeBonus):
        self.state["lifebar"] = min(self.state["lifebar"] + bonus.value, 1)
        bonus.use()

    def has_collectible(self, collectible_id):
        return not not next((o for o in self.inventory if o.id == collectible_id), None)

    def consume_collectible(self, collectible_id):
        self.inventory.discard(
            next((o for o in self.inventory if o.id == collectible_id), None))

    def auto_play_sequence(self, sequence):
        is_end = False
        pos = self.get_center_position() + self.velocity
        current_seq = self.state["auto_play_sequence"]
        current_dir = self.state["auto_play_dir"]

        if not current_seq or not np.array_equal(current_seq, sequence):
            self.state["auto_play_sequence"] = sequence
            self.state["auto_play_target"] = 0

        index = self.state["auto_play_target"]
        target = sequence[index]

        dif = target - pos

        if dif.dot(current_dir) <= 0:
            if index + 1 <= len(sequence) - 1:
                new_index = index + 1
                self.state["auto_play_target"] = new_index
                target = sequence[new_index]
                self.state["auto_play_dir"] = target - pos
            else:
                is_end = True

        self.push_move_request(
            vec2() if is_end else self.state["auto_play_dir"])

    def clear_auto_play(self):
        if self.state["auto_play_sequence"]:
            self.state["auto_play_dir"] = vec2()
            self.state["auto_play_sequence"] = None
            self.state["auto_play_target"] = 0
