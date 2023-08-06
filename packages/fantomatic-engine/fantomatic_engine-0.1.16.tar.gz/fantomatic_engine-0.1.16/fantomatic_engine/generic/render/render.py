import pygame
import os
from functools import reduce
from typing import Optional, List, Set, Tuple
from .. import Sprite
from ..image import Animation
from ..vectors import vec2, vec_is_nul
from ..shapes import Rectangle
from ..dialog_box import DialogBox
from .camera import Camera
from ..menu import Menu
from ..menu.menu_item import MenuItem
from ..feedback import Feedback


class Render:
    def __init__(self, rendering_surface: pygame.Surface):
        # default, will be function of background image
        self.drawing_surface = pygame.Surface((800, 800))

        self.rendering_surface = rendering_surface

        self.scale_factor = rendering_surface.get_size(
        )[0] / self.drawing_surface.get_size()[0]

        self.drawing_size = vec2(*self.drawing_surface.get_size())

        self.render_size = vec2(
            *self.drawing_surface.get_size()) * self.scale_factor

        self.screen_size = vec2(*self.rendering_surface.get_size())

        self.menu_drawing_surface = pygame.Surface(self.screen_size,
                                                   pygame.SRCALPHA)
        self.menu_shadow_surf = pygame.Surface(self.screen_size,
                                               pygame.SRCALPHA)
        self.menu_shadow_surf.fill((0, 0, 0, 180))
        self.menu_wallpaper: Optional[pygame.Surface] = None

        camera_unscaled_focus_rect = Rectangle(
            self.rendering_surface.get_rect())

        camera_unscaled_focus_rect.scale(1 / self.scale_factor)

        self.camera = Camera({
            "get_focus": lambda: self.screen_size / self.scale_factor,
            "get_bounds": lambda: self.drawing_surface.get_rect()
        })

        self.fonts = {
            "regular": {
                "cta": pygame.font.SysFont("mono", 30, True),
                "dialog": pygame.font.SysFont("mono", 20),
                "small": pygame.font.SysFont("mono", 16),
                "menu": pygame.font.SysFont("mono", 40, True),
                "menu_secondary": pygame.font.SysFont("mono", 30),
                "menu_read_only": pygame.font.SysFont("mono", 25),
                "menu_small": pygame.font.SysFont("mono", 20),
                "menu_file_explorer_dirname": pygame.font.SysFont("mono", 20),
                "menu_notification": pygame.font.SysFont("mono", 25)
            },
            "larger": {
                "cta": pygame.font.SysFont("sans", 45, True),
                "dialog": pygame.font.SysFont("sans", 25),
                "small": pygame.font.SysFont("sans", 24),
            },
        }

        self.prev_left = 0

        self.drawing_pos_offset = vec2()
        self.x_rendering_offset = 0
        self.last_drawn_background = None

    def __clear(self):
        self.rendering_surface.fill((0, 0, 0, 255))
        if self.menu_wallpaper:
            self.menu_wallpaper = None

    def draw_game(self,
                  sprites: List[Sprite],
                  scene_background: Animation,
                  light_surface: Optional[pygame.Surface],
                  camera_follow_sprite: Sprite,
                  cta: str,
                  dialog_box: Optional[DialogBox],
                  inventory: Optional[Set[Sprite]],
                  feedback: Optional[Feedback]):

        rendering_opts = scene_background.rendering_options or dict()

        if self.last_drawn_background != scene_background:
            self.last_drawn_background = scene_background
            use_max_height = rendering_opts.get("use_max_height", False)
            scale_axis = 1 if use_max_height else 0

            self.drawing_surface = pygame.Surface(scene_background.dimensions)

            self.scale_factor = (self.rendering_surface.get_size()[scale_axis]
                                 / self.drawing_surface.get_size()[scale_axis])

            self.drawing_size = vec2(*self.drawing_surface.get_size())

            self.render_size = vec2(
                *self.drawing_surface.get_size()) * self.scale_factor

        if not rendering_opts.get("ignore_camera"):
            self.camera.follow(camera_follow_sprite.get_center_position())
            if rendering_opts.get("ignore_camera_y"):
                self.camera.position[1] = 0
        else:
            self.camera.position = vec2()

        self.__clear()

        self.drawing_pos_offset = -self.camera.position

        self.__draw_background(scene_background)
        self.__draw_sprites(sprites)

        if light_surface:
            self.__draw_light(light_surface)

        if dialog_box:
            self.__draw_dialog(dialog_box, rendering_opts)

        if cta and not (dialog_box
                        and dialog_box.open
                        and not dialog_box.stream_is_complete()):
            self.__draw_cta(cta, rendering_opts)

        if inventory and len(inventory) > 0:
            self.__draw_inventory(inventory)

        if feedback and feedback.image:
            self.__draw_feedback(feedback)

        self.__render()

    def draw_fade_out(self, duration):
        alpha = int(255 / max(1, duration))
        size = self.drawing_surface.get_size()
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0, 0, 0, alpha))
        self.drawing_surface.blit(surf, (0, 0))
        self.__render()

    def __draw_background(self, anim):
        rendering_opts = anim.rendering_options or dict()
        self.x_rendering_offset = (self.rendering_surface.get_size()
                                   [0] - self.render_size[0]) / 2 if rendering_opts.get("center_x") else 0

        self.drawing_surface.blit(anim.get_frame(), self.drawing_pos_offset)

    def __draw_sprites(self,  sprites):
        sprites.sort(key=lambda s: s.z_index)

        self.drawing_surface.blits([(
            sprite.animation.get_frame(),
            sprite.position + self.drawing_pos_offset
        ) for sprite in sprites])

    def __draw_light(self, light_surface):
        self.drawing_surface.blit(light_surface,
                                  (0, 0),
                                  (0, 0, self.drawing_size[0], self.drawing_size[1]))

    def __draw_cta(self, cta: str, background_rendering_options):
        font_key = ("regular"
                    if not background_rendering_options.get("use_max_height")
                    else "larger")

        font_cta = self.fonts[font_key]["cta"]
        font_small = self.fonts[font_key]["small"]

        line_height = font_cta.get_height()
        hint = "[ touche espace ]"

        cta_text_size = font_cta.size(cta)
        hint_text_size = font_small.size(hint)

        cta_size = vec2(max(cta_text_size[0], hint_text_size[0]) +
                        40, cta_text_size[1] + hint_text_size[1] + 30)

        x_pos_cta = (cta_size[0] - cta_text_size[0]) / 2
        y_pos_cta = (cta_size[1] - (hint_text_size[1] + cta_text_size[1])) / 2
        x_pos_hint = (cta_size[0] - hint_text_size[0]) / 2

        cta_surf = pygame.Surface(cta_size, pygame.SRCALPHA)
        cta_surf.fill((0, 0, 0, 127))

        cta_surf.blit(font_cta.render(
            cta, False, (255, 255, 255)), (x_pos_cta, y_pos_cta))

        cta_surf.blit(font_small.render(
            hint, False, (255, 255, 255)), (x_pos_hint, y_pos_cta + line_height))

        unscaled_screen_size = self.screen_size / self.scale_factor

        if not vec_is_nul(self.drawing_pos_offset):
            base_cta_pos = unscaled_screen_size / 2
        else:
            base_cta_pos = vec2(
                self.drawing_size[0], unscaled_screen_size[1]) / 2

        cta_pos = base_cta_pos - (cta_size / 2)

        self.drawing_surface.blit(cta_surf, cta_pos)

    def __draw_dialog(self, dialog: DialogBox, background_rendering_options):
        font_key = ("regular"
                    if not background_rendering_options.get("use_max_height")
                    else "larger")

        font_dialog = self.fonts[font_key]["dialog"]

        stream = dialog.get_text_stream()
        line_height = font_dialog.get_height()

        unscaled_render_size = self.render_size / self.scale_factor
        unscaled_screen_size = self.screen_size / self.scale_factor

        total_text_height = len(dialog.text.split("\n")) * line_height

        margin = 50
        padding_x = 40
        padding_y = 20

        image_size = (100, 100) if dialog.image else (0, 0)

        dialog_box_height = (max(image_size[1], total_text_height)
                             + (2*padding_y if dialog.image
                                else total_text_height + 2*padding_y))

        dialog_box_size = (unscaled_render_size[0] - margin * 2,
                           dialog_box_height)

        dialog_box_pos = (margin,
                          unscaled_screen_size[1] - margin - dialog_box_size[1])

        text_pos_x = (padding_x +
                      ((image_size[0] + 20) if dialog.image else 0))

        text_pos_y = (dialog_box_size[1] - total_text_height) / 2

        dialog_surf = pygame.Surface(dialog_box_size, pygame.SRCALPHA)

        dialog_surf.fill((200, 200, 200, 150))

        for (i, line) in enumerate(stream.split("\n")):
            text_surf = font_dialog.render(line, False, (20, 20, 20))
            dialog_surf.blit(text_surf, (text_pos_x,
                                         text_pos_y + i * line_height))

        if dialog.image:
            image_surf = pygame.transform.scale(
                dialog.image.get_frame(),
                image_size)

            dialog_surf.blit(
                dialog.image.get_frame(),
                (padding_x, padding_y, *image_size))

        self.drawing_surface.blit(dialog_surf, dialog_box_pos)

    def __draw_inventory(self, inventory: Set[Sprite]):
        icon_size = vec2(50, 50) / self.scale_factor
        margin = 10
        panel_width = len(inventory) * (icon_size[0] + margin)
        panel_height = icon_size[1]
        surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        x = 0

        items = sorted(inventory, key=lambda i: i.inventory_position)

        for (i, item) in enumerate(items):
            image = item.animation.get_frame()
            im_size = vec2(*image.get_size())
            icon = pygame.transform.scale(image,
                                          im_size * (icon_size[0] / im_size[0]))
            surf.blit(icon,
                      (x + i*(icon_size[0] + margin),
                       (panel_height - icon.get_size()[1]) / 2))

        self.drawing_surface.blit(surf, (5, 5))

    def __draw_feedback(self, feedback: dict):
        unscaled_screen_size = self.screen_size / self.scale_factor
        surf = pygame.Surface(unscaled_screen_size, pygame.SRCALPHA)
        surf.fill((0, 0, 0, 127))
        img = feedback.image.get_frame()
        base_size = vec2(*img.get_size())
        render_height = unscaled_screen_size[1] / 2
        render_img = pygame.transform.scale(img,
                                            base_size * (render_height / base_size[1]))

        render_size = render_img.get_size()

        img_pos = ((unscaled_screen_size[0] - render_size[0]) / 2,
                   (unscaled_screen_size[1] - render_size[1]) / 2)

        surf.blit(render_img, img_pos)
        font_cta = self.fonts["regular"]["cta"]

        text_surf = font_cta.render(
            feedback.message, False, (200, 200, 200))

        surf.blit(text_surf, ((unscaled_screen_size[0] - text_surf.get_size()[0]) / 2,
                              img_pos[1] + render_size[1] + 20))

        self.drawing_surface.blit(surf, (0, 0))

    def draw_menu(self, menu: Menu, notification: str):
        # Menu is drawn directly at screen size in order to prevent the font from being pixelated
        self.menu_drawing_surface.fill((0, 0, 0, 255))

        if not self.menu_wallpaper:
            self.menu_wallpaper = pygame.transform.scale(self.drawing_surface,
                                                         self.render_size)
        wallpaper = self.menu_wallpaper

        self.menu_drawing_surface.blit(wallpaper,
                                       (self.x_rendering_offset, 0),
                                       (0, 0, self.render_size[0], self.render_size[1]))

        self.menu_drawing_surface.blit(self.menu_shadow_surf, (0, 0))

        menu_screen_margin = self.screen_size / 5
        file_explorer_margin = vec2(0, 25)

        font_menu = self.fonts["regular"]["menu"]
        font_menu_secondary = self.fonts["regular"]["menu_secondary"]
        font_menu_small = self.fonts["regular"]["menu_small"]
        font_menu_read_only = self.fonts["regular"]["menu_read_only"]
        font_menu_notification = self.fonts["regular"]["menu_notification"]

        line_h = font_menu.get_linesize() + 10
        line_h_secondary = font_menu_secondary.get_linesize() + 5
        line_h_small = font_menu_small.get_linesize() + 1
        # ready only lines will have a gap under them
        line_h_read_only = font_menu_read_only.get_linesize() + 10

        white, grey, grey2, yellow = ((255, 255, 255),
                                      (180, 180, 180),
                                      (120, 120, 120),
                                      (255, 220, 30))

        def get_item_h(it):
            return (line_h_secondary if it.secondary
                    else line_h_read_only if it.read_only and not it.small
                    else line_h_small if it.small
                    else line_h)

        total_block_height = reduce(lambda a, b: a + get_item_h(b),
                                    menu.items,
                                    0)

        file_explorer_max_lines = ((self.screen_size
                                    - (menu_screen_margin * 2)
                                    - file_explorer_margin)[1] - total_block_height) / line_h_small

        if menu.browse_files:
            total_block_height += line_h_small * file_explorer_max_lines

        menu_items_block_pos = vec2(
            menu_screen_margin[0],
            (self.screen_size[1] - total_block_height) / 2
        )

        item_pos = menu_items_block_pos

        for (i, item) in enumerate(menu.items):
            font = (font_menu_secondary if item.secondary
                    else font_menu_read_only if item.read_only and not item.small
                    else font_menu_small if item.small
                    else font_menu)

            h = get_item_h(item)

            item_color = white if item.selected else grey
            item_surf = font.render(item.text, False, item_color)

            self.menu_drawing_surface.blit(item_surf, item_pos)

            if item.selected:
                bullet_radius = 8
                bullet_margin = 20
                bullet_pos = (
                    item_pos[0] - bullet_margin - bullet_radius / 2,
                    item_pos[1] + (h / 2) - (bullet_radius / 2)
                )
                pygame.draw.circle(self.menu_drawing_surface,
                                   white,
                                   bullet_pos,
                                   bullet_radius)

            item_pos += vec2(0, h)

        if menu.browse_files:
            font_menu_file_explorer_dirname = self.fonts["regular"]["menu_file_explorer_dirname"]

            item_pos += file_explorer_margin
            explorer_pos = vec2(*item_pos)
            f_explorer_surf = pygame.Surface((self.screen_size[0] - self.screen_size[0] / 2.5,
                                              self.screen_size[1] - explorer_pos[1] - self.screen_size[1] / 10))

            f_explorer_surf.fill((0, 0, 255))
            explorer_size = f_explorer_surf.get_size()

            f_items = menu.file_explorer.get_items()
            visible_f_items = f_items
            h = line_h_small
            max_items = int(explorer_size[1] / h)

            selected_item = next((it for it in f_items if it.selected), None)
            index_of_selected = f_items.index(
                selected_item) if selected_item else -1

            if index_of_selected >= max_items:
                remove_on_top = (index_of_selected - max_items)
                visible_f_items = list()
                for (i, it) in enumerate(f_items):
                    if it.read_only:
                        visible_f_items.append(it)
                    elif i - len(visible_f_items) > remove_on_top:
                        visible_f_items.append(it)

            for f_it in visible_f_items:
                font = font_menu_file_explorer_dirname if f_it.dirname else font_menu_small

                it_surf = pygame.Surface((explorer_size[0], h),
                                         pygame.SRCALPHA)
                left_shift = 50 if f_it.abs_path else 25 if f_it.dirname else 10
                if f_it.selected:
                    it_surf.fill(white)
                    it_surf.blit(font.render(f_it.text, False, (0, 0, 0)),
                                 (left_shift, 0))
                else:
                    color = white if f_it.abs_path else grey if f_it.dirname else grey2
                    it_surf.blit(font.render(f_it.text, False, color),
                                 (left_shift, 0))

                f_explorer_surf.blit(it_surf, item_pos - explorer_pos)
                item_pos += vec2(0, h)

            self.menu_drawing_surface.blit(f_explorer_surf, explorer_pos)

        if notification:
            lines = notification.split("\n")
            line_h = font_menu_notification.get_height()
            for (i, l) in enumerate(lines):
                self.menu_drawing_surface.blit(
                    font_menu_notification.render(l, False, yellow),
                    (10, 10 + i*line_h))

        self.__render(True)

    def __render(self, menu=False):
        if menu:
            self.rendering_surface.blit(self.menu_drawing_surface, (0, 0))
        else:
            self.rendering_surface.blit(pygame.transform.scale(self.drawing_surface,
                                                               self.render_size),
                                        (self.x_rendering_offset, 0),
                                        (0, 0, self.render_size[0], self.render_size[1]))

        pygame.display.flip()
