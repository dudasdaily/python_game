import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])) : 0, # (1,0), (0,1) 이 연결된 경우 variant = 0
    tuple(sorted([(1, 0), (0, 1) , (-1, 0)])) : 1,
    tuple(sorted([(-1, 0), (0, 1)])) : 2,
    tuple(sorted([(-1, 0), (0, -1) , (0, 1)])) : 3,
    tuple(sorted([(-1, 0), (0, -1)])) : 4,
    tuple(sorted([(-1, 0), (0, -1) , (1, 0)])) : 5,
    tuple(sorted([(1, 0), (0, -1) ])) : 6,
    tuple(sorted([(1, 0), (0, -1) , (0, 1)])) : 7,
    tuple(sorted([(1, 0), (-1, 0) , (0, 1), (0, -1)])) : 8,
}
AUTOTILE_TYPES = {'grass', 'stone'}

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {} # tile_map = {'grass' : {}, ... } ,tile_map['grass'] = { 'type' : 'grass', 'variant' : 0, 'pos' : (xpos, ypos)}
        self.off_grid_tiles = []
        self.portals = []

    # def tiles_around(self, pos):
    #     tiles = []
    #     tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

    #     for offset in NEIGHBOR_OFFSET:
    #         check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])

    #         if check_loc in self.tile_map:
    #             tiles.append(self.tile_map[check_loc])
        
    #     return tiles
    
    # 충돌 감지 로직 변경! pos(플레이어의 왼쪽 위 좌표)의 주변타일 -> rect(히트박스)의 주변타일
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
    
    def autotile(self):
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            neighbors = set()

            for shift in [(1,0), (-1,0), (0, -1), (0, 1)]:
                check_loc = f"{tile['pos'][0] + shift[0]};{tile['pos'][1] + shift[1]}"
                if check_loc in self.tile_map:
                    if self.tile_map[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)

            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap' : self.tile_map, 'tile_size' : self.tile_size, 'offgrid' : self.off_grid_tiles, 'portals' : self.portals}, f)
        f.close()

    def load(self, path, cleared_maps=set()):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close

        self.tile_map = {}
        if 'tilemap' in map_data:
            for loc, tile in map_data['tilemap'].items():
                if tile.get('clear_required') not in cleared_maps:
                    self.tile_map[loc] = tile

        self.tile_size = map_data.get('tile_size', self.tile_size)
        self.off_grid_tiles = map_data.get('offgrid', [])
        self.portals = map_data.get('portals', [])


    def solid_check(self, pos):
        tile_loc = f"{int(pos[0]//self.tile_size)};{int(pos[1]//self.tile_size)}"
        if tile_loc in self.tile_map:
            if self.tile_map[tile_loc]['type'] in PHYSICS_TILES:
                return self.tile_map[tile_loc]

    # id_pair : (type, variant)
    # id_pairs : [id_pair, ...]
    def extract(self, id_pairs, keep=False):
        # [(타일타입1, variant1), (타일타입2, variant2)] 이 타일들의 정보들을 담은 리스트를 준다!
        matches = []
    
        for tile in self.off_grid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.off_grid_tiles.remove(tile)

        for loc in self.tile_map:
            tile = self.tile_map[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                # 타일 좌표 -> 픽셀좌표
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size

                if not keep:
                    del self.tile_map[loc]
        return matches
        

    def render(self, surf, offset=(0, 0)):
        # x : top-left 타일의 x좌표 ~ 타일의 오른쪽 끝
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        for tile in self.off_grid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))