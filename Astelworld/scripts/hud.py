import pygame

class Hp:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.hp_bar = [0, 0, 0]
        self.hp_img_width = self.game.assets['hp'][0].get_width()

    def update(self):
        for i in range(self.player.max_hp):
            if self.player.hp - (i + 1) >= 0:
                self.hp_bar[i] = self.game.assets['hp'][0]
            else:
                self.hp_bar[i] = self.game.assets['hp'][1]

    def render(self, surf, offset=(0, 0)):
        if self.game.level == '0':
            return
        
        for i, x in enumerate(range(10, 10 + self.hp_img_width * 3, self.hp_img_width)):
            surf.blit(self.hp_bar[i], (x, 10))
            
class Timer:
    def __init__(self, game):
        self.game = game
        self.timer = pygame.font.Font()
    def update(self):
        pass
    def render(self, surf):
        # surf.blit()
        pass