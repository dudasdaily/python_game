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

        self.hurt_cooldown = 0 # 짧은 연속 판정 방지
        self.knockback_timer = 0 # 넉백 유지 시간 선택
        self.knockback_immunity = 0 # 넉백 무적 프레임 (180 프레임)

    def update(self, tilemap, movement=(0,0,0,0)):
        if self.factor != 0:
            movement = self.last_movement

        if self.is_fly:
            self.air_time += 1

        if self.hurt_cooldown > 0:
            self.hurt_cooldown -= 1
        
        if self.knockback_immunity > 0:
            self.knockback_immunity -= 1

        if self.knockback_timer > 0:
            movement = self.last_movement
            self.knockback_timer -= 1
            
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

    def jump_attack(self):
        self.is_attacking = True
        self.last_movement = [0, 0, 0, 0]
        self.velocity[1] = 20

    def enemy_collision_vertical(self, game, player, enemy):
        if player.is_attacking:
            self.game.kill_enemy(enemy)
        else:
            # 적의 히트박스 상단 중앙을 기준으로 법선 벡터 계산 (위쪽 방향)
            enemy_rect = enemy.rect()
            normal = Vector2(0, -1)  # 적의 상단 면의 법선 벡터 (위로 향함)
            
            # 플레이어의 입사 벡터 (충돌 직전 이동 벡터)
            v_in = Vector2(player.frame_move.x, player.frame_move.y)
            
            # 입사 벡터를 법선 성분과 접선 성분으로 분해
            v_n = normal * v_in.dot(normal)  # 법선 성분
            v_t = v_in - v_n                 # 접선 성분
            
            # 반사: 법선 성분만 반대로, 접선 성분은 유지
            restitution = 0.8  # 탄성 계수
            v_out = (-restitution) * v_n + v_t
            
            # 플레이어 위치를 적의 상단 위로 조정
            player.pos[1] = enemy_rect.top - player.size[1]
            
            # 반사된 벡터를 플레이어 속도에 적용
            if abs(v_out.x) < 0.05:
                player.last_movement = [0, 0, 0, 0]
                player.velocity[0] = 1.5
            else:
                if v_out.x < 0:
                    player.last_movement = [1, 0, 0, 0]  # 왼쪽
                else:
                    player.last_movement = [0, 1, 0, 0]  # 오른쪽
                player.velocity[0] = max(1.5, abs(v_out.x))
            
            # 수직 속도 설정 (위로 튕겨나가므로 음수)
            player.velocity[1] = max(-5, min(5, v_out.y))
            self.game.kill_enemy(enemy)
            
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

    def _apply_knockback(self, dir_vec: Vector2, enemy_rect, hop_y: float = 0.0, push_out: bool = True):
        """
        dir_vec: 플레이어가 '밀려날' 방향의 단위벡터(예: 좌(-1,0), 우(1,0), 하(0,1))
        hop_y : 수직 넉백(아래로 +, 위로 -). 지상 옆치기라도 살짝 튕기는 느낌을 줄 수 있음(원하면 0으로).
        push_out: 겹침 해소를 위해 즉시 위치를 뽑아내기
        """
        if dir_vec.length_squared() == 0:
            return

        d = dir_vec.normalize()
        # 진행 방향의 반대로 '밀려남' = d 방향 속도 부여
        # 수평
        if abs(d.x) > 0.1:
            # last_movement는 방향키 유지처럼 쓰이므로, x의 부호에 맞춰 설정
            if d.x > 0:
                self.last_movement = [0, 1, 0, 0]   # 오른쪽으로 밀려남
            else:
                self.last_movement = [1, 0, 0, 0]   # 왼쪽으로 밀려남
            self.velocity[0] = max(2.5, self.velocity[0])  # 넉백 세기

            if push_out:
                if d.x > 0:  # 오른쪽으로 빼내기
                    self.pos[0] = enemy_rect.right + 1
                else:         # 왼쪽으로 빼내기
                    self.pos[0] = enemy_rect.left - self.size[0] - 1

        # 수직
        if abs(d.y) > 0.1:
            # 아래로 밀어내는 경우(+): 땅에 붙어 있어도 확실히 밀려남
            self.velocity[1] = max(self.velocity[1], 3.5) if d.y > 0 else min(self.velocity[1], -3.5)
            if push_out:
                if d.y > 0:  # 아래로 빼내기(적의 아랫면과 충돌했을 때)
                    self.pos[1] = enemy_rect.bottom + 1
                else:        # 위로 빼내기(필요시)
                    self.pos[1] = enemy_rect.top - self.size[1] - 1

        # 살짝 점프 느낌(옵션)
        if hop_y != 0.0:
            self.velocity[1] = hop_y

        # 한두 프레임 공중 판정으로 만들어 넉백이 확실히 먹도록
        self.is_fly = True
        # 연속 판정 방지
        self.hurt_cooldown = 15  # 0.25초(60fps 기준)

        if getattr(self, 'factor', 0) <= 0:
            self.factor = 1

        self.knockback_immunity = 180

    def enemy_collision_side(self, enemy):
        """좌/우 측면 충돌: 진행 반대로 수평 넉백(지상에서도 강제)."""
        if self.knockback_immunity > 0:
            return
        if self.hurt_cooldown:
            return
        if self.is_attacking:
            return
        v = Vector2(self.frame_move.x, self.frame_move.y)

        # '진행 방향'이 거의 없다면, 적의 위치 기준으로 반대쪽으로 밀기
        if v.length() < 0.1:
            dir_x = -1 if enemy.rect().centerx > self.rect().centerx else 1
        else:
            # 진행 방향의 '반대'로 밀려남 => v의 반대 방향이지만, 좌/우 충돌이므로 수평 성분만 사용
            dir_x = -1 if v.x > 0 else (1 if v.x < 0 else (-1 if enemy.rect().centerx > self.rect().centerx else 1))

        self._apply_knockback(Vector2(dir_x, 0), enemy.rect(), hop_y=-1.2)  # 살짝 위로 톡 튀는 느낌

    def enemy_collision_below(self, enemy):
        """아래(플레이어가 적의 아랫면에 부딪힘): 진행 반대로 + 수직으로 아래로 밀어내기."""
        if self.knockback_immunity > 0:
            return
        if self.hurt_cooldown:
            return
        v = Vector2(self.frame_move.x, self.frame_move.y)

        # 기본은 '아래로' 밀치기(충돌면 법선의 반대 = 진행 반대가 보통 위쪽이므로)
        knock_dir = Vector2(0, 1)

        # 수평 성분도 '진행 반대'로 섞어주면 더 자연스러움(선택)
        if abs(v.x) > 0.05:
            knock_dir.x = -1 if v.x > 0 else 1

        self._apply_knockback(knock_dir, enemy.rect(), hop_y=0.0)

    def render(self, surf, offset=(0, 0)):
        if not self.is_attacking:
            super().render(surf, offset=offset)