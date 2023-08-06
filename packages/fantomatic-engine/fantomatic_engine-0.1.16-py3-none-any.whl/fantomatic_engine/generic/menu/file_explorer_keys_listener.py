import pygame
from typing import List
from ..events import EventListener
from .menu_item import MenuItem


@EventListener.register
class FileExplorerKeysListener(EventListener):
    def __init__(self, shared_state):
        self.shared_state = shared_state
        self.selected_index: int
        self.reset()

    def reset(self):
        items = self.__get_items()
        selected_item = next((it for it in items if it.selected), None)
        self.selected_index = items.index(
            selected_item) if selected_item else 0

    def update_menu_item_selected(self):
        for (i, item) in enumerate(self.__get_items()):
            item.selected = i == self.selected_index

        self.shared_state["update_selected_path"]()

    def on_key_up(self):
        items = self.__get_items()
        if not next((it for it in items if not it.read_only), None):
            return

        def select_available():
            self.selected_index = (self.selected_index - 1
                                   if self.selected_index > 0
                                   else len(items) - 1)
            if items[self.selected_index].read_only:
                select_available()
        select_available()

        self.update_menu_item_selected()

    def on_key_down(self):
        items = self.__get_items()
        if not next((it for it in items if not it.read_only), None):
            return

        def select_available():
            self.selected_index = (self.selected_index + 1
                                   if self.selected_index + 1 <= len(items) - 1
                                   else 0)

            if items[self.selected_index].read_only:
                select_available()

        select_available()

        self.update_menu_item_selected()

    def __get_items(self) -> List[MenuItem]:
        return self.shared_state["get_items"]()

    def on_key_enter(self):
        item_selected = next(
            (it for it in self.__get_items() if it.selected), None)
        if item_selected:
            item_selected.callback()

    def on_key_right(self):
        self.shared_state["navigate"](1)

    def on_key_left(self):
        self.shared_state["navigate"](-1)

    def handle_event(self, event):
        k_names = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "right": pygame.K_RIGHT,
            "left": pygame.K_LEFT,
            "enter": pygame.K_RETURN,
        }

        handlers = {
            "up": self.on_key_up,
            "down": self.on_key_down,
            "enter": self.on_key_enter,
            "right": self.on_key_right,
            "left": self.on_key_left,
        }

        if event.type == pygame.KEYDOWN and event.key in k_names.values():
            key = next(k for (k, val) in k_names.items() if val == event.key)

            handle = next(handler for (k, handler)
                          in handlers.items() if k == key)

            handle()
