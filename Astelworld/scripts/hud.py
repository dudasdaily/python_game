import string
import pygame

FONT_PATH = 'data/jump/font/NeoDunggeunmoPro-Regular.ttf'

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
        self.timer = pygame.font.Font(FONT_PATH, 14)
        self.score_surf = None
        self.elapsed_time = None

    def update(self):
        self.elapsed_time = self.get_time()
        self.score_surf = self.timer.render(self.elapsed_time, False, (255, 255, 255))

    def render(self, surf):
        surf.blit(self.score_surf, (surf.get_width() - 80, 5))

    def get_time(self) -> string:
        current_time = pygame.time.get_ticks() - self.game.paused_time
        
        hour = current_time // 3600000
        current_time %= 3600000

        min = current_time // 60000
        current_time %= 60000

        sec = current_time // 1000
        current_time %= 1000

        return f"{hour:02d}:{min:02d}:{sec:02d}.{current_time // 10:02d}"