import pygame
import sys
from typing import Tuple, Callable


class EventsHandler:
    """
    Provides a set of methods to handle window events.
    """

    def __init__(self, listeners=dict()):
        """
        Listeners must implement the abstract EventListener class
        """
        self.listeners = listeners

    def handle_events_queue(self, events):
        """
        Parse the window event queue and call the appropriate event listeners
        """
        def handle(listener_key):
            for l in self.listeners.get(listener_key, ()):
                l.handle_event(e)

        for e in events:
            if e.type == pygame.QUIT:
                handle("quit")
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                handle("escape")
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                handle("keyboard")
            elif e.type in {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEMOTION,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEWHEEL}:
                handle("mouse")

    def update_listeners_for_key(self, key, listeners: Tuple[Callable]):
        self.listeners[key] = listeners
