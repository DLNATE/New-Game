import pygame as pg
class createTile():
    def __init__(self, sheet, x, y, group, tile_map):
        self.tileMap = tile_map
        self.x = x*tile_size
        self.y = y*tile_size
        self.groups = all_sprites, group
        super().__init__(self.groups)
        self.image = pg.Surface((tileWidth, tileLength))
        # self.image.blit(sheet, (0, 0), (40, 120, 14, 14))
        self.image = pg.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
