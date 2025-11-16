from pydoc import text
from unittest import TextTestResult
import pygame

class Hud:
    def __init__(self, game, text=None):
        self.game = game
        self.font = pygame.font.Font('data/fonts/NeoDunggeunmoPro-Regular.ttf', 12)
        self.lines = text.split('\n')
        self.y_offset = 10
        self.line_spacing = 20

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
        self.player_idx = self.game.sm.scenes["maingame"].map.player_idx
        self.obj_len = len(self.game.sm.scenes["maingame"].map.obj_list)

        self.state = [0, 0, 0]
        self.state[option_idx] = 1

    def render(self, surf):
        if self.player_idx == 0 and self.obj_len == 1:
            pass
        elif self.player_idx == 0:
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

class InteractMenu(Hud):
    TXTBOX_COLOR = (255, 255, 255, 200)
    SELECT_COLOR = (0, 0, 0)
    UNSELECT_COLOR = (169, 169, 169)

    def __init__(self, game, text=None):
        super().__init__(game, text)

        # 텍스트 박스 설정
        self.x_pos = 10
        self.y_pos = self.game.display.get_height() - 60
        self.text_box = pygame.Surface((self.game.display.get_width() - 2 * self.x_pos, 50), pygame.SRCALPHA)

        # 폰트 설정
        
    def update(self):
        pass

    def render(self, surf):
        pygame.draw.rect(self.text_box, self.TXTBOX_COLOR, pygame.Rect(0, 0, self.text_box.get_width(), self.text_box.get_height()))
        for line in self.lines:
            self.text_box.blit(self.font.render(line, False, self.SELECT_COLOR), (50, self.y_offset))
            self.y_offset += self.line_spacing


        # display에 텍스트 박스를 렌더링
        surf.blit(self.text_box, (self.x_pos, self.y_pos))

class Box:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('data/fonts/NeoDunggeunmoPro-Regular.ttf', 14)

        # 텍스트 박스 설정
        self.box_x = 10
        self.box_y = self.game.display.get_height() - 50
        self.box = pygame.Surface((self.game.display.get_width() - 2 * self.box_x, 50), pygame.SRCALPHA)

    def render(self, surf):
        pygame.draw.rect(self.box, (255, 255, 255, 210), (0, 0, self.box.get_width(), self.box.get_height()))
        pygame.draw.rect(self.box, (0, 0, 0), (0, 0, self.box.get_width(), self.box.get_height()), 2) # 텍스트 박스 외곽선

class TextBox(Box):
    def __init__(self, game, texts):
        super().__init__(game)
        self.texts = texts
        self.y_offset = 10
        self.line_spacing = 15

    def update(self):
        pass

    def render(self, surf):
        super().render(surf)

        y_offset = self.y_offset

        for text in self.texts:
            # self.box.blit(self.font.render(text, False, (0, 0, 0)), (30, y_offset))
            self.box.blit(self.font.render(text, False, (0, 0, 0)), (30, y_offset))
            y_offset += self.line_spacing

        surf.blit(self.box, (self.box_x, self.box_y))
        
        
    
class InteractBox(Box):
    def __init__(self, game, interact_text):
        super().__init__(game)
        self.interact_text = interact_text
        self.selected_idx = 0

    def update(self):
        pass

    def render(self, surf):
        super().render(surf)
        # 여기에 코딩
        surf.blit(self.box, (self.box_x, self.box_y))
        pass


class Battle_options:
    def __init__(self):
        pass