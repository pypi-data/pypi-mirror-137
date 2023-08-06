from .feedback import Feedback
from ..resources_manager import ResourcesManager


class Feedbackable:
    def __init__(self, resource_manager: ResourcesManager, data: dict):
        self.feedback = Feedback(resource_manager, data)
