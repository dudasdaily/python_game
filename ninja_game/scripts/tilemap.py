import pygame

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
# NEIGHBOR_OFFSET = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {} # tile_map['3;10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3, 10)}
        self.off_grid_tiles = [] # 타일처럼 16x16 픽셀이 정해지지 않은 정렬되지 않은 오브젝트, 픽셀좌표

        for i in range(10):
            self.tile_map[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3+i, 10)}
            self.tile_map['10;' + str(5+i)] = {'type' : 'stone', 'variant' : 1, 'pos' : (10, 5+i)}

    # pos 주변의 타일들을 반환한다!
    def tiles_around(self, pos):
        tiles = [] # 현재 플레이어의 타일좌표에서 offset만큼 떨어진 거리에 있는 타일

        # 픽셀 좌표인 pos를 타일좌표로 바꿈!
        # 좌표값으로 음수가 들어오면 '/' 과 '//' 연산에 차이가 생김
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])

            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        
        return tiles

    #
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rects

    def render(self, surf, offset = (0,0)):
        # off_grid_tiles 렌더링
        for tile in self.off_grid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        # tile_map 렌더링
        # loc : "10;10" 같은 tile_map의 키
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            # self.game.assets => utils.load_images로 로딩한 이미지들의 리스트임
            # ex) game.assests['grass'] => [0.png, 1.png, ...]
            # tile_map['variant']가 마치 이 이미지 리스트의 인덱스 역할을 함!
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))