import os
from pathlib import Path
from typing import Optional
from getopt import getopt
import json
import sys


class GameConfig:
    def __init__(self, argv):
        self.app_dir = Path(os.path.abspath(os.path.dirname(__file__))).parent

        # any writable data like config.json should be copied in there
        self.default_data_dir = self.get_default_data_path()

        # If a dynamic data directory path is provided it will be used first
        self.data_dir = self.find_or_make_data_dir()

        opts, _args = getopt(
            argv, "n:r:", ["game_name=", "resources_dir="])

        self.arg_opts = opts

        conf = self.get_conf()

        self.window_frame = conf.get("window_frame", True)
        self.window_fullscreen = conf.get("window_fullscreen", False)
        self.default_small_window_size = (800, 550)
        self.window_size = tuple(
            conf.get("window_size", self.default_small_window_size))

        self.lang = conf.get("lang", "en")

        self.game_name = (self.get_opt("n", "game_name")
                          or conf.get("game_name", "Fantomatic Engine"))

        self.resources_dir = (self.get_opt("r", "resources_dir")
                              or conf.get("resources_dir")
                              or self.get_maybe_resources_in_data_dir()
                              or "")

        if self.resources_dir:
            assert os.path.isdir(self.resources_dir), \
                "A valid resources directory path is required. Got: " + \
                str(self.resources_dir)

        self.no_resources = not self.resources_dir

        if self.no_resources:
            print("[WARNING] No game resources were found")

        self.save_file = os.path.join(self.default_data_dir, "save.json")

        self.translations_file = os.path.join(self.data_dir,
                                              "translations.json")

        self.disable_change_resources_dir = conf.get(
            "disable_change_resources_dir", False)

        self.disable_light = conf.get("disable_light", False)

        self.create_default_config_file()

    def get_maybe_resources_in_data_dir(self) -> Optional[str]:
        resources_in_data_dir_path = os.path.join(self.data_dir, "resources")

        if os.path.isdir(resources_in_data_dir_path):
            return str(resources_in_data_dir_path)

        return None

    def get_default_data_path(self):
        home_dir = os.path.abspath(Path.home())
        return os.path.join(home_dir, ".fantomatic_data")

    def find_or_make_data_dir(self):
        def find_data_dir(root) -> (str, bool):
            data_dir = os.path.join(root, ".fantomatic_data")
            return (data_dir, os.path.isdir(data_dir))

        exec_dir = os.getenv("EXEC_DIR")
        data_dir_path = ""

        for pth in (exec_dir,  # Exec dir is provided so data dir could be inside it or be a virtual dir inside a onefile binary
                    self.app_dir):  # a data directory can be provided in dev mode, in local source directory
            if pth:
                (data_dir, exists) = find_data_dir(pth)
                if exists:
                    data_dir_path = data_dir
                    break

        if not data_dir_path:
            data_dir_path = self.default_data_dir

        if not os.path.isdir(data_dir_path):
            os.mkdir(data_dir_path)

        return data_dir_path

    def create_default_config_file(self):
        if not self.default_conf_exists():
            default_conf_data = {
                "window_fullscreen": self.window_fullscreen,
                "window_frame": self.window_frame,
                "window_size": self.window_size,
                "resources_dir": "",
                "disable_change_resources_dir": self.disable_change_resources_dir,
                "disable_light": self.disable_light,
                "game_name": self.game_name,
                "lang": self.lang
            }

            self.write_conf(default_conf_data)

    def get_conf(self):
        default_conf_path = os.path.join(self.default_data_dir, "config.json")

        if os.path.isfile(default_conf_path):
            return json.load(open(default_conf_path, encoding="utf-8"))
        else:
            dyn_conf_path = os.path.join(self.data_dir, "config.json")

            if os.path.isfile(dyn_conf_path):
                return json.load(open(dyn_conf_path, encoding="utf-8"))
            else:
                return dict()

    def default_conf_exists(self):
        return os.path.isfile(os.path.join(self.default_data_dir, "config.json"))

    def translations_available(self):
        return os.path.isfile(self.translations_file)

    def write_conf(self, data: dict):
        if not os.path.isdir(self.default_data_dir):
            os.mkdir(self.default_data_dir)

        f = open(os.path.join(self.default_data_dir, "config.json"),
                 "w", encoding="utf-8")

        f.write(json.dumps(data))

    def write_conf_key(self, key, value):
        conf = self.get_conf()
        conf[key] = value
        self.write_conf(conf)

    def get_opt(self, shortopt, longopt):
        for opt, arg in self.arg_opts:
            if opt in {"-"+shortopt, "--"+longopt}:
                return arg or True
        return None
