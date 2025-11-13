import pygame
import sys

from scripts.entities import Player
from scripts.camera import Camera
from scenes.scene import Scene, SceneManager

FRAME = 60

pygame.init()

class Game:
    def __init__(self):
        # pygame 설정들
        self.screen = pygame.display.set_mode((640, 480))
        self.display =pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        # 에셋
        self.assets = {
            
        }
        
        # 카메라 설정
        self.camera = Camera(self)

        # Scene 관련 설정
        self.sm = SceneManager(None)
        self.first_scene = Scene(self.sm)

    def run(self):
        play = True
        while play:
            self.display.fill((255, 255, 0)) # 배경 렌더링
            dt = self.clock.tick(FRAME) / 1000 # dt = 직전 업데이트로부터 흐른 시간 (sec)

            # 유저 입력
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 화면 렌더링
            pygame.transform.scale(self.display, self.screen.get_size(), self.screen)
            pygame.display.update()

game = Game()
game.run()