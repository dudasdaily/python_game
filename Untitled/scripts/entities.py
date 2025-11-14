class Entity:
    def __init__(self, game):
        self.game = game

        # self.pos = [50, 120]
        self.pos = [self.game.screen.get_width() // 2, 100]

        self.movement = [0, 0]
        self.velocity = [0, 0]
    
    def update(self, dt):
        pass

    def render(self, surf):
        pass

class Player(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.velocity = [100, 2]

        self.state = {
            "left" : False,
            "right" : False,
            "space" : False,
        }

        self.flip = False
    
    def update(self, dt):
        self.movement[0] = self.state["right"] - self.state["left"]
        self.pos[0] += self.movement[0] * self.velocity[0] * dt

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player/idle'].img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def handle_collision(self):
        pass