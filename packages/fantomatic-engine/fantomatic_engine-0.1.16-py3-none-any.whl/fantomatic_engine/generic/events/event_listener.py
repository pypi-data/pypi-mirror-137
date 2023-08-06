import abc


class EventListener(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event):
        pass
