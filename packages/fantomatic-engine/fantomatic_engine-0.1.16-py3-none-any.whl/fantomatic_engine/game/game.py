import pygame
import os
import time
from typing import Optional, Dict
import json
from _thread import start_new_thread
from fantomatic_engine.generic.control.inputs import QuadridirectionalInput
from fantomatic_engine.generic.light import LightHalo
from fantomatic_engine.generic import Render, ResourcesManager
from fantomatic_engine.generic.menu import Menu, MenuItem, MenuSession
from fantomatic_engine.generic.events import EventsHandler, AnyListener
from fantomatic_engine.generic.vectors import vec2
from fantomatic_engine.generic.sound import Sound
from fantomatic_engine.generic.feedback import Feedback
from fantomatic_engine.generic.timing import Timer, MainLoopFrameRateController

from .interactions_manager import InteractionsManager
from .sound_player import SoundPlayer
from .scene import Scene
from .sprites import Character, Bot
from .config import GameConfig
from .lang import Translator
from .skip_cinematic_listener import SkipCinematicListener


class Game:
    def __init__(self, config: GameConfig, win_data: dict, ready_state: dict):
        self.config = config
        self.resources_manager = ResourcesManager(self.config.resources_dir)
        self.resources_manager.load_resources()
        r_m = self.resources_manager

        self.character = Character(r_m)

        self.cinematic_timer = Timer()
        self.main_loop_rate_controller = MainLoopFrameRateController(30)
        self.apply_rate_reduction = self.main_loop_rate_controller.get_rate_reduction_factor()

        self.scenes = {Scene(s_data, r_m) for s_data in r_m.scenes}

        if len(self.scenes) == 0:
            self.scenes = {Scene({"name": "none"}, r_m)}

        self.sound_state: Dict[Optional[Sound]] = {
            "soundtrack": None,
            "bot_fx": None,
            "feedback_fx": None,
        }

        self.sound_player = SoundPlayer(
            {"get_sound_state": lambda: self.sound_state})

        self.show_menu_after = {
            "active": False,
            "frames": 0,
            "duration": 0,
        }

        title_scene = next(s for s in self.scenes if s.game_title)
        self.set_scene(title_scene.name, 0, True)

        self.character.set_position(*self.scene.get_spawn(0))

        light_resource = r_m.get_animation_set("light")[0]

        self.light_halo: Optional[LightHalo] = LightHalo({
            "get_render_size": lambda: self.render.drawing_surface.get_size()
        }, light_resource) if not config.disable_light and not light_resource.is_none else None

        self.interactions_manager = InteractionsManager({
            "get_scene": self.get_scene,
            "push_pending_set_scene": self.push_pending_set_scene,
            "push_feedback": self.push_feedback,
            "character": self.character,
            "resources_manager": self.resources_manager
        })

        self.arrows_input = QuadridirectionalInput()

        self.quit = False

        self.events_handler = EventsHandler(listeners={
            "keyboard": (
                self.arrows_input,
                self.interactions_manager.action_events_listener,
                SkipCinematicListener(self.handle_skip_cinematic),
                SkipCinematicListener(self.handle_skip_feedback),
            ),
            "quit": (
                AnyListener(self.handle_quit_event),
            ),
            "escape": (
                AnyListener(self.handle_toggle_menu),
            )
        })

        self.pending_scene = None
        self.pending_feedback: Optional[Feedback] = None
        self.pending_soundtrack: Optional[Sound] = None

        self.feedback_state = {
            "feedback": None,
            "frames": 0,
            "duration": 90,
        }

        self.menu_notification_state = {
            "text": "",
            "frames": 0,
            "duration": 70,
            "keep_alive": False
        }

        self.translator = Translator(self.config)
        t = self.translator.trad

        self.menu_state = "base"

        self.menu_items_descriptors = (
            {
                "text": t("Continue"),
                "callback": self.handle_toggle_menu,
                "cond": lambda: (self.menu_state == "base"
                                 and not self.scene.is_none()
                                 and not self.scene.game_title),
            },
            {
                "text": t("New game"),
                "callback": self.handle_new_game,
                "cond": lambda: self.menu_state == "base" and not self.config.no_resources,
            },
            {
                "text": t("Load save"),
                "callback": self.handle_load_game,
                "cond": lambda: (self.menu_state == "base"
                                 and self.has_available_saved_game()
                                 and not self.config.no_resources),
            },
            {
                "text": t("Save game"),
                "callback": self.handle_save_game,
                "cond": lambda: (self.menu_state == "base"
                                 and not self.config.no_resources
                                 and not self.scene.disable_save)
            },
            {
                "text": t("Configuration"),
                "callback": lambda: self.handle_menu_change_state("config"),
                "cond": lambda: self.menu_state == "base",
            },
            {
                "text": t("Quit"),
                "callback": self.handle_quit_event,
                "cond": lambda: self.menu_state == "base",
            },
            # Config menu items
            {
                "text": "-- "+t("Configuration")+" --",
                "cond": lambda: self.menu_state == "config" and not self.menu.browse_files,
                "read_only": True,
            },
            {
                "text": t("Full screen mode"),
                "callback": lambda: self.handle_set_fullscreen_mode(True),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and not self.config.window_fullscreen),
                "secondary": True,
            },
            {
                "text": t("Small window"),
                "callback": lambda: self.handle_set_window_size("small"),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and not self.config.window_fullscreen
                                 and self.config.window_size == (-1, -1)),
                "secondary": True,
            },
            {
                "text": t("Large window"),
                "callback": lambda: self.handle_set_window_size("large"),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and not self.config.window_fullscreen
                                 and self.config.window_size != (-1, -1)),
                "secondary": True,
            },
            {
                "text": t("Window mode"),
                "callback": lambda: self.handle_set_fullscreen_mode(False),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and self.config.window_fullscreen),
                "secondary": True,
            },
            {
                "text": t("Disable light effect"),
                "callback": lambda: self.handle_toggle_light_effect(True),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and not self.config.disable_light),
                "secondary": True,
            },
            {
                "text": t("Enable light effect"),
                "callback": lambda: self.handle_toggle_light_effect(False),
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and self.config.disable_light),
                "secondary": True,
            },
            {
                "text": t("Select game data"),
                "callback": self.handle_menu_browse_files,
                "cond": lambda: (self.menu_state == "config"
                                 and not self.menu.browse_files
                                 and not self.config.disable_change_resources_dir),
                "secondary": True,
            },
            {
                "text": t("Back"),
                "callback": lambda: self.handle_menu_change_state("base"),
                "cond": lambda: self.menu_state == "config" and not self.menu.browse_files,
            },
            # Configuration file explorer
            {
                "text": "-- " + t("Browse files") + " --",
                "read_only": True,
                "cond": lambda: self.menu_state == "config" and self.menu.browse_files,
            },
            {
                "text": t("Browse directory") + ": ->" + " | " + t("Parent directory") + ": <-",
                "read_only": True,
                "small": True,
                "cond": lambda: self.menu_state == "config" and self.menu.browse_files,
            },
            {
                "text":  t("Select directory") + ": " + t("Enter") + " | " + t("Cancel") + ": " + t("Escape"),
                "read_only": True,
                "small": True,
                "cond": lambda: self.menu_state == "config" and self.menu.browse_files,
            },
        )

        self.menu_session = MenuSession(self.get_menu_items())

        self.menu = Menu({
            "get_items": lambda: self.menu_session.items,
            "before_refresh_items": self.refresh_menu_session,
            "on_escape": self.handle_toggle_menu,
            "on_quit": self.handle_quit_event,
            "select_resources_directory": self.handle_set_resources_directory,
        })

        self.fade_state = {
            "fading": False,
            "frames": 0,
            "duration": 35,
        }

        win_flag = (pygame.FULLSCREEN if config.window_fullscreen
                    else pygame.NOFRAME if not config.window_frame
                    else 0)

        surf_size = ((0, 0) if config.window_fullscreen
                     else config.window_size if config.window_size != (-1, -1)
                     else (win_data["screen_w"] - 2*win_data["margin"],
                           win_data["screen_h"] - 2*win_data["margin"]))

        ready_state["ready"] = True

        self.render = Render(pygame.display.set_mode(surf_size, win_flag))

        if self.scene.is_none():
            self.push_menu_notification(self.translator.trad(
                "No game data loaded.\nPlease select a directory in the configuration menu."))

    def handle_new_game(self):
        self.reset_state()

        starting_scene = next(s for s in self.scenes if s.game_starting_point)
        self.set_scene(starting_scene.name, 0)

        self.character.reset(True)

        r_m = self.resources_manager
        self.scenes = {Scene(s_data, r_m) for s_data in r_m.scenes}

        self.menu.close()

    def handle_save_game(self):
        save_file = open(self.config.save_file, "w")

        save_data = {
            "scene": self.scene.name,
            "scenes": [s.get_saved() for s in self.scenes],
            "character": self.character.get_saved(),
        }

        save_file.write(json.dumps(save_data))

        self.push_menu_notification(self.translator.trad("Game saved!"))

    def push_menu_notification(self, text, keep_alive=False):
        max_chars_per_line = 60
        lines = text.split("\n")
        if any(len(l) > max_chars_per_line for l in lines):
            new_lines = list()
            for line in lines:
                if len(line) < max_chars_per_line:
                    new_lines.append(line)
                else:
                    split_line = line.split()
                    tmp_line = ""
                    for w in split_line:
                        if len(tmp_line + w) < max_chars_per_line:
                            tmp_line += w + " "
                        else:
                            new_lines.append(tmp_line.strip())
                            tmp_line = w + " "
                    new_lines.append(tmp_line.strip())
            text = "\n".join(new_lines)

        self.menu_notification_state["text"] = text
        self.menu_notification_state["frames"] = 0
        self.menu_notification_state["keep_alive"] = keep_alive

    def handle_menu_browse_files(self):
        self.menu.set_browse_files(True)

    def handle_load_game(self):
        if self.has_available_saved_game():
            json_data = open(self.config.save_file)
            data = json.load(json_data)

            self.reset_state()
            self.character.reset()
            self.set_scene(data["scene"], 0)

            for scene in filter(lambda s: (not s.game_title
                                           and not s.game_starting_point
                                           and not s.game_generic),
                                self.scenes):
                saved_scene = next(
                    s for s in data["scenes"] if s["name"] == scene.name)
                scene.restore_saved(saved_scene)

            all_collectibles = list()
            for s in self.scenes:
                for c in s.collectibles:
                    all_collectibles.append(c)

            self.character.restore_saved(
                data["character"], all_collectibles)

            self.menu.close()

    def handle_set_fullscreen_mode(self, value):
        self.config.write_conf_key("window_fullscreen", value)
        self.push_change_conf_notif()

    def handle_toggle_light_effect(self, value):
        self.config.write_conf_key("disable_light", value)
        self.push_change_conf_notif()

    def handle_set_window_size(self, pseudo_value):
        sw = {
            "large": (-1, -1),
            "small": self.config.default_small_window_size,
        }
        self.config.write_conf_key("window_size", sw[pseudo_value])
        self.push_change_conf_notif()

    def handle_set_resources_directory(self, path):
        self.push_menu_notification(
            self.translator.trad("Data validation, please wait ..."), keep_alive=True)
        self.menu.set_freeze(True)
        self.menu_session.resources_directory_settings.pending_validation = path

    def handle_pending_resources_directory_validation(self):
        if self.menu_session.resources_directory_settings.pending_validation:
            start_new_thread(self.validate_pending_resources_directory, ())

    def handle_pending_resources_directory_notification(self):
        if self.menu_session.resources_directory_settings.pending_success:
            self.push_change_conf_notif()
            self.menu_session.reset_resources_dir_settings()
        elif self.menu_session.resources_directory_settings.pending_error:
            self.push_menu_notification(self.translator.trad("Error - invalid data directory")
                                        + "\n"
                                        + self.menu_session.resources_directory_settings.pending_error)
            self.menu_session.reset_resources_dir_settings()

    def validate_pending_resources_directory(self):
        error = None
        try:
            path = self.menu_session.resources_directory_settings.pending_validation
            self.menu_session.clear_resources_dir_pending_validation()
            tmp_rm = ResourcesManager(path)
            tmp_rm.load_resources()
        except Exception as e:
            error = e

        if not error:
            self.config.write_conf_key("resources_dir", str(path))
            self.menu_session.set_resources_directory_pending_notification(
                "success", "")
            self.menu.on_escape_file_explorer()
        else:
            self.menu_session.set_resources_directory_pending_notification(
                "error", str(error))

        self.menu.set_freeze(False)

    def push_change_conf_notif(self):
        self.push_menu_notification(self.translator.trad(
            "Modifications saved.\nRestart the game to see the changes."))

    def has_available_saved_game(self):
        return os.path.exists(self.config.save_file)

    def reset_state(self):
        self.sound_state = {
            "soundtrack": None,
            "bot_fx": None,
            "feedback_fx": None,
        }

        self.pending_scene = None
        self.feedback_state["feedback"] = None
        self.feedback_state["frames"] = 0
        self.menu_notification_state["text"] = ""
        self.menu_notification_state["keep_alive"] = False
        self.interactions_manager.clear()

    def handle_toggle_menu(self):
        if not self.menu.show:
            self.refresh_menu_session()
            if self.scene.is_cinematic() and self.scene.soundtrack and not self.scene.soundtrack.loops:
                self.sound_state["soundtrack"].pause()
        else:
            self.handle_menu_change_state("base")
            if self.sound_state["soundtrack"]:
                self.sound_state["soundtrack"].unpause()

        self.menu.toggle()

    def refresh_menu_session(self):
        self.menu_session.set_items(self.get_menu_items())

    def handle_menu_change_state(self, state_name):
        self.menu_state = state_name
        self.menu.refresh_items()

    def get_menu_items(self):
        return [MenuItem(
            it["text"],
            it.get("callback"),
            {
                "secondary": it.get("secondary", False),
                "read_only": it.get("read_only", False),
                "small": it.get("small", False),
            }
        ) for it in self.menu_items_descriptors if it["cond"]()]

    def handle_skip_cinematic(self):
        if self.scene.is_cinematic() and not self.scene.cinematic_disable_skip:
            if self.scene.background.play_once:
                self.scene.background.skip()
            else:
                self.handle_cinematic_finished()
            self.sound_state["soundtrack"] = None

    def handle_skip_feedback(self):
        feedback = self.feedback_state["feedback"]
        if feedback and feedback.image:
            self.feedback_state["feedback"] = None

    def handle_quit_event(self):
        self.quit = True

    def get_sprites(self):
        scene = self.scene
        return [
            self.character,
            *self.get_scene_bots(),
            *scene.decor_sprites,
            *scene.get_visible_collectibles(),
            *scene.get_life_bonuses(),
            *self.get_scene_interactable_objects(),
        ] if scene.is_level() else []

    def get_scene_bots(self):
        return {bot for bot in self.scene.bots if bot.should_spawn(self.character)}

    def get_scene_interactable_objects(self):
        return {o for o in self.scene.interactable_objects if o.should_spawn(self.character)}

    def set_scene(self, scene_name, spawn_index, init=False):
        should_fade_out = not init and not self.scene.disable_fade_out
        if should_fade_out:
            self.fade_state["fading"] = True
            self.fade_state["frames"] = 0
            self.pending_soundtrack = self.scene.soundtrack

        if not init and self.scene.could_be_replayed:
            self.scene.background.reset()

        self.scene = next(s for s in self.scenes if s.name == scene_name)

        if not should_fade_out:
            self.sound_state["soundtrack"] = self.scene.soundtrack
        else:
            self.sound_state["soundtrack"] = None
            self.pending_soundtrack = self.scene.soundtrack

        if self.scene.is_level():
            self.character.set_position(*self.scene.get_spawn(spawn_index))
            self.character.push_move_request(vec2())
            self.character.set_velocity(vec2())
        elif self.scene.is_cinematic():
            self.cinematic_timer.start()

        if self.scene.default_show_menu:
            self.show_menu_after = {
                "active": True,
                "frames": 0,
                "duration": self.scene.show_menu_after,
            }

    def handle_auto_menu(self):
        if self.show_menu_after["active"] and not self.menu.show:
            if self.show_menu_after["frames"] < self.show_menu_after["duration"]:
                self.show_menu_after["frames"] += 1
            else:
                self.handle_toggle_menu()
                self.show_menu_after["active"] = False
                self.show_menu_after["frames"] = 0

    def push_pending_set_scene(self, data):
        self.pending_scene = data

    def push_feedback(self, feedback: Feedback):
        self.pending_feedback = feedback

    def handle_pending_scene(self):
        self.set_scene(self.pending_scene["scene_name"],
                       self.pending_scene.get("scene_spawn", 0))
        self.pending_scene = None

    def get_scene(self):
        return self.scene

    def get_halo_surf(self):
        character_center = self.character.get_center_position()
        cam_pos = self.render.camera.position

        if self.scene.is_level() and self.light_halo:
            character_center = self.character.get_center_position()
            cam_pos = self.render.camera.position
            return self.light_halo.get_surface(character_center - cam_pos)

        return None

    def handle_crossing_door(self, door):
        current_scene = self.scene
        door_destination = current_scene.get_door_destination(door)
        if door.complete_level:
            current_scene.complete()
        self.set_scene(*door_destination)

    def handle_death(self):
        self.character.reset()
        reload_scene = self.scene.name
        self.set_scene("cinematic_death", 0)
        self.scene.update_cinematic_destination(reload_scene, 0)

    def handle_cinematic_finished(self):
        self.set_scene(self.scene.cinematic_destination_scene,
                       self.scene.cinematic_destination_spawn)

    def clear_sfx_state(self):
        self.sound_state["bot_fx"] = None
        self.sound_state["feedback_fx"] = None

    def update_fade_state(self):
        duration = self.fade_state["duration"] * \
            self.main_loop_rate_controller.get_rate_reduction_factor()

        if self.fade_state["frames"] < duration:
            self.fade_state["frames"] += 1
        else:
            self.fade_state["fading"] = False
            self.fade_state["frames"] = 0
            if self.pending_soundtrack:
                self.sound_state["soundtrack"] = self.pending_soundtrack

    def update(self):
        if self.menu.show:
            self.update_menu_state()
            return
        elif self.fade_state["fading"]:
            self.update_fade_state()
            return

        scene = self.scene
        scene.update_background()

        self.events_handler.handle_events_queue(pygame.event.get())

        if scene.is_level():
            if self.main_loop_rate_controller.get_rate_reduction_factor() < self.apply_rate_reduction:
                self.apply_rate_reduction = self.main_loop_rate_controller.get_rate_reduction_factor()

            sprite_motor_scale = 1 / self.apply_rate_reduction
            collectibles = scene.get_visible_collectibles()
            life_bonuses = scene.get_life_bonuses()
            interactable_objects = self.get_scene_interactable_objects()
            bots = self.get_scene_bots()
            decor_sprites = scene.decor_sprites
            doors = scene.doors

            if (self.character.state["dead"]
                and self.character.animation.name == "dead"
                    and self.character.animation.finished):
                self.handle_death()
                return

            in_action_area: set = self.character.get_radial_raycasted_collidable_group(
                (*filter(lambda o: not o.disabled, interactable_objects),
                 *filter(lambda b: b.interactive and not b.disabled, bots)))

            first_maybe_interactable = next(iter(in_action_area), None)

            feedback = self.feedback_state["feedback"]

            if self.interactions_manager.dialog_box.open or (feedback and feedback.image):
                self.character.update_animation()

                for sprite in {*decor_sprites, *interactable_objects, *bots}:
                    sprite.update_animation()

                self.interactions_manager.update(first_maybe_interactable)

                if feedback and feedback.image:
                    self.update_feedback_state()

                return

            if self.pending_scene:
                self.handle_pending_scene()
                return

            if scene.auto_play:
                self.character.auto_play_sequence(scene.auto_play)
            else:
                self.character.clear_auto_play()
                self.character.push_move_request(self.arrows_input.state)

            self.character.apply_move_request(sprite_motor_scale)
            self.character.update_velocity_transfer_priority()
            self.character.apply_inertia()

            self.character.handle_collision_detection_with_group(scene.walls)
            self.character.handle_collision_detection_with_group(
                filter(lambda b: b.flying, bots),
                {
                    "response_mode": "none",
                    "use_collider": self.character.get_collider("head"),
                    "notify_collision_both": True
                })

            self.character.handle_collision_detection_with_group(
                filter(lambda b: not b.flying, bots), {
                    "notify_collision_both": True,
                })

            self.character.handle_collision_detection_with_group((*collectibles,
                                                                  *life_bonuses,
                                                                  *doors), {
                "response_mode": "none"
            })

            self.character.handle_collision_detection_with_group(
                interactable_objects)

            for bot in bots:
                bot.play_pattern()
                bot.apply_inertia()

                if bot.is_colliding_with(self.character):
                    self.sound_state["bot_fx"] = bot.collision_sfx

                bot.handle_character_maybe_collision(self.character)
                bot.apply_collisions()

                if bot is first_maybe_interactable:
                    bot.freeze()

                bot.apply_move_request(sprite_motor_scale)

                bot.update_position()
                bot.update_animation()
                bot.flush()

            for obj in {*decor_sprites, *interactable_objects}:
                obj.update_animation()

            for c in collectibles:
                if self.character.is_colliding_with(c):
                    self.push_feedback(c.feedback)
                    self.character.store_collectible(c)

            for bonus in life_bonuses:
                if self.character.is_colliding_with(bonus):
                    self.push_feedback(bonus.feedback)
                    self.character.use_life_bonus(bonus)

            for door in doors:
                if self.character.is_colliding_with(door):
                    self.handle_crossing_door(door)

            self.interactions_manager.update(
                next((o for o in in_action_area
                      if ((isinstance(o, Bot) and not o.use_action_strict_collider)
                          or self.character.is_colliding_with(o))
                      ), None))

            self.character.apply_collisions()
            self.character.handle_bot_collisions()
            self.character.fix_min_speed_threshold()

            self.character.update_position()
            self.character.update_animation()
            self.character.flush()

            self.update_feedback_state()

        elif scene.is_cinematic():
            if scene.cinematic_duration == 0:
                if scene.animation_is_finished():
                    self.handle_cinematic_finished()
            elif self.cinematic_timer.get_elapsed() >= scene.cinematic_duration:
                self.handle_cinematic_finished()

    def update_feedback_state(self):
        if self.pending_feedback and not self.interactions_manager.dialog_box.open:
            feedback = self.pending_feedback
            self.feedback_state["feedback"] = feedback
            self.sound_state["feedback_fx"] = self.resources_manager.get_sfx(
                feedback.sfx)
            self.feedback_state["frames"] = 0
            self.pending_feedback = None

        if self.feedback_state["feedback"]:
            duration = self.feedback_state["duration"] * \
                self.main_loop_rate_controller.get_rate_reduction_factor()
            self.feedback_state["frames"] += 1
            if self.feedback_state["frames"] >= duration:
                self.feedback_state["feedback"] = None

    def update_menu_state(self):
        if not self.menu.freeze:
            self.menu.get_events_handler().handle_events_queue(pygame.event.get())
        else:
            pygame.event.clear()

        if self.menu_notification_state["text"] and not self.menu_notification_state["keep_alive"]:
            self.menu_notification_state["frames"] += 1
            if self.menu_notification_state["frames"] >= self.menu_notification_state["duration"]:
                self.menu_notification_state["text"] = ""
                self.menu_notification_state["frames"] = 0

    def handle_menu_session(self):
        self.handle_pending_resources_directory_validation()
        self.handle_pending_resources_directory_notification()

    def play_sounds(self):
        self.sound_player.play()
        self.clear_sfx_state()

    def draw(self):
        render = self.render

        if self.menu.show:
            notification = self.menu_notification_state["text"]
            render.draw_menu(self.menu, notification)
            self.handle_menu_session()
        elif self.fade_state["fading"]:
            duration = self.fade_state["duration"] * \
                self.main_loop_rate_controller.get_rate_reduction_factor()
            render.draw_fade_out(duration - 5)
        else:
            scene = self.scene
            character = self.character
            inventory = character.inventory if scene.is_level() else None
            cta = self.interactions_manager.get_cta() if scene.is_level() else ""
            dialog = self.interactions_manager.get_dialog() if scene.is_level() else None
            feedback = self.feedback_state["feedback"] if scene.is_level(
            ) else None

            render.draw_game(self.get_sprites(),
                             scene.background,
                             self.get_halo_surf(),
                             character,
                             cta,
                             dialog,
                             inventory,
                             feedback)

            self.handle_auto_menu()

    def main_loop(self):
        while not self.quit:
            if self.main_loop_rate_controller.next_frame_ready():
                self.update()
                self.draw()
                self.play_sounds()
