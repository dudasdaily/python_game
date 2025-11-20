import random
import pygame
from scripts.entities import Boss, Enemy, Chest, Hp_Potion, Ap_Potion

GRID_SIZE = 400 # 오브젝트 사이의 거리
OBJ_APPEND_MIN = 3
OBJ_APPEND_MAX = 5

class Map:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.player_idx = 0
        self.curr_player_idx = 0
        self.num_of_object = None
        # self.obj_list = [self.player, Hp_Potion(self.game, 'hp_potion', (60, 90), (0, 0)), Ap_Potion(self.game, 'ap_potion', (60, 90), (0, 0)), Boss(self.game, 'boss', (90, 120), (0, 0))]
        self.obj_list = [self.player, Enemy(self.game, 'enemy', (60, 90), (0, 0)), Ap_Potion(self.game, 'ap_potion', (60, 90), (0, 0))]

    def generate_object(self):
        self.num_of_object = random.randint(OBJ_APPEND_MIN, OBJ_APPEND_MAX)

        for i in range(self.num_of_object):
            r = random.random()

            if r <= 0.5:
                self.obj_list.append(Enemy(self.game, 'enemy', (60, 90), (0, 0)))
            elif 0.5 < r <= 0.7:
                self.obj_list.append(Hp_Potion(self.game, 'hp_potion', (60, 90), (0, 0)))
            elif 0.7 < r <= 0.9:
                self.obj_list.append(Ap_Potion(self.game, 'ap_potion', (60, 90), (0, 0)))
            else:
                self.obj_list.append(Chest(self.game, 'chest', (60, 90), (0, 0)))

        self.num_of_object = len(self.obj_list)

        random.shuffle(self.obj_list)

        if self.obj_list[0] is self.player:
            swap_idx = random.randint(1, self.num_of_object - 2)
            self.obj_list[0], self.obj_list[swap_idx] = self.obj_list[swap_idx], self.obj_list[0]

        elif self.obj_list[-1] is self.player:
            swap_idx = random.randint(1, self.num_of_object - 2)
            self.obj_list[-1], self.obj_list[swap_idx] = self.obj_list[swap_idx], self.obj_list[-1]

        # 오브젝트를 맵에 배치
        for i, obj in enumerate(self.obj_list):
            x_pos = GRID_SIZE * (i+1) - obj.size[0] // 2
            y_pos = self.game.display.get_height() // 2

            obj.pos = [x_pos, y_pos]

            if obj == self.player:
                self.player_idx = i
                self.curr_player_idx = i

    def update(self):
        for i, obj in enumerate(self.obj_list):
            if obj == self.player:
                self.player_idx = i