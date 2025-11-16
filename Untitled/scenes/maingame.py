import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera
from scripts.entities import Player
from scripts.hud import Player_hud
from scripts.map import Map

class Maingame(Scene):
    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.camera = Camera(game)
        # self.player = Player(game, 'player', (60, 90), (self.game.screen.get_width() // 2, self.game.display.get_height() // 2))
        # self.player = Player(game, 'player', (60, 90), (100, self.game.display.get_height() // 2))
        self.player = Player(game, 'player', (60, 90), (0, 0))
        self.map = Map(game, self.player)
        self.map.generate_object()

        # for obj in self.map.obj_list:
        #     print(obj.type)

        self.p_hud = Player_hud(game)

        self.option_idx = 1 # 0 = 왼쪽, 1 = 정면, 2 = 오른쪽
        self.camera.set_target(self.player)

    def handle_events(self, events):
        # 입력 감지
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not self.player.state["moving"]:
                if event.key == pygame.K_LEFT and len(self.map.obj_list) > 1:
                    if self.map.curr_player_idx == 0:
                        self.option_idx = max(1, self.option_idx - 1)
                    else:
                        self.option_idx = max(0, self.option_idx - 1)

                    # if self.map.player_idx == 0 and len(self.map.obj_list) == 1:
                    #     pass
                    # elif self.map.player_idx == 0:
                    #     self.option_idx = self.option_idx - 1 if self.option_idx > 1 else 2
                    # elif self.map.player_idx == len(self.map.obj_list) - 1:
                    #     self.option_idx = self.option_idx - 1 if self.option_idx > 0 else 1
                    # else:
                    #     self.option_idx = self.option_idx - 1 if self.option_idx > 0 else 2

                if event.key == pygame.K_RIGHT and len(self.map.obj_list) > 1:
                    if self.map.curr_player_idx == len(self.map.obj_list) - 1:
                        # self.option_idx = 0
                        self.option_idx = min(1, self.option_idx + 1)
                    else:
                        self.option_idx = min(2, self.option_idx + 1)
                    # if self.map.player_idx == 0 and len(self.map.obj_list) == 1:
                    #     pass
                    # elif self.map.player_idx == 0:
                    #     self.option_idx = self.option_idx + 1 if self.option_idx < 2 else 1
                    # elif self.map.player_idx == len(self.map.obj_list) - 1:
                    #     self.option_idx = self.option_idx + 1 if self.option_idx < 1 else 0
                    # else:
                    #     self.option_idx = self.option_idx + 1 if self.option_idx < 2 else 0

                

                if event.key == pygame.K_SPACE:
                   self.judge_movement()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(self.map.player_idx)

    def update(self, dt):
        self.p_hud.update(self.option_idx)
        self.player.update(dt)

        # 충돌 감지
        for obj in self.map.obj_list.copy():            
            if self.player.handle_collision(obj):
                self.game.sm.go_to("interact", obj)

        self.camera.follow()

    def render(self, surf, offset=(0, 0)):
        bg_width = self.game.assets['background'].get_width()
        wrapping_x = -self.camera.offset[0] % bg_width
        y_pos = -self.camera.offset[1]

        surf.blit(self.game.assets['background'], (wrapping_x - bg_width, y_pos))
        surf.blit(self.game.assets['background'], (wrapping_x, y_pos))

        self.map.render(surf, self.camera.offset)
        self.player.render(surf, self.camera.offset)

        # 왼쪽, 오른쪽 선택
        if not self.player.state["moving"]:
            self.p_hud.render(surf)

    def judge_movement(self):
        if self.option_idx == 1:
            return
        
        self.player.state["moving"] = True
        self.player.state["collision"] = False

        self.player.defying_collision = self.player.DEFYING_TIME

        if self.option_idx == 0:
            self.player.state["left"] = True
            self.map.curr_player_idx = max(0, self.map.curr_player_idx - 1)
        
            if self.map.obj_list[self.map.curr_player_idx].type == 'player':
                self.map.curr_player_idx -= 1

        if self.option_idx == 2:
            self.player.state["right"] = True
            self.map.curr_player_idx = min(len(self.map.obj_list), self.map.curr_player_idx + 1)

            if self.map.obj_list[self.map.curr_player_idx].type == 'player':
                self.map.curr_player_idx += 1

        self.option_idx = 1