import pygame

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.off_grid_tiles = []

        for i in range(10):
            self.tile_map[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3+i, 10)}
            self.tile_map['10;' + str(5+i)] = {'type' : 'stone', 'variant' : 1, 'pos' : (10, 5+i)}

    # def tiles_around(self, pos):
    #     tiles = []

    #     tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        

    #     for offset in NEIGHBOR_OFFSET:
    #         check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])

    #         if check_loc in self.tile_map:
    #             tiles.append(self.tile_map[check_loc])
        
    #     return tiles
    
    def physics_rects_in_region(self, rect):
        """
            엔티티의 히트박스(Rect)를 입력으로 받아서
            이 히트박스 주변 타일들의 딕셔너리가 들어간 리스트를 리턴한다!
        """
        tiles = []
        tile = self.tile_size

        x0 = rect.left // tile - 1
        x1 = rect.right // tile + 1
        y0 = rect.top // tile - 1
        y1 = rect.bottom // tile + 1

        for tx in range(int(x0), int(x1) + 1):
            for ty in range(int(y0), int(y1) + 1):
                loc = f"{tx};{ty}"
                if loc in self.tile_map and self.tile_map[loc]['type'] in PHYSICS_TILES:
                    tiles.append(self.tile_map[loc])

        return tiles

    def physics_rects_around(self, rect):
        """
            플레이어의 주변 타일들 중,
            물리 작용을 하는 타일들의 히트박스 리스트를 리턴한다!
        """
        rects = []
        for tile in self.physics_rects_in_region(rect):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.off_grid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # x : top-left 타일의 x좌표 ~ 타일의 오른쪽 끝
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))