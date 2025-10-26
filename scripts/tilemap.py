class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {} # 딕셔너리로 한 이유 : 더미 타일을 저장하지 않아도 되서 저장공간 이득!, 타일좌표
        self.off_grid_tiles = [] # 타일처럼 16x16 픽셀이 정해지지 않은 정렬되지 않은 오브젝트, 픽셀좌표

        for i in range(10):
            self.tile_map[str(3 + i) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (3+i, 10)}
            self.tile_map['10;' + str(5+i)] = {'type' : 'stone', 'variant' : 1, 'pos' : (10, 5+i)}

    def render(self, surf):
        # off_grid_tiles 렌더링
        for tile in self.off_grid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
        
        # tile_map 렌더링
        # loc : "10;10" 같은 tile_map의 키!
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            # self.game.assets => utils.load_images로 로딩한 이미지들의 리스트임
            # ex) game.assests['grass'] => [0.png, 1.png, ...]
            # tile_map['variant']가 마치 이 이미지 리스트의 인덱스 역할을 함!
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

        