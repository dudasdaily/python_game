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
        self.velocity = [100, 2]
        self.anim_offset = (0, 0)

        self.set_action('idle')

        self.state = {
            "left" : False,
            "right" : False,
            "space" : False,
        }
        
        self.flip = False
    
    def update(self, dt):
        self.movement[0] = self.state["right"] - self.state["left"]
        self.pos[0] += self.movement[0] * self.velocity[0] * dt

        self.animation.update()

        self.flip = self.movement[0] < 0

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0] - self.anim_offset[0], self.pos[1] - offset[1] - self.anim_offset[1]))

    def handle_collision(self):
        pass