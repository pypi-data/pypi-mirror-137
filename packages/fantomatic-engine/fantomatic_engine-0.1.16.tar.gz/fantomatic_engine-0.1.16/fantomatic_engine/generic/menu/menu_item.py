from typing import Callable


class MenuItem:
    def __init__(self, text, callback: Callable, options=dict()):
        self.text = text
        self.callback = callback
        self.selected = False
        self.secondary = options.get("secondary", False)
        self.read_only = options.get("read_only", False)
        self.small = options.get("small", False)

        # File explorer type attributes
        self.file_explorer_item = options.get("file_explorer_item", False)
        self.abs_path = options.get("abs_path")
        self.dirname = options.get("dirname", False)
