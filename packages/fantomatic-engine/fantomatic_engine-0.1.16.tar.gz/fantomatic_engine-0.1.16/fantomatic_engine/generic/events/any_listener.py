from fantomatic_engine.generic.events import EventListener
import pygame
from typing import Callable


@ EventListener.register
class AnyListener(EventListener):
    def __init__(self, callback: Callable):
        self.callback = callback

    def handle_event(self, _e):
        self.callback()
