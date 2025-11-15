class Hud:
    def __init__(self):
        pass

class Player_hud:
    def __init__(self, game):
        self.game = game
        self.state = [0, 0, 0]
        self.action = ''
        self.set_action('idle')

    def update(self, option_idx):
        self.state = [0, 0, 0]
        self.state[option_idx] = 1

    def render(self, surf):
        if self.state == [0, 1, 0]:
            surf.blit(self.animation.img(), (0, 0))
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f'arrow/{self.action}'].copy()

class Battle_options:
    def __init__(self):
        pass