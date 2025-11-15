import pygame

class Entity:
    def __init__(self, game, e_type, size, pos=(0, 0)):
        self.game = game

        self.pos = list(pos)
        self.type = e_type
        self.size = size
        self.action = ''

        self.movement = [0, 0]
        self.velocity = [0, 0]
    
    def update(self, dt):
        pass

    def render(self, surf):
        pass

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f'{self.type}/{self.action}'].copy()

class Player(Entity):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.max_hp = 5
        self.hp = self.max_hp

        self.max_ap = 5
        self.ap = self.max_ap
        
        self.velocity = [100, 2]
        self.anim_offset = (0, 0)

        self.set_action('idle')

        self.state = {
            "left" : False,
            "right" : False,
            "moving" : False,
        }
        
        self.flip = False
    
    def update(self, dt):
        if not self.state["moving"]:
            self.state["left"] = False
            self.state["right"] = False

        self.movement[0] = self.state["right"] - self.state["left"]
        self.pos[0] += self.movement[0] * self.velocity[0] * dt

        self.animation.update()

        if self.state["left"]:
            self.flip = True
            self.set_action('run')
        elif self.state["right"]:
            self.flip = False
            self.set_action("run")
        else:
            self.set_action("idle")

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] - self.anim_offset[0], self.pos[1] - offset[1] - self.anim_offset[1]))

    def handle_collision(self):
        # 오브젝트와 충돌을 한다면
        # self.state["moving"] = False
        pass

class Enemy(Entity):
    def __init__(self, game, e_type, size, pos):
        pass

class Chest:
    def __init__(self, game):
        pass

class Potion:
    def __init__(self, game):
        pass

class Hp_Potion(Potion):
    def __init__(self, game):
        super().__init__(game)

class Ap_Potion(Potion):
    def __init__(self, game):
        super().__init__(game)