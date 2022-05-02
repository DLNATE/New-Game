import pygame as pg
import sys 

def main():
    pg.init()
    all_sprites = pg.sprite.LayeredUpdates()
    walls = pg.sprite.LayeredUpdates()
    floor = pg.sprite.LayeredUpdates()
    tileMap = [
        'W..................W',
        'W..................W',
        'W.........P........W',
        'W..................W',
        'W..................W',
        'WFFFFFFFFFFFFFFFFFFW',
        'W..................W',
        'W..................W',
        'W..................W',
        'W..................W',
        'W..................W',
        'W..................W',
    ]
    health = 100
    hunger = 100
    stress = 0
    temp = 0
    energy = 100
    fps = pg.time.Clock()
    screen = pg.display.set_mode((1280, 720))
    BROWN = (255, 217, 179)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    TILESIZE = 64
    GRAVITY = 1
    class createTile(pg.sprite.Sprite):
        def __init__(self,  x, y, group, tileWidth, tileLength, color):
            self.color = color
            self.x = x*TILESIZE
            self.y = y*TILESIZE
            self.groups = group, all_sprites
            if group == None:
                self.groups = all_sprites
            self._layer = 1
            self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(self.color)
            self.image = pg.transform.scale(self.image, (tileWidth, tileLength))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            super().__init__(self.groups)

    class Player(createTile):
        def __init__(self, x, y, group, tileWidth, tileLength, color):
            self.speed_x, self.speed_y = 0, 0
            self.jumped = False
            super().__init__(x, y, group, tileWidth, tileLength, color)
        def move(self):
            if self.speed_x >5:
                self.speed_x = 5
            self.rect.x += self.speed_x
            spritesTouched = pg.sprite.spritecollide(self, walls, False)
            if self.speed_x > 0 :
                for sprite in spritesTouched:
                    self.rect.right = min(self.rect.right, sprite.rect.left)
            if self.speed_x < 0 :
                for sprite in spritesTouched:
                    self.rect.left = max(self.rect.left, sprite.rect.right)
            self.speed_y += GRAVITY
            self.rect.y += self.speed_y
            spritesTouched = pg.sprite.spritecollide(self, floor, False)
            if self.speed_y > 0:
                for sprite in spritesTouched:
                    self.speed_y -= GRAVITY
                    self.rect.bottom = min(self.rect.bottom, sprite.rect.top)
                    self.jumped = False
                    self.speed_y = 0
            elif self.speed_y < 0:
                for sprite in spritesTouched:
                    self.rect.top = max(self.rect.top, sprite.rect.bottom)
    for i, row in enumerate(tileMap):
        for b, c in enumerate(row):
            if c == 'W':
                createTile(b, i, walls, 64, 64, BROWN)
            elif c == 'F':
                createTile(b, i, floor, 64, 64, BLACK)
            elif c == 'P':
                player = Player(b, i, None, 40, 120, RED)
    while True:
        screen.fill((0, 255, 255))
        player.move()
        player.speed_x = 0
        for i in all_sprites:
            screen.blit(i.image, (i.rect.x, i.rect.y))
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    sys.exit()
        pressed = pg.key.get_pressed()
        if pressed[pg.K_d] and pressed[pg.K_a] == False:
            player.speed_x += 3
        if pressed[pg.K_a] and pressed[pg.K_d] == False:
            player.speed_x -= 3 
        if pressed[pg.K_SPACE] and player.jumped == False:
            player.jumped = True
            player.speed_y = -20
        pg.display.update()
        fps.tick(60)
if __name__ == '__main__':
    main()