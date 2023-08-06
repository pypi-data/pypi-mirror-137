import pygame
from fantomatic_engine.generic.events import EventListener
import numpy as np
from fantomatic_engine.generic.vectors import vec2


@EventListener.register
class QuadridirectionalInput:
    def __init__(self):
        self.state = vec2(0, 0)
        keys = dict()
        keys[pygame.K_UP] = vec2(0, -1)
        keys[pygame.K_DOWN] = vec2(0, 1)
        keys[pygame.K_LEFT] = vec2(-1, 0)
        keys[pygame.K_RIGHT] = vec2(1, 0)
        self.keyBindingSubscription = keys

    def bindKeys(self, keyBindings):
        keys = dict()
        for kb in keyBindings:
            keys[kb] = keyBindings[kb]
        self.keyBindingSubscription = keys

    def handle_event(self, e):
        if not e.key in self.keyBindingSubscription:
            return

        reqvec = self.keyBindingSubscription.get(e.key)
        k_down = e.type == pygame.KEYDOWN
        self.state = self.state + reqvec if k_down else self.state - reqvec
