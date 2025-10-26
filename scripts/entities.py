import pygame

class PhysicsEntitiy:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # convert iterable to list
        self.size = size
        self.velocity = [1, 0] # 위치를 시간에 대해 미분

    # (-1, 0)
    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] * self.velocity[0], movement[1] * self.velocity[1]) # 이 프레임에서 개체가 얼마나 움직여야 하는가

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)