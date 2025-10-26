import sys
import pygame
from scripts.entities import PhysicsEntitiy
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        # self.screen = pygame.display.set_mode((640, 480))
        self.screen = pygame.display.set_mode((320, 240))

        pygame.display.set_caption('test game')

        self.display = pygame.Surface((320, 240)) # 여기에 작은 이미지를 blit한 다음 screen 표면으로 스케일링 할 거임

        self.player = PhysicsEntitiy(self, 'player', (50, 50), (8, 15))
        self.assets = {
            'decor' : load_images('tiles/decor'), 
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }
        self.movement = [False, False]

        self.tilemap = Tilemap(self, tile_size = 16)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60) # 60 FPS -> 60FPS를 맞추도록 sleep
            self.display.fill((14, 219, 248))
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # 플레이어의 위치를 업데이트
            self.tilemap.render(self.display)
            self.player.render(self.display) # 플레이어 이미지 로드!

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # 종료 이벤트
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN: # 키 눌림 이벤트
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                    if event.key == pygame.K_UP:
                        if self.player.jump_cnt < 2:
                            self.player.velocity[1] = -3
                            self.player.jump_cnt += 1

                if event.type == pygame.KEYUP: # 키 떼짐 이벤트
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False

                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) 
            pygame.display.update() # 호출 할 때마다 변경된 사항을 screen에 띄어줌

Game().run()