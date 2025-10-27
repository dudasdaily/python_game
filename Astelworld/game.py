import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'decor' : load_images('tiles/decor'), 
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=12),
            'player/up' : Animation(load_images('entities/player/up')),
            'player/down' : Animation(load_images('entities/player/down') ),
            'player/left' : Animation(load_images('entities/player/left')),
            'player/right' : Animation(load_images('entities/player/right')),
        }
        self.player = Player(self, (50, 50), (15, 25))
        self.movement = [0, 0, 0, 0] # 좌, 우, 상, 하
        self.tilemap = Tilemap(self, tile_size = 16)
        self.scroll = [0, 0] # 카메라 위치(position)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 25
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 25
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.player.update(self.tilemap, self.movement)
            self.tilemap.render(self.display, render_scroll)
            self.player.render(self.display, render_scroll)

            # 플레이어 히트박스 표시
            # self.rectangle = self.player.rect()
            # self.rectangle.x -= render_scroll[0]
            # self.rectangle.y -= render_scroll[1]
            # pygame.draw.rect(self.display, (0, 0, 0), self.rectangle, 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -1
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 1
                    if event.key == pygame.K_UP:
                        self.movement[2] = -1
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = 1

                    if event.key == pygame.K_F1:
                        print()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 0
                    if event.key == pygame.K_UP:
                        self.movement[2] = 0
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = 0

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

Game().run()