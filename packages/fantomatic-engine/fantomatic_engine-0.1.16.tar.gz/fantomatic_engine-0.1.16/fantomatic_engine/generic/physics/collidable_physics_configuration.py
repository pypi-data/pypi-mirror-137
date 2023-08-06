class CollidablePhysicsConfiguration:
    def __init__(self, data):
        self.min_speed = data.get("min_speed", .3)
        self.motor_power = data.get("motor_power", 1)
        self.movable = int(data.get("movable", True))
        self.solid = data.get("solid", True)
        self.mass: float = 1 + data.get("mass", 10) / 10

        assert self.mass > 0, "Mass must be >= 0"

        self.velocity_transfer_priority: int = data.get(
            "velocity_transfer_priority", 0) if self.movable else -1

    def update_velocity_transfer_priority(self, value):
        self.velocity_transfer_priority = value
