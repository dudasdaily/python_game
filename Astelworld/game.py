import math
import pygame
import random
import sys

from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'snow' : load_images('tiles/snow'),
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'player/idle' : Animation(load_images('entities/player/idle', (226, 138, 172)), img_dur=10),
            'player/jump' : Animation(load_images('entities/player/jump', (226, 138, 172))),
            'player/charging' : Animation(load_images('entities/player/charging', (226, 138, 172))),
            'player/run' : Animation(load_images('entities/player/run', (226, 138, 172))),
            'particle/leaf' : Animation(load_images('particles/leaf'), img_dur=20, loop=False),
        }
        self.player = Player(self, (50, 50), (28, 27))
        self.movement = [0, 0, 0, 0]
        self.tilemap = Tilemap(self, tile_size = 16)
        self.tilemap.load('map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.particles = []

        self.scroll = [0, 0] # 카메라 위치(position)

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            # self.display.blit(self.assets['background'], (0, 0))
            self.display.fill((0,0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 25
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 25
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, [0.1, 0.3], frame=random.randint(0, 20)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.player.is_fly:
                        if not self.player.is_charging:
                            self.movement[0] = 1
                        else:
                            self.player.direction = [1, 0, 0, 0]

                    if event.key == pygame.K_RIGHT and not self.player.is_fly:
                        if not self.player.is_charging:
                            self.movement[1] = 1
                        else:
                            self.player.direction = [0, 1, 0, 0]
                    
                    if event.key == pygame.K_SPACE:
                        self.player.charge = pygame.time.get_ticks()
                        self.player.jump_cnt += 1

                        if self.player.jump_cnt < 2:
                            self.player.is_charging = True
                            self.player.direction = self.movement.copy()
                            self.movement = [0, 0, 0, 0]
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 0
                    if event.key == pygame.K_SPACE:
                        if self.player.jump_cnt < 2:
                            self.player.charge = pygame.time.get_ticks() - self.player.charge
                            self.player.is_fly = True
                            self.player.is_charging = False

                            factor = 0
                            if 0 <= self.player.charge < 500:
                                factor = 1.25
                            if 500 <= self.player.charge < 1000:
                                factor = 2
                            if self.player.charge >= 1000:
                                factor = 3

                            self.player.velocity[0] = factor
                            self.player.velocity[1] = -1.5 * factor

            self.player.update(self.tilemap, self.movement)
            self.tilemap.render(self.display, render_scroll)
            self.player.render(self.display, render_scroll)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # 낙엽을 좌우로 흔들어줌
                if kill:
                    self.particles.remove(particle)

            # 플레이어 히트박스 표시
            # self.rectangle = self.player.rect()
            # self.rectangle.x -= render_scroll[0]
            # self.rectangle.y -= render_scroll[1]
            # pygame.draw.rect(self.display, (0, 0, 0), self.rectangle, 2)


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

Game().run()