import numpy as np
import pygame


class LightHalo:
    def __init__(self, state: dict, halo_resource):
        self.state = state
        self.shadow_alpha = 127
        self.halo_image = halo_resource.get_frame()
        self.halo_center_offset = np.array(self.halo_image.get_size()) / 2

    def get_surface(self, follow_position: np.array):
        halo_pos = follow_position - self.halo_center_offset
        halo_image = self.halo_image

        surf = pygame.Surface(
            self.state["get_render_size"](), pygame.SRCALPHA)

        surf.fill((0, 0, 0, self.shadow_alpha), None)
        surf.blit(halo_image,
                  halo_pos,
                  None,
                  pygame.BLEND_RGBA_SUB)

        return surf
