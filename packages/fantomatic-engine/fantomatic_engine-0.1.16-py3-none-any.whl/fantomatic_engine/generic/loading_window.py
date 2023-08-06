import pygame


class LoadingWindow:
    def __init__(self, text: str):
        self.font = pygame.font.SysFont("mono", 18)
        self.font.set_bold(True)
        self.text = text
        self.text_dots = ""
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_size = self.text_surf.get_size()
        dots_surf = self.font.render("...", True, (255, 255, 255))
        dots_size = dots_surf.get_size()
        self.padding = 30
        self.window = pygame.display.set_mode((text_size[0] + dots_size[0] + 2 * self.padding,
                                               text_size[1] + 2 * self.padding),
                                              pygame.NOFRAME)
        self.frames = 0

    def clear(self):
        self.window.fill((40, 40, 40))

    def update_text(self):
        self.text_dots = self.text_dots + "." if self.frames % 4000 == 0 else self.text_dots
        if len(self.text_dots) > 3:
            self.text_dots = ""
        text = self.text + self.text_dots
        self.text_surf = self.font.render(text, True, (255, 255, 255))

    def draw(self):
        self.frames += 1
        self.clear()
        self.update_text()

        text_size = self.text_surf.get_size()
        win_size = self.window.get_size()

        self.window.blit(
            self.text_surf, (self.padding,
                             win_size[1] - self.padding - text_size[1]))

        pygame.display.flip()
