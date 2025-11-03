import math
from xml.dom.minidom import Entity
import pygame
import random
import sys

from scripts.entities import PhysicsEntity, Player, Enemy, Portal
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 480))
        # self.screen = pygame.display.set_mode((1280, 960))
        # self.screen = pygame.display.set_mode((320, 240))
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'snow' : load_images('tiles/snow'),
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'player/landing' : Animation(load_images('entities/player/landing'), img_dur=20, loop=True),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=20),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/run' : Animation(load_images('entities/player/run')),
            'player/charging' : Animation(load_images('entities/player/charging')),
            'player/fall' : Animation(load_images('entities/player/fall')),
            'slime/idle' : Animation(load_images('entities/slime/idle'), img_dur=12),
            'portal/idle' : Animation(load_images('tiles/portal', (255, 255, 255)), img_dur=12),
            'enemy/idle' : Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run' : Animation(load_images('entities/enemy/run'), img_dur=6),
            'particle/leaf' : Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle' : Animation(load_images('particles/particle'), img_dur=5, loop=False),
            'particle/burst' : Animation(load_images('particles/particle'), img_dur=20, loop=False),
            'gun' : load_image('gun.png'),
            'projectile' : load_image('projectile.png'),
        }
        self.player = Player(self, (50, 50), (28, 27))
        self.movement = [0, 0, 0, 0]
        self.tilemap = Tilemap(self, tile_size = 16)
        self.level = '0'
        self.cleared_maps = set()
        self.screenshake = 0
        self.portals = []
        self.visual_portals = []
        self.disappearing_tiles = []

        self.pos_queue = [[100, self.display.get_height() - 30]]

        self.load_level(self.level)
        

    def load_level(self, map_id):
        removed_tiles = self.tilemap.load(f"data/maps/{map_id}.json", self.cleared_maps)
        for tile in removed_tiles:
            is_animating = False
            for t, _ in self.disappearing_tiles:
                if t['pos'] == tile['pos']:
                    is_animating = True
                    break
            if not is_animating:
                self.disappearing_tiles.append([tile, 60])

        self.level = map_id
        # 파티클
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        # 적 스포너
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)], keep=False):
            if spawner['variant'] == 0 and self.level != '0':
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (20, 15)))

        if self.level == '0':
            self.player.pos = self.pos_queue.pop(0)

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0] # 카메라 위치(position)
        self.dead = 0
        self.player.air_time = 0
        self.transition = -30

        self.portals = self.tilemap.portals
        self.visual_portals = []
        for portal in self.portals:
            self.visual_portals.append(Portal(self, portal['pos'], portal['size']))

    def kill_enemy(self, enemy):
        """적을 죽이고 파티클 생성"""
        for i in range(30):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.sparks.append(Spark(enemy.rect().center, angle, 2 + random.random()))
            self.particles.append(Particle(self, 'particle', enemy.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
        
        self.sparks.append(Spark(enemy.rect().center, 0, 5 + random.random()))
        self.sparks.append(Spark(enemy.rect().center, math.pi, 5 + random.random()))
        self.enemies.remove(enemy)

    def run(self):
        while True:
            self.clock.tick(60) # 60fps
            self.display.blit(self.assets['background'], (0, 0))
            # self.display.fill((0,0,0))
            self.screenshake = max(0, self.screenshake - 1)

            if self.level != '0' and not len(self.enemies): # 맵의 모든 적을 처치했고, 현재 맵이 0번맵이 아니라면
                self.cleared_maps.add(self.level)
                self.transition += 1
                if self.transition > 30:
                    self.load_level('0')
            if self.transition < 0: # 연출
                    self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(self.level)

            # 카메라 고정
            if self.level == '0':
                self.scroll[0] = 0
                if self.player.rect().top < self.scroll[1]:
                    self.scroll[1] -= self.display.get_height()
                if self.player.rect().bottom > self.scroll[1] + self.display.get_height():
                    self.scroll[1] += self.display.get_height()
            else:
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 25
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 25
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # 나무 잎 파티클
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, [0.1, 0.3], frame=random.randint(0, 20)))

            # 유저 입력
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 키 다운
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.movement = [0, 0, 0, 0]
                        self.ingame_menu()

                    if event.key == pygame.K_LEFT and not self.player.is_fly:
                        if not self.player.is_charging:
                            self.movement[0] = 1
                        else:
                            self.player.last_movement = [1, 0, 0, 0]

                    if event.key == pygame.K_RIGHT and not self.player.is_fly:
                        if not self.player.is_charging:
                            self.movement[1] = 1
                        else:
                            self.player.last_movement = [0, 1, 0, 0]
                    
                    if event.key == pygame.K_SPACE:
                        self.player.charge = pygame.time.get_ticks()

                        if self.player.jump_cnt and not self.player.is_fly:
                            self.player.is_charging = True
                            self.player.jump_cnt -= 1
                            self.movement = [0, 0, 0, 0]

                        # elif self.player.is_fly and self.player.factor != 0:
                        #     self.player.jump_attack()

                        elif self.player.is_fly and self.level != '0':
                            self.player.jump_attack()

                # 키 업
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 0
                    if event.key == pygame.K_SPACE:
                        self.player.charge = pygame.time.get_ticks() - self.player.charge
                        self.player.jump()

            # 타일 맵 랜더링
            self.tilemap.render(self.display, render_scroll)

            # 사라지는 타일 애니메이션
            for i, (tile, timer) in enumerate(self.disappearing_tiles):
                self.disappearing_tiles[i][1] = max(0, timer - 1)
                tile_img = self.assets[tile['type']][tile['variant']].copy()
                alpha = int(255 * (timer / 60))
                tile_img.set_alpha(alpha)
                self.display.blit(tile_img, (tile['pos'][0] * self.tilemap.tile_size - render_scroll[0], tile['pos'][1] * self.tilemap.tile_size - render_scroll[1]))
            self.disappearing_tiles = [t for t in self.disappearing_tiles if t[1] > 0]

            for portal in self.visual_portals:
                portal.update()
                portal.render(self.display, (render_scroll[0] + 20, render_scroll[1] + 20))

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                # 적 히트박스 표시
                # self.show_hitbox(enemy, render_scroll)

                if kill:
                    self.enemies.remove(enemy)
            if not self.dead:
                self.player.update(self.tilemap, self.movement)
                self.player.render(self.display, render_scroll)
            
            # 플레이어와 적 충돌 감지
            for enemy in self.enemies:
                if self.player.rect().colliderect(enemy.rect()):
                    pr = self.player.rect()
                    er = enemy.rect()

                    # 1) 스톰프(플레이어가 적의 위를 밟는 경우)
                    if pr.bottom <= er.top + 5 and self.player.velocity[1] > 1.5:
                        self.screenshake = max(16, self.screenshake)
                        self.player.enemy_collision_vertical(self, self.player, enemy)

                    # 2) 아래(플레이어가 적의 아랫면에 부딪힌 경우: 위로 올라가던 중이고 수평으로 겹치는 상태)
                    elif pr.top <= er.bottom and self.player.velocity[1] < 0 and (pr.centerx >= er.left and pr.centerx <= er.right):
                        self.player.enemy_collision_below(enemy)

                    # 3) 그 외는 좌/우 측면 충돌로 간주
                    else:
                        if not self.player.knockback_immunity:
                            self.screenshake = max(16, self.screenshake)
                        self.player.enemy_collision_side(enemy)

            # 포탈 충돌 감지
            for portal in self.portals:
                portal_rect = pygame.Rect(portal['pos'][0], portal['pos'][1], portal['size'][0], portal['size'][1])
                if self.player.rect().colliderect(portal_rect) and str(portal['destination']) not in self.cleared_maps:
                    self.pos_queue.append(list(self.player.pos))
                    self.level = str(portal['destination'])
                    self.load_level(self.level)

            # 총알
            # projectile[] = [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1] # [x, y]의 x에 더한다는 것
                projectile[2] += 1 # timer += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))

                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                        
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif not self.player.is_attacking: # 점프 공격중에는 총알 안맞음
                    if self.player.rect().collidepoint(projectile[0]) and not self.player.knockback_immunity: # 플레이어가 총알에 맞았다면
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
            
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)

                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # 낙엽을 좌우로 흔들어줌
                if kill:
                    self.particles.remove(particle)

            # 플레이어 히트박스 표시
            # self.show_hitbox(self.player, render_scroll)

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height()), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
            pygame.display.update()

    def ingame_menu(self):
        running = True

        base_screen = self.screen.copy()

        while running:
            # self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.clock.tick(60)
            self.screen.blit(base_screen, (0, 0))

            # overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            # overlay.fill((0, 0, 0, 140))
            # self.screen.blit(overlay, (0, 0))

            menu_rect = pygame.Rect(0, 0, 400, 300)
            menu_rect.center = (self.display.get_width() // 2, self.display.get_height() // 2)

            pygame.draw.rect(self.screen, (240, 240, 240), menu_rect, border_radius=12)
            # pygame.draw.rect(self.screen, (30, 30, 30), menu_rect, 3, border_radius=12)

            pygame.display.update()

    def show_hitbox(self, entity : Entity, offset=(0, 0)):
        rectangle = entity.rect()
        rectangle.x -= offset[0]
        rectangle.y -= offset[1]
        pygame.draw.rect(self.display, (0, 0, 0), rectangle, 2)

Game().run()