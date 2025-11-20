import pygame

class Object:
    def __init__(self, game, e_type, size, pos):
        self.game = game
        self.type = e_type
        self.size = size
        self.pos = list(pos)
        self.texts = '' # 스페이스 바 누르면 바로 넘어가는 텍스트 박스의 내용
        self.interact_text = '' # 1. 2. 3. 등 유저가 선택할 수 있는 상호작용 박스의 내용

        self.kill = False

    def update(self, dt):
        pass

    def render(self, surf, offset=(0,0)):
        pass

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

class Entity(Object):
    def __init__(self, game, e_type, size, pos=(0, 0)):
        super().__init__(game, e_type, size, pos)
        self.action = ''

        self.movement = [0, 0]
        self.velocity = [0, 0]
    
    def update(self, dt):
        pass

    def render(self, surf, offset=(0, 0)):
        pass

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f'{self.type}/{self.action}'].copy()

class Player(Entity):
    DEFYING_TIME = 50

    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.max_hp = 5
        self.hp = self.max_hp

        self.max_ap = 5
        self.ap = self.max_ap
        
        self.velocity = [150, 2]
        self.anim_offset = (0, 0)
        self.defying_collision = self.DEFYING_TIME

        self.set_action('idle')

        self.state = {
            "left" : False,
            "right" : False,
            "moving" : False,
            "collision" : True,
        }
        
        self.flip = False
    
    def update(self, dt):
        if not self.state["moving"]:
            self.state["left"] = False
            self.state["right"] = False

        self.movement[0] = self.state["right"] - self.state["left"]
        self.pos[0] += self.movement[0] * self.velocity[0] * dt

        self.animation.update()

        if self.defying_collision:
            self.defying_collision = max(0, self.defying_collision - 1)

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

class Enemy(Entity):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.max_hp = 5
        self.hp = self.max_hp
        
        self.texts = ['적을 만났다!', '버거워 보인다...']
        self.interact_text = '1. 싸운다\n2. 도망간다\n3. 테스트'

class Boss(Entity):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.texts = ['보스를 만났다!']
        self.interact_text = '1. 싸운다\n2. 도망간다'

class Chest(Object):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)

class Hp_Potion(Object):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.animation = self.game.assets['hp'].copy()
        self.texts = ['HP 포션이다!']
        self.interact_text = 'HP가 2만큼 회복되었다!'

    def update(self, dt):
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Ap_Potion(Object):
    def __init__(self, game, e_type, size, pos):
        super().__init__(game, e_type, size, pos)
        self.animation = self.game.assets['ap'].copy()
        self.texts = ['AP 포션이다!']
        self.interact_text = 'AP가 2만큼 회복되었다!'


    def update(self, dt):
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))