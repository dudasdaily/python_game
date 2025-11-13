import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera
from scripts.entities import Player

class Maingame(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.camera = Camera()
        self.player = Player()
        
        # 이미지 에셋들
        self.assets = {

        }

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
        pass

    def render(self, surf, offset=(0, 0)):
        surf.fill((255, 255, 255))