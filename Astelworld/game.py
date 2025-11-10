import math
from xml.dom.minidom import Entity
import pygame
import random
import sys

from scripts.entities import Eyeball, Player, Slime, Portal, Star
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.hud import Hp, Timer

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.paused_time = 0
        self.timer = Timer(self)
        # self.screen = pygame.display.set_mode((320, 240))
        self.screen = pygame.display.set_mode((640, 480))
        # self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'hp' : load_images('ui/hp'),
            'snow' : load_images('tiles/snow'),
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'meteor' : load_images('tiles/meteor'),
            'player' : load_image('entities/player.png'),
            'background0' : load_image('background0.png'),
            'background1' : load_image('background1.png'),
            'background2' : load_image('background2.png'),
            'player/landing' : Animation(load_images('entities/player/landing'), img_dur=20, loop=True),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=20),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/run' : Animation(load_images('entities/player/run')),
            'player/charging' : Animation(load_images('entities/player/charging')),
            'player/charging2' : Animation(load_images('entities/player/charging_anim'), img_dur=10),
            'player/charging3' : Animation(load_images('entities/player/charging_anim'), img_dur=3),
            'player/fall' : Animation(load_images('entities/player/fall')),
            'slime/idle' : Animation(load_images('entities/slime/idle'), img_dur=12),
            'eyeball/idle' : Animation(load_images('entities/eyeball/idle'), img_dur=12),
            'eyeball/run' : Animation(load_images('entities/eyeball/run'), img_dur=12),
            'eyeball/attack' : Animation(load_images('entities/eyeball/attack'), img_dur=17, loop=False),
            'portal/idle' : Animation(load_images('tiles/portal', (255, 255, 255)), img_dur=12),
            'star/idle' : Animation(load_images('tiles/star'), img_dur=12),
            'particle/leaf' : Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle' : Animation(load_images('particles/particle'), img_dur=5, loop=False),
            'particle/player_particle' : Animation(load_images('particles/player_particle'), img_dur=5, loop=False),
            'particle/burst' : Animation(load_images('particles/player_particle'), img_dur=20, loop=False),
            'gun' : load_image('gun.png'),
            'projectile' : load_image('projectile.png'),
        }
        self.player = Player(self, (50, 50), (22, 27))
        self.movement = [0, 0, 0, 0]
        self.tilemap = Tilemap(self, tile_size = 16)
        self.level = '0'
        self.cleared_maps = set()
        self.screenshake = 0
        self.visual_portals = []
        self.disappearing_tiles = []
        self.hp_ui = Hp(self, self.player)

        self.background = 'background0'
        self.background_idx = 0

        self.final_score = None

        self.pos_queue = [[100, self.display.get_height() - 30]] # 포탈 타기 전 플레이어의 위치를 저장하는 리스트
        self.load_level(self.level)
        
    def run(self):
        play = True

        while play:
            self.clock.tick(60) # 60fps
            self.display.blit(self.assets[self.background], (0, 0))
            self.screenshake = max(0, self.screenshake - 1)

            if self.level != '0' and not len(self.enemies): # 맵의 모든 적을 처치했고, 현재 맵이 0번맵이 아니라면
                self.cleared_maps.add(self.level)
                self.transition += 1
                if self.transition > 30:
                    self.load_level('0')
            if self.transition < 0: # 연출
                    self.transition += 1

            if self.player.hp <= 0:
                self.dead += 1
                self.player.hp = self.player.max_hp

            if self.dead:
                self.screenshake = max(16, self.screenshake)
                for i in range(5):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                    self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.dead += 1
                if self.dead > 40:
                    self.load_level(self.level)

            # 카메라 고정
            if self.level == '0':
                self.scroll[0] = 0
                if self.player.rect().top < self.scroll[1]:
                    self.scroll[1] -= self.display.get_height()
                    self.background_idx = min(2, self.background_idx + 1)
                    self.background = f"background{self.background_idx}"
                elif self.player.rect().top > self.scroll[1] + self.display.get_height():
                    self.scroll[1] += self.display.get_height()
                    self.background_idx = max(0, self.background_idx - 1)
                    self.background = f"background{self.background_idx}"

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

                    if event.key == pygame.K_r:
                        # print(self.player.pos)
                        # self.player.pos = [105, -360]
                        # print(self.display.get_size())
                        self.__init__()

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
                        if self.player.jump_cnt and not self.player.is_fly:
                            self.player.charge += 1
                            self.player.is_charging = True
                            self.player.jump_cnt -= 1
                            self.movement = [0, 0, 0, 0]

                        elif self.player.is_fly and self.level != '0':
                            self.player.jump_attack()

                # 키 업
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 0
                    if event.key == pygame.K_SPACE:
                         
                        # self.player.charge = pygame.time.get_ticks() - self.player.charge - self.paused_time
                        self.player.jump()


            keys = pygame.key.get_pressed()
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not self.player.is_fly:
                if self.player.is_charging:
                    self.player.last_movement = [0, 0, 0, 0]
                

            # 타일 맵 랜더링
            self.tilemap.render(self.display, render_scroll)

            # 사라지는 타일 애니메이션
            for i, (tile, timer) in enumerate(self.disappearing_tiles):
                self.disappearing_tiles[i][1] = max(0, timer - 1) # 타이머 감소
                tile_img = self.assets[tile['type']][tile['variant']].copy()
                alpha = int(255 * (timer / 100))
                # if 10 < timer < 60:
                #     alpha = 125
                # if timer <= 10:
                #     alpha = 0
                tile_img.set_alpha(alpha)
                self.display.blit(tile_img, (tile['pos'][0] * self.tilemap.tile_size - render_scroll[0], tile['pos'][1] * self.tilemap.tile_size - render_scroll[1]))
            self.disappearing_tiles = [t for t in self.disappearing_tiles if t[1] > 0] # 타이머가 0인 타일은 제거

            # 포탈 애니메이션 렌더링
            for portal in self.visual_portals.copy():
                portal.update()
                x_offset = 16

                if str(portal.destination) in self.cleared_maps:
                    self.visual_portals.remove(portal)

                portal.render(self.display, (render_scroll[0] + x_offset, render_scroll[1]))

            for star in self.visual_goal.copy():
                star.update()
                star.render(self.display, (render_scroll[0] + 8, render_scroll[1] + 16))
                # self.show_hitbox(star, render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                # 적 히트박스 표시
                # self.show_hitbox(enemy, render_scroll)

                if kill:
                    self.enemies.remove(enemy)

            # 플레이어 업데이트, 렌더링
            if not self.dead:
                self.player.update(self.tilemap, self.movement)
                self.hp_ui.update()
                self.hp_ui.render(self.display)
                self.player.render(self.display, render_scroll)

            self.timer.update()
            self.timer.render(self.display)
            
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
                            self.player.hp -= 1
                            self.screenshake = max(16, self.screenshake)
                        self.player.enemy_collision_side(enemy)

            # 포탈 충돌 감지
            for portal in self.portals:
                portal_rect = pygame.Rect(portal['pos'][0], portal['pos'][1], portal['size'][0], portal['size'][1])
                if self.player.rect().colliderect(portal_rect) and str(portal['destination']) not in self.cleared_maps:
                    self.pos_queue.append(list(self.player.pos))
                    self.level = str(portal['destination'])
                    self.load_level(self.level)

            # 목적지 충돌 감지
            for star in self.visual_goal:
                star_rect = pygame.Rect(star.pos[0], star.pos[1], star.size[0], star.size[1])
                if self.player.rect().colliderect(star_rect):
                    self.final_score = self.timer.get_time()
                    self.show_score()
                    # play = False
                    self.__init__()

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
                        self.player.hp -= 1
                        self.player.knockback_immunity = self.player.max_knockback_immunity
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

    def load_level(self, map_id):
        removed_tiles = self.tilemap.load(f"data/jump/maps/{map_id}.json", self.cleared_maps)
        for tile in removed_tiles:
            is_animating = False
            for t, _ in self.disappearing_tiles:
                if t['pos'] == tile['pos']:
                    is_animating = True
                    break
            if not is_animating:
                self.disappearing_tiles.append([tile, 120]) # [tile, timer]

        self.level = map_id
        # 파티클
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        # 적 스포너
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)], keep=False):
            if spawner['variant'] == 0 and self.level != '0':
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1 and self.level != '0':
                self.enemies.append(Slime(self, spawner['pos'], (20, 15)))
            elif spawner['variant'] == 2 and self.level != '0':
                self.enemies.append(Eyeball(self, spawner['pos'], (32, 32)))
            

        if self.level == '0':
            if not len(self.pos_queue):
                self.player.pos = [100, self.display.get_height() - 30]
            else:
                self.player.pos = self.pos_queue.pop(0)
                self.movement = [0, 0, 0, 0]

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0] # 카메라 위치(position)
        self.dead = 0
        self.player.knockback_immunity = 0
        self.player.air_time = 0
        self.transition = -30

        self.portals = self.tilemap.portals
        self.goal = self.tilemap.goal
        self.visual_portals = []
        self.visual_goal = []
    
        for portal in self.portals:
            self.visual_portals.append(Portal(self, portal['pos'], portal['size'], destination=portal['destination']))

        for star in self.goal:
            self.visual_goal.append(Star(self, star['pos'], star['size'], pos_offset=(16, 16)))

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

    def ingame_menu(self):
        running = True
        base_screen = self.screen.copy()

        pause_time = pygame.time.get_ticks()

        while running:
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

        resume_time = pygame.time.get_ticks()
        self.paused_time += resume_time - pause_time

        if self.player.is_charging:
            self.player.factor = 0
            self.player.is_charging = False
            self.player.jump_cnt = 1
            self.player.last_movement = [0,0,0,0]
            self.player.charge = 0

    def show_hitbox(self, entity : Entity, offset=(0, 0)):
        rectangle = entity.rect()
        rectangle.x -= offset[0]
        rectangle.y -= offset[1]
        pygame.draw.rect(self.display, (0, 0, 0), rectangle, 2)

    def show_score(self):
        self.clock.tick(60)
        base_screen = self.screen.copy()

        score_font = pygame.font.Font('data/jump/font/NeoDunggeunmoPro-Regular.ttf', 28)
        score_font.set_bold(True)

        running = True
        while running:
            self.screen.blit(base_screen, (0, 0))

            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))

            txt = score_font.render(f'Your Score : {self.final_score}', False, (255, 255, 255))
            self.screen.blit(txt, (self.screen.get_rect().centerx - (txt.get_width() // 2), self.screen.get_rect().centery - (txt.get_height() // 2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

            pygame.display.update()

Game().run()