import pygame
import os
import json
from .image.animation import Animation
from .sound import Sound
from typing import List, Set


class ResourcesManager:
    """
    A ResourceManager instance handles the loading and managing of all game resources. Animations, sounds etc
    """

    def __init__(self, resources_directory):
        self.resources_dir = resources_directory
        self.animations = dict()
        self.sounds = dict()
        self.scenes: List[dict] = list()
        self.soundtracks: Set[Sound] = set()
        self.sfx: Set[Sound] = set()
        self.character_config = dict()

    def load_resources(self):
        if self.resources_dir:
            self.load_animations()
            self.load_character_config()
            self.load_scenes()
            self.load_sounds()

    def load_animations(self):
        """
        Loads the project's animation resources from the resource/animations/index.json,
        creates a dictionary of Animations instances from the files data and write them in the
        self.animations field.
        """
        anims_index_file = open(os.path.join(
            self.resources_dir, "animations", "index.json"))

        anims_index = json.load(anims_index_file)

        animations = dict()
        for key in anims_index.keys():
            animations[key] = [Animation(dict(anim_data, **{
                "anim_file": (os.path.join(self.resources_dir, "animations", key, anim_data["file"])
                              if anim_data.get("file")
                              else None),
                "anim_folder":(os.path.join(self.resources_dir, "animations", key, anim_data["folder"])
                               if anim_data.get("folder")
                               else None),
            })) for anim_data in anims_index[key]]

        self.animations = animations

    def load_character_config(self):
        self.character_config = json.load(
            open(os.path.join(self.resources_dir, "character.json")))

    def load_scenes(self):
        scenes_dir_path = os.path.join(self.resources_dir, "scenes")
        for f_path in os.listdir(scenes_dir_path):
            f = open(os.path.join(scenes_dir_path, f_path), encoding="utf-8")
            data = json.load(f)
            self.scenes.append(data)

    def load_sounds(self):
        sounds_dir = os.path.join(self.resources_dir, "sounds")
        index_file = open(os.path.join(sounds_dir, "index.json"))

        index_data = json.load(index_file)

        for track in index_data["tracks"]:
            file_path = os.path.join(sounds_dir, "tracks", track["file"])
            audio = pygame.mixer.Sound(file_path)
            self.soundtracks.add(Sound({
                "name": track["name"],
                "audio": audio,
                "once": track.get("once", False)
            }))

        for sfx in index_data["sfx"]:
            file_path = os.path.join(sounds_dir, "sfx", sfx["file"])
            audio = pygame.mixer.Sound(file_path)
            self.sfx.add(Sound({
                "name": sfx["name"],
                "audio": audio,
                "once": True
            }))

    def get_animation_set(self, key) -> List[pygame.Surface]:
        """
        Returns a list of animations from the self.animations dict for the given key.
        """
        return self.animations.get(key) or [Animation({"name": "none"})]

    def get_soundtrack(self, name):
        return next((tr for tr in self.soundtracks if tr.name == name), None)

    def get_sfx(self, name):
        return next((fx for fx in self.sfx if fx.name == name), None)
