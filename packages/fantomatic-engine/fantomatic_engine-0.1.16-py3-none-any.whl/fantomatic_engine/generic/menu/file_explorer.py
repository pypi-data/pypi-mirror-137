import os
from pathlib import Path
from os.path import isdir
from os import listdir
from typing import List
from .menu_item import MenuItem
from ..events import AnyListener, EventsHandler
from .file_explorer_keys_listener import FileExplorerKeysListener


class FileExporer:
    def __init__(self, shared_state, options):
        self.dir_only = options.get("dir_only", False)
        self.shared_state = shared_state
        self.current_browse_path = Path.home()
        self.browse_empty = False
        self.items: List[MenuItem]
        self.update_items()

        self.selected_path = next(
            it for it in self.items if it.abs_path).abs_path

        self.browse_events_listener = FileExplorerKeysListener({
            "get_items": self.get_items,
            "update_selected_path": self.update_selected_path,
            "navigate": self.on_navigate
        })

        self.events_handler = EventsHandler(listeners={
            "keyboard": (
                self.browse_events_listener,
            ),
            "quit": (
                AnyListener(self.shared_state["on_quit"]),
            ),
            "escape": (
                AnyListener(self.shared_state["on_escape"]),
            ),
        })

    def update_browse_path(self, dir_path):
        self.current_browse_path = dir_path
        self.update_items()
        self.browse_events_listener.reset()
        self.update_selected_path()

    def update_selected_path(self):
        if not self.browse_empty:
            self.selected_path = self.items[self.browse_events_listener.selected_index].abs_path

    def dir_is_readable(self, path):
        return os.access(path, os.R_OK)

    def is_hidden_dir(self, path):
        return os.path.basename(path)[0] == "."

    def update_items(self):
        def full_path(p):
            return os.path.join(self.current_browse_path, p)

        self.items = [MenuItem(str(path),
                               self.on_select_current_path,
                               {"file_explorer_item": True,
                                "abs_path": os.path.join(self.current_browse_path, path),
                                }) for path in listdir(self.current_browse_path)
                      if (not self.is_hidden_dir(path)
                          and (not self.dir_only or (isdir(full_path(path))
                                                     and self.dir_is_readable(full_path(path)))))]

        self.items.sort(key=lambda it: it.text.lower())

        self.browse_empty = len(self.items) == 0

        if not self.browse_empty:
            self.items[0].selected = True
        else:
            self.items.insert(0,
                              MenuItem("          NO LOADABLE DATA",
                                       None,
                                       {"read_only": True,
                                        "file_explorer_item": True, }))

        self.items.insert(0,
                          MenuItem(os.path.basename(self.current_browse_path),
                                   None,
                                   {"read_only": True,
                                    "file_explorer_item": True,
                                    "dirname": True}))

        browse_root = os.path.realpath(os.path.join(
            self.current_browse_path, "..")) == str(self.current_browse_path)

        parent_name = os.path.basename(
            Path(self.current_browse_path).parent) or "ROOT"

        if not browse_root:
            self.items.insert(0,
                              MenuItem("← " + parent_name,
                                       None,
                                       {"read_only": True,
                                        "file_explorer_item": True,
                                        "small": True, }))

    def on_select_current_path(self):
        if not self.browse_empty:
            self.shared_state["on_select"](self.selected_path)

    def on_navigate(self, direction):
        to_parent = direction == -1
        if to_parent:
            parent_path = (Path(self.selected_path).parent
                           if self.browse_empty
                           else Path(self.selected_path).parent.parent)
            self.update_browse_path(parent_path)
        else:
            self.update_browse_path(self.selected_path)

    def get_items(self):
        return self.items
