from .game import Game, GameConfig
from .generic import LoadingWindow
from _thread import start_new_thread
import sys
import os
import pygame


def show_loading(state, loading_window):
    while not state["ready"]:
        loading_window.draw()


def run_game(argv):
    os.environ["SDL_VIDEO_WINDOW_POS"] = "40,40"

    pygame.init()

    screen_info = pygame.display.Info()

    win_data = {
        "screen_w": screen_info.current_w,
        "screen_h": screen_info.current_h,
        "margin": 60
    }

    conf = GameConfig(argv)

    pygame.font.init()
    pygame.display.set_caption(conf.game_name)
    pygame.mouse.set_visible(False)
    icon_path = os.path.join(conf.resources_dir,
                             "animations",
                             "icon",
                             "icon.png")

    if os.path.isfile(icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))
    else:
        print("[WARNING] icon file was not found in resources directory at "
              + conf.resources_dir
              + "icon/icon.png. Window icon will be not set")

    loading_win = LoadingWindow(conf.game_name + " - Loading ")

    ready_state = {"ready": False}

    start_new_thread(show_loading, (ready_state, loading_win))

    game = Game(conf, win_data, ready_state)

    game.main_loop()

    if __name__ == "__main__":
        run_game(sys.argv[1:])
