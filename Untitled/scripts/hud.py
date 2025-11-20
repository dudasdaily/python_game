import pygame

class Hud:
    def __init__(self, game, text=None):
        self.game = game
        self.font = pygame.font.Font('data/fonts/NeoDunggeunmoPro-Regular.ttf', 16)
        self.lines = text.split('\n')
        self.y_offset = 10
        self.line_spacing = 20

    def render(self, surf):
        for line in self.lines:
            text_surface = self.font.render(line, False, (255, 255, 255))
            surf.blit(text_surface, (50, self.y_offset))
            self.y_offset += self.line_spacing

class Player_hud:
    def __init__(self, game, player):
        self.game = game
        self.state = [0, 0, 0]
        self.action = ''
        self.player = player

        self.interact_button_render = True

    def update(self, option_idx, can_go_left, can_go_right):
        if option_idx == 0 and can_go_left:
            self.state = [1, 0, 0]

        elif option_idx == 2 and can_go_right:
            self.state = [0, 0, 1]

        else:
            self.state = [0, 1, 0]

        # # maingame.py의 option_idx와 동기화
        # for i, x in enumerate(self.state):
        #     if x:
        #         return i

    def render(self, surf, can_go_left, can_go_right, offset=(0, 0)):
        if can_go_left:
            surf.blit(self.game.assets['arrow/left'].copy(), (0, 0))

        if can_go_right:
            surf.blit(self.game.assets['arrow/right'].copy(), (0, 0))

        if self.state == [1, 0, 0]:
            surf.blit(self.game.assets['arrow/left_select'].copy(), (0, 0))

        if self.state == [0, 0, 1]:
            surf.blit(self.game.assets['arrow/right_select'].copy(), (0, 0))

        if self.state == [0, 1, 0] and self.game.sm.scenes['maingame'].collided_obj and self.interact_button_render:
            font = pygame.font.Font('data/fonts/NeoDunggeunmoPro-Regular.ttf', 16)
            render_font = font.render('Press Space to interact', False, (255, 255, 255), (0, 0, 0))
            surf.blit(render_font, (self.player.rect().centerx - render_font.get_width() // 2 - offset[0], self.player.rect().top - 30 - offset[1]))

class InteractMenu(Hud):
    TXTBOX_COLOR = (255, 255, 255, 200)

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

    def update(self, idx=None):
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
    SELECT_COLOR = (0, 0, 0)
    UNSELECT_COLOR = (169, 169, 169)

    def __init__(self, game, interact_text):
        super().__init__(game)
        self.x_offset = 30
        self.y_offset = 10

        self.x_spacing = 60
        self.y_spacing = 18

        self.interact_text = interact_text
        self.selected_idx = 0

    def update(self, interact_idx):
        self.selected_idx = interact_idx

    def render(self, surf):
        super().render(surf)

        y_offset = self.y_offset
        # 여기부터 코딩
        for i, text in enumerate(self.interact_text):
            FONT_COLOR = self.UNSELECT_COLOR if i != self.selected_idx else self.SELECT_COLOR
            self.box.blit(self.font.render(text, False, FONT_COLOR), (self.x_offset + (i % 2) * (self.x_spacing + len(text)*14), y_offset))

            if i % 2 == 1:
                y_offset += self.y_spacing
        # 여기까지
        surf.blit(self.box, (self.box_x, self.box_y))
        pass

class Battle_options:
    def __init__(self):
        pass

class HpHud:
    def __init__(self, game, player, pos=(0, 0)):
        self.game = game
        self.player = player
        self.animation = self.game.assets['hp'].copy()
        self.pos = pos

    def update(self):
        # self.animation.update()
        pass

    def render(self, surf):
        x_offset = 0
        for i in range(self.player.hp):
            scaled_img = pygame.transform.scale(self.animation.img(), (26, 26))
            surf.blit(scaled_img, (self.pos[0] + x_offset, self.pos[1]))
            x_offset += 22

class ApHud:
    def __init__(self, game, player, pos=(0, 0)):
        self.game = game
        self.player = player
        self.animation = self.game.assets['ap'].copy()
        self.pos = pos

    def render(self, surf):
        x_offset = 0
        for i in range(self.player.ap):
            scaled_img = pygame.transform.scale(self.animation.img(), (32, 32))
            surf.blit(scaled_img, (self.pos[0] + x_offset, self.pos[1]))
            x_offset += 16