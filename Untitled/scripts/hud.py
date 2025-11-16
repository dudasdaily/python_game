import pygame

class Hud:
    def __init__(self, text=None):
        self.font = None
        self.lines = text.split('\n')
        self.y_offset = 30
        self.line_spacing = 30

    def render(self, surf):
        for line in self.lines:
            text_surface = self.font.render(line, False, (255, 255, 255))
            surf.blit(text_surface, (50, self.y_offset))
            self.y_offset += self.line_spacing

class Player_hud:
    def __init__(self, game):
        self.game = game
        self.state = [0, 0, 0]
        self.action = ''

    def update(self, option_idx):
        self.player_idx = self.game.sm.current_scene.map.player_idx
        self.obj_len = len(self.game.sm.current_scene.map.obj_list)

        self.state = [0, 0, 0]
        self.state[option_idx] = 1

    def render(self, surf):
        if self.player_idx == 0:
            surf.blit(self.game.assets['arrow/right'].copy(), (0, 0))
        elif self.player_idx == self.obj_len - 1:
            surf.blit(self.game.assets['arrow/left'].copy(), (0, 0))
        else:
            surf.blit(self.game.assets['arrow/left'].copy(), (0, 0))
            surf.blit(self.game.assets['arrow/right'].copy(), (0, 0))

        if self.state == [1, 0, 0]:
            surf.blit(self.game.assets['arrow/left_select'].copy(), (0, 0))
        elif self.state == [0, 0, 1]:
            surf.blit(self.game.assets['arrow/right_select'].copy(), (0, 0))

class Interact(Hud):
    SELECT_COLOR = (0, 0, 0)
    UNSELECT_COLOR = (169, 169, 169)

    def __init__(self, game):
        self.game = game
        
        x_pos = 10
        # y_pos = self.game.display.get_height() - 
        self.text_box = pygame.Rect()
        
    def update(self):
        pass

    def render(self, surf):
        pass

class Battle_options:
    def __init__(self):
        pass