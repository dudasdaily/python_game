import pygame
import sys

from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
MAP_PATH = 'map.json'

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
        
        try:
            self.tilemap.load(MAP_PATH)
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0] # 카메라 위치(position)
        self.clock = pygame.time.Clock()

        self.tile_list = list(self.assets) # 'grass', 'decor', ... 이런 스트링 리스트
        self.tile_group = 0 # tile_list에 대한 인덱스
        self.tile_variant = 0 # 0, 1, 2, ... (0.png, 1.png, 2.png, ... 에 대한 인덱스)

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[0] + self.movement[1]) * 2
            self.scroll[1] += (self.movement[2] + self.movement[3]) * 2


            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) # 0~255의 투명도 조절. 0 == 투명, 255 == 불투명

            mpos = pygame.mouse.get_pos()
            # 화면에는 RENDER_SCALE 만큼 스케일링된 픽셀들이 보일 것임
            # 그래서 우리의 마우스 위치를 RENDER_SCALE만큼 나눠줘야함
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            # 마우스의 타일 좌표
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                # 내 마우스 커서의 위치에서 타일이 어디 놓일것인지 나타냄!
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tile_map[f"{tile_pos[0]};{tile_pos[1]}"] = {'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos' : tile_pos}
            

            if self.right_clicking:
                tile_loc = f"{tile_pos[0]};{tile_pos[1]}"
                if tile_loc in self.tilemap.tile_map:
                    del self.tilemap.tile_map[tile_loc]
                for tile in self.tilemap.off_grid_tiles.copy(): # 이터레이터를 망치고 싶지 않아서 copy를 씀
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos): # 다른 사각형 말고, 좌표와 충돌하는지 검사!
                        self.tilemap.off_grid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.off_grid_tiles.append({'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos' : (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})

                    if event.button == 3:
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4: # 휠 업
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5: # 휠 다운
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = -1
                    if event.key == pygame.K_d:
                        self.movement[1] = 1
                    if event.key == pygame.K_w:
                        self.movement[2] = -1
                    if event.key == pygame.K_s:
                        self.movement[3] = 1
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save(MAP_PATH)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[1] = 0
                    if event.key == pygame.K_w:
                        self.movement[2] = 0
                    if event.key == pygame.K_s:
                        self.movement[3] = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

Editor().run()