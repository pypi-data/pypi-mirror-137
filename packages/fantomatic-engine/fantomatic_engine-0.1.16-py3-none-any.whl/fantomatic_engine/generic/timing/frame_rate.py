from time import time


def get_time():
    """
    Returns current time in milliseconds.
    """
    return int(time() * 1000)


class FrameRateController:
    """
    Provides a set of methods to control the frame rate of a game loop.
    """

    def __init__(self, ideal_fps):
        self.tframe = get_time()
        self.ideal_fps = ideal_fps
        self.interval = 1000 / ideal_fps

    def next_frame_ready(self, use_fps=None) -> bool:
        """
        Returns true if interval is elapsed since last update
        """
        interval = 1000 / use_fps if use_fps else self.interval

        now = get_time()
        elpased = now - self.tframe
        ready = elpased >= interval
        if ready:
            self.tframe = now - (elpased % interval)
        return ready


class RateState:
    def __init__(self, rate):
        self.count_frames = 0
        self.time = get_time()
        self.max_recorded_delay = 0
        self.current_delay = 0
        self.ideal_rate = rate  # wanted rate in frames per seconds
        self.rate = rate  # The actual current rate
        self.rate_reduction_factor = 1

    def reset(self, use_new_rate):
        self.count_frames = 0
        self.max_recorded_delay = 0
        self.current_delay = 0
        self.rate = use_new_rate
        self.rate_reduction_factor = self.rate / self.ideal_rate

    def update(self):
        self.count_frames += 1
        now = get_time()
        a_second = 1000
        if now - self.time >= a_second:
            delay = self.rate - self.count_frames
            self.max_recorded_delay = max(self.max_recorded_delay, delay)
            self.current_delay = delay
            self.time = now
            self.count_frames = 0


class MainLoopFrameRateController(FrameRateController):
    def __init__(self, ideal_fps):
        super().__init__(ideal_fps)
        self.rate_state = RateState(ideal_fps)

    def update_ideal_fps(self):
        delay_tolerance = 5
        if self.rate_state.max_recorded_delay > delay_tolerance:
            new_rate = self.ideal_fps - self.rate_state.max_recorded_delay
            new_interval = 1000 / new_rate
            if new_interval > self.interval:
                self.interval = new_interval
                self.rate_state.reset(new_rate)

    def get_rate_reduction_factor(self):
        return self.rate_state.rate_reduction_factor

    def next_frame_ready(self, use_fps=None):
        ready = super().next_frame_ready(use_fps)
        if ready:
            self.rate_state.update()
            self.update_ideal_fps()
        return ready
