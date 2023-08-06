from typing import Callable
import pygame
from fantomatic_engine.generic.events import EventListener


@EventListener.register
class SkipCinematicListener(EventListener):
    def __init__(self, callback: Callable):
        self.callback = callback

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key in {pygame.K_SPACE, pygame.K_RETURN}:
            self.callback()
