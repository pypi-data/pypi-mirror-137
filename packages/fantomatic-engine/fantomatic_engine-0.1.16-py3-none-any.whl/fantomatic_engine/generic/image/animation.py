import pygame
from os import listdir, path
import numpy as np
from ..shapes import Rectangle
from ..timing import FrameRateController
from ..vectors import vec2
from typing import Optional, Tuple


class Animation:
    """
    Provides an abstraction of an animation. Holds convenient animation data like frame_count, size, name, collider, etc.
    """

    def __init__(self, data: dict):
        self.name = data["name"]
        self.is_none = self.name == "none"
        self.fps = data.get("fps", 0)
        self.use_fps = self.fps
        self.frames = self.build_frames(data)
        self.frame_count = len(self.frames)
        self.dimensions = self.get_image_dimensions()
        self.current_frame = 0
        self.alpha = 255

        collider_data = data.get("collider", [
            [0, 0],
            [self.dimensions[0], 0],
            [self.dimensions[0], self.dimensions[1]],
            [0, self.dimensions[1]]
        ])

        # needs to be float type because may be scaled to a non int
        self.collider = np.array(collider_data, dtype=float)

        scale = data.get("scale", 1)
        if scale != 1:
            self.scale(scale)

        self.fps_controller = FrameRateController(self.fps or 50)
        self.play_once = data.get("play_once", False)
        self.rendering_options: Optional[dict] = data.get("rendering_options")
        self.finished = False

    def build_frames(self, data):
        frames = list()

        if data.get("anim_file"):
            resource = pygame.image.load(data["anim_file"])
            frame_count = data.get("frame_count", 1)
            if frame_count == 1:
                frames = [resource]
            else:
                resource_rect = resource.get_rect()
                fr_size = (resource_rect.width / frame_count,
                           resource_rect.height)
                for i in range(frame_count):
                    fr_surf = pygame.Surface(fr_size, pygame.SRCALPHA)
                    fr_surf.blit(resource, (0, 0),
                                 (i * fr_size[0], 0, fr_size[0], fr_size[1]))
                    frames.append(fr_surf)

        elif data.get("anim_folder"):
            fr_dir = data["anim_folder"]
            files = listdir(fr_dir)
            files.sort()

            for f in files:
                fr_surf = pygame.image.load(path.join(fr_dir, f))
                frames.append(fr_surf)
        else:
            # create a none animation
            frames = [pygame.Surface((1, 1))]

        flip: Optional[Tuple[bool]] = data.get("flip")  # (flip_x, flip_y)

        if flip:
            frames = [pygame.transform.flip(fr, *flip) for fr in frames]

        return np.array(frames, dtype=pygame.Surface)

    def get_image_dimensions(self):
        return vec2(*self.frames[0].get_size())

    def update_frame(self):
        """
        Update the current frame index to use.
        """
        if (self.fps_controller.next_frame_ready(self.use_fps)
                and self.frame_count > 1 and self.fps > 0 and not self.finished):
            if self.current_frame + 1 >= self.frame_count:
                if self.play_once:
                    self.finished = True
                else:
                    self.current_frame = 0
            else:
                self.current_frame += 1

    def get_frame(self):
        fr = self.frames[self.current_frame]
        if fr.get_alpha() != self.alpha:
            fr.set_alpha(self.alpha)
        return fr

    def scale(self, factor):
        current_size = vec2(*self.get_frame().get_size())
        self.frames = np.array([pygame.transform.scale(fr,
                                                       current_size * factor)
                                for fr in self.frames])
        self.collider = self.collider * factor
        self.dimensions = self.get_image_dimensions()

    def reset(self):
        self.current_frame = 0
        self.finished = False

    def set_alpha(self, value):
        self.alpha = value

    def skip(self):
        if self.play_once:
            self.current_frame = self.frame_count - 1
            self.finished = True
