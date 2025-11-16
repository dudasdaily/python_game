import pygame
import sys

from scripts.hud import InteractMenu
from scenes.scene import Scene

class Interact(Scene):
    TXTBOX_COLOR = (255, 255, 255, 200)
    SELECT_COLOR = (0, 0, 0)
    UNSELECT_COLOR = (169, 169, 169)

    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.collided_obj = None
        self.lines = []

        if self.collided_obj != None:
            self.lines = self.collided_obj.interact_text.split('\n')

        # 텍스트 박스 설정
        self.x_pos = 10
        self.y_pos = self.game.display.get_height() - 60
        self.text_box = pygame.Surface((self.game.display.get_width() - 2 * self.x_pos, 50), pygame.SRCALPHA)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.KEYUP:
                pass

    def update(self, dt):
        self.game.sm.scenes['maingame'].update(dt)

    def render(self, surf):
        # 베이스 씬 렌더링
        self.game.sm.scenes["maingame"].render(surf)

        # 텍스트 박스 렌더링
        pygame.draw.rect(self.text_box, self.TXTBOX_COLOR, pygame.Rect(0, 0, self.text_box.get_width(), self.text_box.get_height()))
        for line in self.lines:
            self.text_box.blit(self.font.render(line, False, self.SELECT_COLOR), (50, self.y_offset))
            self.y_offset += self.line_spacing

        # display에 텍스트 박스를 렌더링
        surf.blit(self.text_box, (self.x_pos, self.y_pos))