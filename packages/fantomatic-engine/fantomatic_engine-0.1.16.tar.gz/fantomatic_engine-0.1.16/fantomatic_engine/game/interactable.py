class Interactable:
    def __init__(self, data: dict):
        self.cta_message = data.get("cta_message", "")
        self.id = data.get("id", data["name"])
        self.interaction = data.get("interaction")
        self.type = data.get("type", "")
        self.spawn_if = data.get("spawn_if")
        self.interactive = not not self.interaction
        self.disabled = False

    def disable(self):
        self.disabled = True

    def should_spawn(self, character):
        if not self.spawn_if:
            return True
        elif self.spawn_if.get("character_has"):
            found = next((o for o in character.inventory if o.id ==
                          self.spawn_if["character_has"]), None)
            return not not found
        elif self.spawn_if.get("character_has_not"):
            found = next((o for o in character.inventory if o.id ==
                          self.spawn_if["character_has_not"]), None)
            return not found

        return True
