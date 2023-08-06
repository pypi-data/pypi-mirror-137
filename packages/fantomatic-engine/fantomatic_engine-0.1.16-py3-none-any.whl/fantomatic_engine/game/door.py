from fantomatic_engine.generic.shapes import Segment


class Door(Segment):
    def __init__(self, data: dict):
        super().__init__(*data["segment_points"])
        self.destination_scene: str = data["destination_scene"]
        self.destination_spawn: int = data["destination_spawn"]
        self.complete_level = data.get("complete_level", False)
