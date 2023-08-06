from typing import Optional


class ResourcesDirectorySettings:
    def __init__(self):
        self.pending_validation: Optional[str] = None
        self.pending_success = False
        self.pending_error: Optional[str] = None

    def reset(self):
        self.pending_validation = None
        self.pending_success = False
        self.pending_error = None


class MenuSession:
    def __init__(self, items):
        self.items = items
        self.resources_directory_settings = ResourcesDirectorySettings()

    def clear_resources_dir_pending_validation(self):
        self.resources_directory_settings.pending_validation = None

    def set_items(self, items):
        self.items = items

    def set_resources_directory_pending_notification(self, mode: str, err_msg: str):
        if mode == "error":
            self.resources_directory_settings.pending_error = err_msg
        else:
            self.resources_directory_settings.pending_success = True

    def reset_resources_dir_settings(self):
        self.resources_directory_settings.reset()
