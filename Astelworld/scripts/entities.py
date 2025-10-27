import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type # 엔티티 타입 : 'player'
        self.pos = list(pos)
        self.size = size
        self.velocity = [1, 1]
        self.collisions = { 'up' : False, 'down' : False, 'right' : False, 'left' : False } # 충돌이 일어났는가?

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement=(0,0,0,0)):
        self.collisions = { 'up' : False, 'down' : False, 'right' : False, 'left' : False }
        x = (movement[0] * self.velocity[0] + movement[1] * self.velocity[0])
        y = (movement[2] * self.velocity[1] + movement[3] * self.velocity[1])

        frame_movement = (x, y)

        # x축 충돌 감지
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.pos):
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
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0: # 위로 가다가 충돌
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                if frame_movement[1] > 0: # 아래로 가다가 충돌
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True

                self.pos[1] = entity_rect.y

    def render(self, surf, offset = (0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))