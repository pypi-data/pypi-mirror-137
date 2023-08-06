from typing import Optional
from fantomatic_engine.generic.sound import Sound


class SoundPlayer:
    def __init__(self, shared_state):
        self.shared_state = shared_state
        sound_state = self.shared_state["get_sound_state"]()
        self.soundtrack: Optional[Sound] = sound_state["soundtrack"]
        self.bot_fx: Optional[Sound] = sound_state["bot_fx"]
        self.feedback_fx: Optional[Sound] = sound_state["feedback_fx"]

    def play(self):
        sound_state = self.shared_state["get_sound_state"]()
        snd_track = sound_state["soundtrack"]
        bot_fx = sound_state["bot_fx"]
        feedback_fx = sound_state["feedback_fx"]
        fadeout_values = {
            "soundtrack": 1000,
            "bot_fx": 500,
            "feedback_fx": 2000
        }

        for (snd, key) in zip((snd_track, bot_fx, feedback_fx),
                              ("soundtrack", "bot_fx", "feedback_fx")):
            current = getattr(self, key)
            if not (snd is current):
                if current and current.is_playing():
                    current.stop(fadeout_values[key])

                setattr(self, key, snd)

        for snd in (self.soundtrack, self.bot_fx, self.feedback_fx):
            if snd and not snd.is_playing():
                snd.play()
