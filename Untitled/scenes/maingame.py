import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera

class Maingame(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        pass

    def render(self, surf):
        surf.fill((255, 255, 255))