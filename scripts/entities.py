import pygame

class PhysicsEntitiy:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # convert iterable to list
        self.size = size
        self.velocity = [0, 0] # 위치를 시간에 대해 미분

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) # 이 프레임에서 개체가 얼마나 움직여야 하는가

        # x축 충돌 감지
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # 엔티티가 오른쪽으로 가다가 충돌
                    entity_rect.right = rect.left
                
                if frame_movement[0] < 0: # 엔티티가 왼쪽으로 가다가 충돌
                    entity_rect.left = rect.right

                self.pos[0] = entity_rect.x

        #y축 충돌 감지
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect() # 충돌 감지를 위한 엔티티의 히트박스
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0: # 위로 가다가 충돌
                    entity_rect.top = rect.bottom
                if frame_movement[1] > 0: # 아래로 가다가 충돌
                    entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # 최대 속도를 5로 제한!

    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)