import pygame
from fantomatic_engine.generic.events import EventListener
from typing import Optional, Union
from .sprites.interactable_object import InteractableObject
from .sprites.bot import Bot
from .sprites.character import Character
from .action_keys_listener import ActionKeysListener
from fantomatic_engine.generic import ResourcesManager, DialogBox
from fantomatic_engine.generic.feedback import Feedback


class InteractionsManager:
    def __init__(self, shared_state: dict):
        self.action_events_listener = ActionKeysListener(
            self.handle_action_key_event)

        self.shared_state = shared_state
        self.interactable: Optional[Union[InteractableObject, Bot]] = None
        self.interaction_types = {
            "message": self.handle_display_message,
            "give_collectible": self.handle_give_collectible,
            "require_collectible": self.handle_require_collectible,
            "require_collectibles": self.handle_require_collectibles,
            "modify": self.handle_modifications,
            "set_scene": self.handle_set_scene
        }

        self.modification_types = {
            "animation": self.handle_modify_animation,
            "pattern": self.handle_modify_pattern
        }

        self.dialog_box = DialogBox()
        self.prompt_dialog_close = False

    def clear(self):
        self.interactable = None
        self.dialog_box.close()

    def update(self, maybe_interactable: Optional[Union[InteractableObject, Bot]]):
        self.interactable = maybe_interactable
        if self.dialog_box.open:
            self.dialog_box.update_stream()
            if self.dialog_box.stream_is_complete():
                self.prompt_dialog_close = True

    def handle_action_key_event(self, event):
        if self.dialog_box.open and not self.dialog_box.stream_is_complete():
            return
        if self.prompt_dialog_close:
            self.close_dialog()
            self.prompt_dialog_close = False
        elif self.interactable:
            interaction = self.interactable.interaction
            self.handle_feedback(interaction)

            for key in filter(lambda k: k != "feedback", interaction):
                handle = self.interaction_types.get(key,
                                                    self.unsupported_interaction)
                handle(interaction[key])

    def handle_feedback(self, data_object: dict):
        if data_object.get("feedback"):
            r_m = self.shared_state["resources_manager"]
            self.shared_state["push_feedback"](
                Feedback(r_m, data_object["feedback"]))

    def unsupported_interaction(self, data, _interactable=None):
        print("WARNING UNSUPPORTED INTERACTION TYPE",
              data["modification_type"])

    def handle_modifications(self, modifs):
        scene = self.shared_state["get_scene"]()
        for modif_data in modifs:
            object_to_modify = next(o for o in scene.get_interactables(
            ) if o.id == modif_data["interactable_id"])

            handle = self.modification_types.get(modif_data["modification_type"],
                                                 self.unsupported_interaction)

            handle(modif_data, object_to_modify)

            self.handle_feedback(modif_data)

    def handle_set_scene(self, data):
        self.shared_state["push_pending_set_scene"](data)
        self.handle_interaction_completion(data)

    def handle_modify_animation(self, data: dict, to_modify: Union[InteractableObject, Bot]):
        to_modify.set_animation(data["to"])
        self.handle_interaction_completion(data)

    def handle_modify_pattern(self, data: dict, to_modify: Bot):
        to_modify.set_pattern(data["to"])
        self.handle_interaction_completion(data)

    def handle_give_collectible(self, data):
        scene = self.shared_state["get_scene"]()
        scene_collectibles = scene.get_collectibles()

        found_object = next(
            o for o in scene_collectibles if o.id == data["collectible_id"])

        character: Character = self.shared_state["character"]
        character.store_collectible(found_object)
        self.shared_state["push_feedback"](found_object.feedback)
        self.handle_interaction_completion(data)

    def handle_require_collectible(self, data):
        character: Character = self.shared_state["character"]
        character_has_required = character.has_collectible(
            data["collectible_id"])

        next_step_data = (data.get("if_object", dict())
                          if character_has_required
                          else data.get("if_not_object", dict()))

        for key in next_step_data:
            handle = self.interaction_types.get(key,
                                                self.unsupported_interaction)
            handle(next_step_data[key])

        if character_has_required and data.get("consume_collectible"):
            character.consume_collectible(data["collectible_id"])

    def handle_require_collectibles(self, data):
        character: Character = self.shared_state["character"]
        character_has_required = all(
            it in [o.id for o in character.inventory] for it in data["collectibles_id"])

        next_step_data = (data.get("if_all_objects", dict())
                          if character_has_required
                          else data.get("if_not_all_objects", dict()))

        for key in next_step_data:
            handle = self.interaction_types.get(key,
                                                self.unsupported_interaction)
            handle(next_step_data[key])

        if character_has_required and data.get("consume_collectibles"):
            for oid in data["collectibles_id"]:
                character.consume_collectible(oid)

    def handle_display_message(self, data):
        dial_data = {"text": data["text"]}

        if data.get("image"):
            r_m: ResourcesManager = self.shared_state["resources_manager"]
            anim_set = r_m.get_animation_set(data["image"])

            dial_image = next(
                (a for a in anim_set if a.name == "dialog"), None)

            assert dial_image, "Dialog image missing for set " + data["image"]

            dial_data["image"] = dial_image

        self.dialog_box.show(dial_data)
        self.handle_interaction_completion(data)

    def handle_interaction_completion(self, data: dict):
        if data.get("complete"):
            self.interactable.disable()

    def get_cta(self) -> str:
        if self.prompt_dialog_close:
            return "Fermer le dialogue"
        elif (self.interactable and self.interactable.interactive
                and not (self.dialog_box.open
                         and not self.dialog_box.stream_is_complete())):
            return self.interactable.cta_message
        return ""

    def get_dialog(self) -> Optional[DialogBox]:
        return self.dialog_box if self.dialog_box.open else None

    def close_dialog(self):
        self.dialog_box.close()
