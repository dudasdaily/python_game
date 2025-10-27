import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        self.assets = {
            'decor' : load_images('tiles/decor'), 
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
        }
        self.movement = [0, 0, 0, 0] # 좌, 우, 상, 하
        self.tilemap = Tilemap(self, tile_size = 16)
        self.scroll = [0, 0] # 카메라 위치(position)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            self.display.fill((14, 219, 248))

            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 25
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 25
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.player.update(self.tilemap, self.movement)
            self.tilemap.render(self.display, render_scroll)
            self.player.render(self.display, render_scroll)

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