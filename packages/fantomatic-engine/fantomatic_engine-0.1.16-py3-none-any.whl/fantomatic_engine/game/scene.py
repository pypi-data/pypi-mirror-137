import numpy as np
from fantomatic_engine.generic.shapes import Segment
from fantomatic_engine.generic.automation import BotSprite
from fantomatic_engine.generic.physics import CollidablePhysicsConfiguration
from fantomatic_engine.generic.image import Animation
from .sprites import DecorSprite, CollectibleSprite, LifeBonus, Bot, InteractableObject
from .door import Door
from typing import Tuple


class Scene:
    def __init__(self, data, resource_manager):
        r_m = resource_manager

        self.name = data["name"]

        if self.name == "none":
            self.create_none_scene()
            return

        self.game_starting_point = data.get("game_starting_point", False)
        self.game_title = data.get("game_title", False)
        self.game_generic = data.get("game_generic", False)
        self.disable_save = data.get("disable_save", False)
        self.disable_fade_out = data.get("disable_fade_out", False)
        self.could_be_replayed = data.get("could_be_replayed", False)
        self.background: Animation = r_m.get_animation_set(
            data.get("background"))[0]

        self.soundtrack = r_m.get_soundtrack(data.get("soundtrack"))

        self.walls = [
            Segment(*np.array(wall)) for wall in data.get("walls", list())
        ]

        for w in self.walls:
            w.set_physics_config(CollidablePhysicsConfiguration({
                "movable": False,
            }))

        self.type = data.get("type", "level")  # level or cinematic

        self.bots = np.array([
            Bot(r_m, bot) for bot in data.get("bots", list())
        ], dtype=Bot)

        self.decor_sprites = np.array([
            DecorSprite(r_m, ds) for ds in data.get("decor_sprites", list())
        ], dtype=DecorSprite)

        self.collectibles = np.array([
            CollectibleSprite(r_m, c) for c in data.get("collectibles", list())
        ], dtype=CollectibleSprite)

        self.life_bonuses = np.array([
            LifeBonus(r_m, lb) for lb in data.get("life_bonuses", list())
        ], dtype=LifeBonus)

        self.interactable_objects = np.array([
            InteractableObject(r_m, o) for o in data.get("interactable_objects", list())
        ], dtype=InteractableObject)

        self.spawns = np.array(data.get("spawns", [[0, 0]]))

        self.doors = np.array([
            Door(door_data)
            for door_data in data.get("doors", list())
        ], dtype=Door)

        self.auto_play = data.get("auto_play")

        self.cinematic_duration = data.get("cinematic_duration", 0) * 1000
        self.cinematic_destination_scene = data.get(
            "cinematic_destination_scene", "")
        self.cinematic_destination_spawn = data.get(
            "cinematic_destination_spawn", 0)
        self.cinematic_disable_skip = data.get("cinematic_disable_skip", False)

        self.on_first_complete: dict = data.get("on_first_complete")
        self.has_been_completed = False

        self.default_show_menu = data.get("default_show_menu", False)
        self.show_menu_after = data.get("show_menu_after", 0)

        if self.is_cinematic():
            self.background.rendering_options = self.background.rendering_options or dict()
            self.background.rendering_options.update({
                "use_max_height": True,
                "center_x": True,
                "ignore_camera": True
            })

    def create_none_scene(self):
        self.background = Animation({"name": "none"})
        self.soundtrack = None
        self.game_starting_point = True
        self.game_title = True
        self.game_generic = False
        self.disable_save = True
        self.disable_fade_out = True
        self.could_be_replayed = False

        self.walls = list()
        self.type = "none"
        self.bots = list()
        self.decor_sprites = list()

        self.collectibles = list()

        self.life_bonuses = list()

        self.interactable_objects = list()

        self.spawns = np.array([[0, 0]])

        self.doors = list()

        self.auto_play = False

        self.cinematic_duration = 0
        self.cinematic_destination_scene = ""
        self.cinematic_destination_spawn = 0

        self.on_first_complete = None
        self.has_been_completed = False

        self.default_show_menu = True
        self.show_menu_after = 0

        self.background.rendering_options = {
            "use_max_height": True,
            "center_x": True,
            "ignore_camera": True
        }

    def get_saved(self):
        return {
            "name": self.name,
            "interactable_objects": [o.get_saved() for o in self.interactable_objects],
            "collectibles": [o.get_saved() for o in self.collectibles],
            "life_bonuses": [lb.get_saved() for lb in self.life_bonuses],
            "cinematic_destination_scene": self.cinematic_destination_scene,
            "cinematic_destination_spawn": self.cinematic_destination_spawn,
        }

    def restore_saved(self, data):
        for obj in data["interactable_objects"]:
            current = next(
                (o for o in self.interactable_objects if o.id == obj["id"]), None)

            if current:
                current.restore_saved(obj)

        for col in data["collectibles"]:
            current = next(
                (o for o in self.collectibles if o.id == col["id"]), None)
            if current:
                current.restore_saved(col)

        for bonus in data["life_bonuses"]:
            current = next(
                (o for o in self.life_bonuses if (o.name == bonus["name"]
                                                  and np.array_equal(o.position, bonus["position"]))
                 ), None)
            if current:
                current.restore_saved(bonus)

        self.cinematic_destination_scene = data["cinematic_destination_scene"]
        self.cinematic_destination_spawn = data["cinematic_destination_spawn"]

    def update_cinematic_destination(self, scene_name, spawn_index):
        self.cinematic_destination_scene = scene_name
        self.cinematic_destination_spawn = spawn_index

    def is_cinematic(self):
        return self.type == "cinematic"

    def is_level(self):
        return self.type == "level"

    def is_none(self):
        return self.type == "none"

    def complete(self):
        self.has_been_completed = True

    def get_door_destination(self, door: Door) -> Tuple[str, int]:
        if (self.on_first_complete and not self.has_been_completed and door.complete_level):
            return (self.on_first_complete["destination_scene"],
                    self.on_first_complete.get("destination_spawn", 0))
        else:
            return (door.destination_scene,  door.destination_spawn)

    def get_spawn(self, index):
        return self.spawns[index]

    def get_visible_collectibles(self):
        return {c for c in self.collectibles if not c.collected and not c.hidden}

    def get_collectibles(self):
        return {c for c in self.collectibles if not c.collected}

    def get_interactables(self):
        return {
            *filter(lambda bot: bot.interactive, self.bots),
            *self.interactable_objects,
        }

    def get_life_bonuses(self):
        return {lb for lb in self.life_bonuses if not lb.used}

    def update_background(self):
        self.background.update_frame()

    def animation_is_finished(self):
        return self.background.play_once and self.background.finished
