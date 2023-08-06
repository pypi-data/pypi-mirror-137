import pygame
from typing import List
from ..events import EventListener
from .menu_item import MenuItem


@EventListener.register
class MenuNavigationKeysListener(EventListener):
    def __init__(self, shared_state):
        self.shared_state = shared_state
        self.selected_index: int
        self.reset()

    def reset(self):
        items = self.__get_items()
        self.selected_index = items.index(
            next(it for it in items if it.selected))

    def update_menu_item_selected(self):
        items = self.__get_items()
        for (i, item) in enumerate(items):
            item.selected = i == self.selected_index

    def on_key_up(self):
        items = self.__get_items()

        def select_index():
            self.selected_index = (self.selected_index - 1
                                   if self.selected_index > 0 and not items[self.selected_index - 1].read_only
                                   else len(items) - 1)
            if items[self.selected_index].read_only:
                select_index()
        select_index()

        self.update_menu_item_selected()

    def on_key_down(self):
        items = self.__get_items()

        def select_index():
            self.selected_index = (self.selected_index + 1
                                   if self.selected_index + 1 <= len(items) - 1
                                   else 0)

            if items[self.selected_index].read_only:
                select_index()

        select_index()

        self.update_menu_item_selected()

    def __get_items(self) -> List[MenuItem]:
        return self.shared_state["get_items"]()

    def on_key_enter(self):
        items = self.__get_items()
        item_selected = next((it for it in items if it.selected), None)
        if item_selected:
            item_selected.callback()

    def handle_event(self, event):
        k_names = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "enter": pygame.K_RETURN,
        }

        handlers = {
            "up": self.on_key_up,
            "down": self.on_key_down,
            "enter": self.on_key_enter,
        }

        if event.type == pygame.KEYDOWN and event.key in k_names.values():
            key = next(k for (k, val) in k_names.items() if val == event.key)

            handle = next(handler for (k, handler)
                          in handlers.items() if k == key)

            handle()
