from typing import Optional
from .image import Animation


class DialogBox:
    def __init__(self):
        self.text = ""
        self.stream_state = 0
        self.open = False
        self.image: Optional[Animation] = None

    def show(self, data: dict):
        self.open = True
        self.text = data["text"]
        self.stream_state = 0
        self.image = data.get("image")

    def update_stream(self):
        if self.stream_state < len(self.text) - 1:
            self.stream_state += 1

    def stream_is_complete(self):
        return self.stream_state == len(self.text) - 1

    def get_text_stream(self):
        return self.text[:self.stream_state+1]

    def close(self):
        self.open = False
        self.text = ""
        self.image = None
