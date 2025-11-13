import pygame
import sys
from scenes.scene import Scene

class Battle(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.KEYUP:
                pass

    def update(self, dt):
        pass

    def render(self, surf):
        surf.fill((0, 0, 0))