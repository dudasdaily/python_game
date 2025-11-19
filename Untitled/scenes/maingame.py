import pygame
import sys

from scenes.scene import Scene
from scripts.camera import Camera
from scripts.entities import Player
from scripts.hud import Player_hud, HpHud, ApHud
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

        self.Hp_bar = HpHud(game, self.player, (10, 10))
        self.Ap_bar = ApHud(game, self.player, (10, 35))

        print(self.map.obj_list)

        # for obj in self.map.obj_list:
        #     print(obj.type)

        self.p_hud = Player_hud(game, self.player)

        self.option_idx = 1 # 0 = 왼쪽, 1 = 정면, 2 = 오른쪽
        self.camera.set_target(self.player)

        self.can_go_left = False
        self.can_go_right = False

    def handle_events(self, events):
        # 입력 감지
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not self.player.state["moving"]:
                if event.key == pygame.K_LEFT:
                    self.option_idx = max(0, self.option_idx - 1)

                if event.key == pygame.K_RIGHT:
                    self.option_idx = min(2, self.option_idx + 1)

                if event.key == pygame.K_SPACE:
                    self.judge_movement()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(f'curr_idx : {self.map.curr_player_idx}, left : {self.can_go_left}, right : {self.can_go_right}')

    def update(self, dt):
        self.can_go_left = False
        self.can_go_right = False

        # 맵에서 플레이어를 기준으로 왼쪽으로 갈 수 있는지 체크
        for idx in range(self.map.curr_player_idx - 1, -1, -1):
            if self.map.obj_list[idx].type == 'player' or self.map.obj_list[idx].kill:
                continue
            self.can_go_left = True

        # 맵에서 플레이어를 기준으로 오른쪽으로 갈 수 있는지 체크
        for idx in range(self.map.curr_player_idx + 1, len(self.map.obj_list)):
            if self.map.obj_list[idx].type == 'player' or self.map.obj_list[idx].kill:
                continue
            self.can_go_right = True

        self.option_idx = self.p_hud.update(self.option_idx, self.can_go_left, self.can_go_right) # p_hud.state와 동기화!
        self.player.update(dt)

        # 충돌 감지
        for obj in self.map.obj_list:
            if self.player.handle_collision(obj, self.can_go_left, self.can_go_right):
                self.collided_obj = obj
            
            if obj.type != 'player':
                obj.update(dt)

        self.camera.follow()

    def render(self, surf, offset=(0, 0)):
        bg_width = self.game.assets['background'].get_width()
        wrapping_x = -self.camera.offset[0] % bg_width
        y_pos = -self.camera.offset[1]

        surf.blit(self.game.assets['background'], (wrapping_x - bg_width, y_pos))
        surf.blit(self.game.assets['background'], (wrapping_x, y_pos))
        
        for obj in self.map.obj_list:
            if obj.type != 'player' and not obj.kill: # kill 된 오브젝트는 렌더링 안함
                pygame.draw.rect(surf, (255, 0, 0), (obj.pos[0] - self.camera.offset[0], obj.pos[1] - self.camera.offset[1], obj.size[0], obj.size[1]), 1)
                obj.render(surf, self.camera.offset)

        self.player.render(surf, self.camera.offset)
        self.Hp_bar.render(surf)
        self.Ap_bar.render(surf)

        # 왼쪽, 오른쪽 선택
        if not self.player.state["moving"]:
            self.p_hud.render(surf, self.can_go_left, self.can_go_right, self.camera.offset)

    def judge_movement(self):
        print(self.option_idx, self.collided_obj)
        if self.option_idx == 1 and self.collided_obj:
            self.p_hud.interact_button_render = False
            self.manager.go_to("interact", self.collided_obj)
            return
        
        elif self.option_idx == 1:
            return

        # 이동 관련
        self.player.state["moving"] = True
        self.player.state["collision"] = False

        self.player.defying_collision = self.player.DEFYING_TIME

        if self.option_idx == 0:
            self.player.state["left"] = True
            self.map.curr_player_idx -= 1

            if self.map.obj_list[self.map.curr_player_idx].type == 'player':
                self.map.curr_player_idx -= 1


        if self.option_idx == 2:
            self.player.state["right"] = True
            self.map.curr_player_idx += 1

            if self.map.obj_list[self.map.curr_player_idx].type == 'player':
                self.map.curr_player_idx += 1

        self.player.ap = max(0, self.player.ap - 1)

        self.option_idx = 1