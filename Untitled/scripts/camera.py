import pygame

class Camera:
    def __init__(self, game):
        self.game = game

        self.screen_width = self.game.screen.get_width() # 640, 240
        self.screen_height = self.game.screen.get_height() # 320, 240
        self.display_width = self.game.display.get_width()
        self.display_height = self.game.display.get_height()

        self.target = None
        self.offset = [0, 0]

    def set_target(self, target):
        self.target = target

    def follow(self):
        x = self.target.pos[0] - self.display_width // 2
        y = self.target.pos[1] - self.display_height // 2

        x = max(0, min(x, self.screen_width - self.display_width))
        y = max(0, min(y, self.screen_height - self.display_height))

        self.offset = [x, y]