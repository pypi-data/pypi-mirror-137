import pygame


class Sound:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.audio: pygame.mixer.Sound = data["audio"]
        self.loops = 0 if data.get("once") else -1
        self.channel = None

    def play(self):
        self.channel = self.audio.play(loops=self.loops)

    def pause(self):
        self.channel.pause()
        # self.audio.pause()

    def unpause(self):
        self.channel.unpause()

    def stop(self, fadeout=0):
        self.audio.fadeout(fadeout)

    def is_playing(self):
        return self.audio.get_num_channels() > 0
