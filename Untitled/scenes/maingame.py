import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera
from scripts.entities import Player
from scripts.hud import Player_hud

class Maingame(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.camera = Camera(game)
        self.player = Player(game, 'player', (16, 16), (self.game.screen.get_width() // 2, self.game.display.get_height() // 2))

        self.p_hud = Player_hud(game)

        self.option_idx = 1 # 0 = 왼쪽, 1 = 정면, 2 = 오른쪽
        self.camera.set_target(self.player)

    def handle_events(self, events):
        # 입력 감지
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not self.player.state["moving"]:
                if event.key == pygame.K_LEFT:
                    self.option_idx = self.option_idx - 1 if self.option_idx > 0 else 2
                if event.key == pygame.K_RIGHT:
                    self.option_idx = self.option_idx + 1 if self.option_idx < 2 else 0
                if event.key == pygame.K_SPACE:
                    self.judge_movement()

    def update(self, dt):
        self.p_hud.update(self.option_idx)
        self.player.update(dt)
        # 충돌 감지
        self.player.handle_collision()
        self.camera.follow()

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['background'], (-self.camera.offset[0], -self.camera.offset[1]))
        self.player.render(surf, self.camera.offset)

        # 왼쪽, 오른쪽 선택
        if not self.player.state["moving"]:
            self.p_hud.render(surf)

    def judge_movement(self):
        if self.option_idx == 1:
            return
        
        self.player.state["moving"] = True
        if self.option_idx == 0:
            self.player.state["left"] = True
        if self.option_idx == 2:
            self.player.state["right"] = True