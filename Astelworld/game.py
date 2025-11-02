import math
import pygame
import random
import sys

from scripts.entities import PhysicsEntity, Player, Enemy
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
        # self.screen = pygame.display.set_mode((320, 240))5
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
            'player/fall' : Animation(load_images('entities/player/fall', (226, 138, 172))),
            'slime/idle' : Animation(load_images('entities/slime/idle'), img_dur=12),
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
        self.level = 0
        self.load_level(self.level)
        self.screenshake = 0

        

    def load_level(self, map_id):
        self.tilemap.load(f"data/maps/{map_id}.json")
        # 파티클
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        # 적 스포너
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)], keep=False):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (20, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0] # 카메라 위치(position)
        self.dead = 0
        self.player.air_time = 0
        self.transition = -30

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
            # self.display.blit(self.assets['background'], (0, 0))
            self.display.fill((0,0,0))

            self.display.blit(self.assets['background'], (0, 0))
            self.screenshake = max(0, self.screenshake - 1)

            if not len(self.enemies): # 적이 없으면 다음 레벨(맵)로 변경한다!
                self.transition += 1
                if self.transition > 30:
                    self.level += 1
                    self.load_level(self.level)
            if self.transition < 0: # 연출
                    self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(self.level)

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
                    if event.key == pygame.K_ESCAPE:
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

                        elif self.player.is_fly:
                            self.player.jump_attack()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 0
                    if event.key == pygame.K_SPACE:
                        self.player.charge = pygame.time.get_ticks() - self.player.charge
                        self.player.jump()

            self.tilemap.render(self.display, render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                # 적 히트박스 표시
                # self.rectangle = enemy.rect()
                # self.rectangle.x -= render_scroll[0]
                # self.rectangle.y -= render_scroll[1]
                # pygame.draw.rect(self.display, (0, 0, 0), self.rectangle, 2)

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
            # 총알
            # [[x, y], direction, timer]
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
            # self.rectangle = self.player.rect()
            # self.rectangle.x -= render_scroll[0]
            # self.rectangle.y -= render_scroll[1]
            # pygame.draw.rect(self.display, (0, 0, 0), self.rectangle, 2)

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

            menu_rect = pygame.Rect(120, 90, 400, 300)

            pygame.draw.rect(self.screen, (240, 240, 240), menu_rect, border_radius=12)
            # pygame.draw.rect(self.screen, (30, 30, 30), menu_rect, 3, border_radius=12)

            pygame.display.update()

Game().run()