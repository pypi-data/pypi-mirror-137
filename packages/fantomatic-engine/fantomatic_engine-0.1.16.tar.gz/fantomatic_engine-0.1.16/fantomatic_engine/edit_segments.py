# A helper to build segments coordinates on an image
import pygame
import sys
import os
import json
from getopt import getopt
from generic import ResourcesManager


def main(argv):
    opts, args = getopt(
        argv, "hr:i:o:", ["resources_dir=", "image=", "output=", "help"])
    img = ""
    resources_dir = ""
    output = "output-segments"
    for opt, arg in opts:
        if opt in {"-h", "--help"}:
            print("edit_walls.py -i <image_name> -r <resources_directory>")
            sys.exit()
        elif opt in {"-i", "--image"}:
            img = arg
        elif opt in {"-r", "--resources_directory"}:
            resources_dir = arg
        elif opt in {"-o", "--output"}:
            output = arg
        else:
            print("[ERROR] Unrecognized option ", opt)
            sys.exit(2)

    assert img != "", "Option -i or --image is required."
    assert resources_dir != "", "Option -r or --resources_dir is required."
    assert os.path.isdir(resources_dir), "resources_dir " + \
        resources_dir + "is not a directory."

    output = output.split(".")[0] + ".json"

    pygame.init()
    resources_manager = ResourcesManager(resources_dir)
    resources_manager.load_animations()
    _map = resources_manager.get_animation_set(img)[0]
    screen = pygame.display.set_mode(_map.dimensions)

    s_pressed = False

    segments = list()
    building_segment = list()

    writing = False

    def write_output():
        writing = True
        f = open(output, "w")
        f.write(json.dumps(segments))
        writing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_s:
                s_pressed = event.type == pygame.KEYDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN and s_pressed:
                building_segment.append(event.pos)
                if len(building_segment) == 2:
                    segments.append(building_segment)
                    building_segment = list()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                segments.pop()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o and not writing:
                write_output()

        screen.fill((0, 0, 0))
        screen.blit(_map.get_frame(), _map.get_frame().get_rect())

        for seg in segments:
            pygame.draw.line(screen, (0, 255, 0), seg[0], seg[1])
        pygame.display.flip()


if __name__ == "__main__":
    main(sys.argv[1:])
