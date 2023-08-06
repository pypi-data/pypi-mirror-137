import pygame
from ..events import AnyListener, EventsHandler
from .menu_item import MenuItem
from .menu_navigation_keys_listener import MenuNavigationKeysListener
from .file_explorer import FileExporer


class Menu:
    def __init__(self, shared_state):
        assert (shared_state.get("get_items")
                and all(isinstance(mit,
                                   MenuItem)
                        for mit in shared_state["get_items"]())), "Error, Menu instance requires a get_items parameter function returning a collection of MenuItem instances"

        self.show = False
        self.shared_state = shared_state
        self.browse_files = False

        f_exp_state = shared_state.copy()
        f_exp_state.update({
            "on_escape": self.on_escape_file_explorer,
            "on_select": self.on_select_resources_directory
        })
        self.file_explorer = FileExporer(f_exp_state, {"dir_only": True})

        self.items = self.shared_state["get_items"]()
        self.auto_select_first_item()

        self.nav_events_listener = MenuNavigationKeysListener(
            {"get_items": lambda: self.items})

        self.events_handler = EventsHandler(listeners={
            "keyboard": (
                self.nav_events_listener,
            ),
            "quit": (
                AnyListener(self.shared_state["on_quit"]),
            ),
            "escape": (
                AnyListener(self.shared_state["on_escape"]),
            ),
        })

        self.freeze = False

    def set_freeze(self, value):
        self.freeze = value

    def set_browse_files(self, val):
        self.browse_files = val
        self.refresh_items()

    def on_escape_file_explorer(self):
        self.set_browse_files(False)

    def on_select_resources_directory(self, path):
        self.shared_state["select_resources_directory"](path)

    def get_events_handler(self):
        return (self.file_explorer.events_handler
                if self.browse_files
                else self.events_handler)

    def get_events_listener(self):
        return (self.file_explorer.browse_events_listener
                if self.browse_files
                else self.nav_events_listener)

    def auto_select_first_item(self):
        found_first_selectable = False
        for it in self.items:
            it.selected = not it.read_only and not found_first_selectable
            if it.selected:
                found_first_selectable = True

    def toggle(self):
        self.show = not self.show
        if self.show:
            self.refresh_items()
            self.auto_select_first_item()
        else:
            self.nav_events_listener.reset()

    def close(self):
        self.show = False
        self.nav_events_listener.reset()

    def refresh_items(self):
        self.shared_state["before_refresh_items"]()
        self.items = self.shared_state["get_items"]()
        self.auto_select_first_item()
        self.get_events_listener().reset()
