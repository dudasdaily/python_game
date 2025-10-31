from shutil import move
from numpy import tile
import pygame
import math
import random
from pygame.math import Vector2
from scripts.particle import Particle 
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type # 엔티티 타입 : 'player'
        self.pos = list(pos)
        self.size = size
        self.velocity = [1.5, 1.5]
        self.last_movement = [0, 0, 0, 0]

        self.collisions = { 'up' : False, 'down' : False, 'right' : False, 'left' : False } # 충돌이 일어났는가?
        self.collision_normal = Vector2()
        self.frame_move = Vector2()

        self.action = ''
        self.anim_offset = (0, 0) # 이미지 패딩 처리
        self.flip = False
        self.is_fly = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action: # 이거 안해주면 애니메이션 frame이 0으로 계속 새로 생성되어서 재생 안할거임
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    
    def update(self, tilemap, movement=(0,0,0,0)):
        self.collisions = { 'up' : False, 'down' : False, 'right' : False, 'left' : False }
        
        x = (self.velocity[0] * (movement[1] - movement[0]))
        y = self.velocity[1]

        if (movement[0] != 0 and movement[1] != 0):
            x = 0

        # 이번 프레임 이동 저장
        self.frame_move = Vector2(x, y)
        frame_movement = (x, y)
        normal_sum = Vector2()

        # x축 충돌 감지
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.rect()):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # 엔티티가 오른쪽으로 가다가 충돌
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    normal_sum += Vector2(-1, 0)
                if frame_movement[0] < 0: # 엔티티가 왼쪽으로 가다가 충돌
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    normal_sum += Vector2(1, 0)

                self.pos[0] = entity_rect.x

        #y축 충돌 감지
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.rect()):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0: # 위로 가다가 충돌
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    normal_sum += Vector2(0, 1)

                if frame_movement[1] > 0: # 아래로 가다가 충돌
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                self.pos[1] = entity_rect.y

        self.collision_normal = normal_sum.normalize() if normal_sum.length() > 0 else Vector2()

        self.velocity[0] = max(1.5, self.velocity[0] - 0.1)
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        self.animation.update()

    def render(self, surf, offset = (0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'slime', pos, size)
        self.anim_offset = (0, 0)
        self.walking = 0 # 적이 걷는 시간의 타이머, 0이되면 멈춘다

    def update(self, tilemap, movement=(0, 0, 0, 0)):
        # 적이 걷고 있을 때
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23 )):
                if self.collisions['left'] or self.collisions['right']:
                    self.flip = not self.flip 
                else:
                    movement = [0.5, 0, 0, 0] if self.flip else [0, 0.5, 0, 0]
            else:
                self.flip = not self.flip 
            self.walking = max(0, self.walking - 1) # 여기서 업데이트하기 때문에 바로 밑에서 멈춘 순간 프레임을 포착할 수 있음
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))

        # 적이 안걷고 있을 때
        elif random.random() < 0.01: # 적이 안걷고 있으면, 60fps에서 평균적으로 100프레임당 한번 씩(약 1.67초) 적이 걸을 타이머를 랜덤(30 ~ 119)로 세팅한다!
            self.walking = random.randint(30, 120)
        super().update(tilemap, movement=movement)
        # 적 애니메이션 설정
        # if movement[0] != 0 or movement[1] != 0:
        #     self.set_action('run')
        # else:
        #     self.set_action('idle')

        if self.game.player.is_fly:
            if self.rect().colliderect(self.game.player.rect()):
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True # kill = True를 반환!
             
        

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.anim_offset = (0, -5)
        self.air_time = 0
        self.jump_cnt = 1
        self.is_charging = False
        self.charge = 0
        self.factor = 0
        self.is_attacking = False

    def update(self, tilemap, movement=(0,0,0,0)):
        if self.factor != 0:
            movement = self.last_movement

        if self.is_fly:
            self.air_time += 1
        super().update(tilemap, movement = movement)

        if (self.is_attacking):
            pvelocity = [0, random.random() * 3]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=2))

        if self.is_fly and self.collision_normal.length() > 0:
            self._bounce_by_reflection(restitution=0.6, friction=0.1)

        if not self.collisions['down']:
            self.is_fly = True

        if self.collisions['down']:
            if self.is_fly:
                self.jump_cnt = 1
                self.is_fly = False
                # self.game.movement = [0, 0, 0, 0]
                self.air_time = 0
                self.factor = 0

                if self.is_attacking:
                    # 파티클 버스트
                    for i in range(20):
                        angle = random.random() * 2 * math.pi  # 원의 라디안
                        speed = random.random() * 0.5 + 0.5 # 0.5 ~ 1.0
                        pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed] # 파티클의 속도 : angle에 따라서 속도를 만듦
                        self.game.particles.append(Particle(self.game, 'burst', self.rect().center, velocity=pvelocity, frame=random.randint(0, 4)))
                    self.is_attacking = False


            self.velocity[1] = 1.5 

        if self.is_charging:
            self.set_action('charging')
        elif self.air_time >= 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.flip = True
            self.set_action('run')
        elif movement[1] != 0:
            self.flip = False
            self.set_action('run')
        else:
            self.set_action('idle')

        if not self.is_fly and not self.is_charging:
            self.last_movement = movement

    def jump(self):
        if self.is_charging:
            self.is_charging = False
            if 0 <= self.charge < 500:
                self.factor = 1
                self.velocity[0] = 3
                self.velocity[1] = -1.5

            if 500 <= self.charge < 1000:
                self.factor = 2
                self.velocity[0] = 3
                self.velocity[1] = -3
            if self.charge >= 1000:
                self.factor = 3
                self.velocity[0] = 3
                self.velocity[1] = -5
                

            # self.velocity[0] = self.factor
            # self.velocity[1] = -1.5 * self.factor

    def jump_attak(self):
        self.is_attacking = True
        self.last_movement = [0, 0, 0, 0]
        self.velocity[1] = 20
        

    def _bounce_by_reflection(self, restitution=0.8, friction=0.5):
        """
        restitution(탄성계수): 0(완전 비탄성)~1(완전 탄성)
        friction(마찰): 접선 성분 감쇠율
        """
        v_in = Vector2(self.frame_move.x, self.frame_move.y) # 충돌 직전 이동 벡터
        n = Vector2(self.collision_normal.x, self.collision_normal.y)

        # 분해: v = v_n + v_t
        v_n = n * v_in.dot(n)           # 법선 성분
        v_t = v_in - v_n                # 접선 성분

        # 반사: 법선 성분 뒤집고(계수 적용), 접선은 마찰로 감쇠
        v_out = (-restitution) * v_n + (1 - friction) * v_t

        # 엔진의 내부 표현에 맞춰 재설정
        # 1) 수평 속도/방향
        if abs(v_out.x) < 0.05:
            # 거의 수직이라면 좌/우 입력을 해제
            self.last_movement = [0, 0, 0, 0]
            self.velocity[0] = 1.5
        else:
            if v_out.x < 0:
                self.last_movement = [1, 0, 0, 0]  # 왼쪽 유지
            else:
                self.last_movement = [0, 1, 0, 0]  # 오른쪽 유지
            self.velocity[0] = max(1.5, abs(v_out.x))

        # 2) 수직 속도
        # 이 엔진은 +y가 아래이므로 v_out.y가 음수면 위로 튕김
        self.velocity[1] = max(-5, min(5, v_out.y))

    def render(self, surf, offset=(0, 0)):
        if not self.is_attacking:
            super().render(surf, offset=offset)

        