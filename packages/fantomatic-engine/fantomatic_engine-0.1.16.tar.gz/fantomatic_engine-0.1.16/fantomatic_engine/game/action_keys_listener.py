from fantomatic_engine.generic.events import EventListener
import pygame
from typing import Callable


@EventListener.register
class ActionKeysListener(EventListener):
    def __init__(self, on_action_callback: Callable):
        self.on_action_callback = on_action_callback

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.on_action_callback(event)
