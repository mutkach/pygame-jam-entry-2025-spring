import pygame
from typing import List, Any, Tuple, Dict, Iterable
from pathlib import Path
from collections import OrderedDict, defaultdict
import random
from figure import Figure
from constants import ScreenConstants
from level import Level
import pygame_gui
from PIL import Image

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([ScreenConstants.WIDTH, ScreenConstants.HEIGHT])
gui_manager = pygame_gui.UIManager((ScreenConstants.WIDTH, ScreenConstants.HEIGHT))

check_perspective = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 75), (200, 50)),text='Check Perspective',manager=gui_manager)


def main():
    running = True
    clock = pygame.time.Clock()
    level = Level(n_level=6)
    background = pygame.image.load("./assets/backgrounds/level8.png")
    layer = 0
    font = pygame.font.SysFont("Helvetica", 20)

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((0, 0, 0))
        screen.blit(background, (0,0))
        screen.convert_alpha()
        pygame.draw.line(screen, color=(200, 200, 0), 
                         start_pos=(0,ScreenConstants.HEIGHT//2), 
                         end_pos=(ScreenConstants.WIDTH, ScreenConstants.HEIGHT//2), 
                         width=5)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == check_perspective:
                    level.check_perspective()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #probe = level.probe_layer(x,y)
                #if probe:
                #    print(probe)
                #    layer = probe
                level.try_grab(x,y, layer)
            if event.type == pygame.MOUSEBUTTONUP:
                level.try_release(x,y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    layer += 1
                if event.key == pygame.K_MINUS:
                    layer = max(0, layer-1)
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    layer += 1
                else:
                    layer = max(0, layer-1)

            gui_manager.process_events(event)

        gui_manager.update(time_delta)
        level.update(x,y)
        level.draw(screen)

        
        for fig_name,intersections in level.intersections.items():
            for intersect in intersections:
                pygame.draw.circle(screen, color=(10, 0, 0), center=intersect, radius=5)
                fof = font.render(str(fig_name), False, color=(255,0, 125))
                screen.blit(fof, intersect)

        layer_indicator = font.render(f"LAYER: {layer}", True, color=(230, 230, 210))
        screen.blit(layer_indicator, (10, 10))


        gui_manager.draw_ui(screen)
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
