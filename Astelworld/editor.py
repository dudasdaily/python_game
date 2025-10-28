import pygame
import sys

from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'decor' : load_images('tiles/decor'), 
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
        }

        self.movement = [0, 0, 0, 0] # 좌, 우, 상, 하
        self.tilemap = Tilemap(self, tile_size = 16)
        self.scroll = [0, 0] # 카메라 위치(position)
        self.clock = pygame.time.Clock()

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            self.display.fill((0, 0, 0))

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) # 0~255의 투명도 조절. 0 == 투명, 255 == 불투명

            self.display.blit(current_tile_img, (5, 5))

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

Editor().run()