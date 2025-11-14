import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera
from scripts.entities import Player

class Maingame(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.camera = Camera(game)
        self.player = Player(game, 'player', (16, 16), (50, 120))

        self.camera.set_target(self.player)

    def handle_events(self, events):
        # 입력 감지
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.state["left"] = True
                if event.key == pygame.K_RIGHT:
                    self.player.state["right"] = True
                if event.key == pygame.K_SPACE:
                    self.player.state["space"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.state["left"] = False
                if event.key == pygame.K_RIGHT:
                    self.player.state["right"] = False
                if event.key == pygame.K_SPACE:
                    self.player.state["space"] = False

        # 충돌 감지
        self.player.handle_collision()

    def update(self, dt):
        self.player.update(dt)
        self.camera.follow()

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['background'], (-self.camera.offset[0], -self.camera.offset[1]))
        self.player.render(surf, self.camera.offset)