import sys
import pygame
from scripts.entities import PhysicsEntitiy
from scripts.utils import load_image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('test game')

        self.clock = pygame.time.Clock()
        self.player = PhysicsEntitiy(self, 'player', (50, 50), (8, 15))
        self.movement = [False, False]

        self.assets = {
            'player' : load_image('entities/player.png')
        }

    def run(self):
        while True:
            self.clock.tick(60) # 60 FPS -> 60FPS를 맞추도록 sleep
            self.screen.fill((14, 219, 248))
            self.player.update((self.movement[1] - self.movement[0], 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # 윈도우의 X버튼
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.player.render(self.screen)
            pygame.display.update() # 호출 할 때 변경된 사항을 screen에 띄어줌



Game().run()
    