import sys
import pygame
from scenes.scene import Scene
from scenes.battle import Battle

FONT_PATH = 'data/fonts/NeoDunggeunmoPro-Regular.ttf'

BLINK_TIME = 1

class Title(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.font_obj = pygame.font.Font(FONT_PATH, 24)
        self.font_obj.set_bold(True)
        self.elasped_time = 0
        self.is_render = True
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pass
                if event.key == pygame.K_SPACE:
                    self.manager.go_to("maingame")

    def update(self, dt):
        self.elasped_time += dt

    def render(self, surf):
        surf.fill((255, 255, 0))
        ft = self.font_obj.render('Press to Start', False, (0, 0, 0))

        if self.elasped_time > BLINK_TIME:
            self.is_render = not self.is_render
            self.elasped_time = 0

        if self.is_render:
            surf.blit(ft, (self.game.display.get_width() // 2 - ft.get_width() // 2, self.game.display.get_height() // 2 - ft.get_height() // 2))        