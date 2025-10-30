import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type # 엔티티 타입 : 'player'
        self.pos = list(pos)
        self.size = size
        self.velocity = [1.5, 1.5]
        self.external_force = [0, 0]
        self.collisions = { 'up' : False, 'down' : False, 'right' : False, 'left' : False } # 충돌이 일어났는가?

        self.action = ''
        self.anim_offset = (0, -5) # 이미지 패딩 처리
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

        # print(x, y)

        if (movement[0] != 0 and movement[1] != 0):
            x = 0

        frame_movement = (x, y)

        # x축 충돌 감지
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.rect()):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # 엔티티가 오른쪽으로 가다가 충돌
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # 엔티티가 왼쪽으로 가다가 충돌
                    entity_rect.left = rect.right
                    self.collisions['left'] = True

                self.pos[0] = entity_rect.x

        #y축 충돌 감지
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.rect()):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0: # 위로 가다가 충돌
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                if frame_movement[1] > 0: # 아래로 가다가 충돌
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                self.pos[1] = entity_rect.y


        self.velocity[0] = max(1.5, self.velocity[0] - 0.1)
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # if self.is_fly and self.collisions['down']:
        #     self.game.movement = [0, 0, 0, 0]
        #     self.is_fly = False

        self.animation.update()

    def render(self, surf, offset = (0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jump_cnt = 0
        self.is_charging = False

        self.direction = [0, 0, 0, 0]
        self.charge = 0

    def update(self, tilemap, movement=(0,0,0,0)):
        if self.is_fly and not self.is_charging and self.jump_cnt > 0:
            movement = self.direction.copy()

        if self.is_fly:
            self.air_time += 1

        super().update(tilemap, movement = movement)

        if self.collisions['left']:
            if self.is_fly:
                self.direction[0] = 0
                self.direction[1] = 1
                self.velocity[0] = 2
                self.velocity[1] = -2

        elif self.collisions['right']:
            if self.is_fly:
                self.direction[0] = 1
                self.direction[1] = 0
                self.velocity[0] = 2
                self.velocity[1] = -2

        if self.collisions['down']:
            if self.is_fly:
                self.jump_cnt = 0
                self.is_fly = False
                self.game.movement = [0, 0, 0, 0]
                self.air_time = 0

            self.velocity[1] = 1.5        

        if self.is_charging:
            self.set_action('charging')
        elif self.air_time >= 4:
            self.set_action('jump')
        elif self.game.movement[0] != 0:
            self.flip = True
            self.set_action('run')
        elif self.game.movement[1] != 0:
            self.flip = False
            self.set_action('run')
        else:
            self.set_action('idle')