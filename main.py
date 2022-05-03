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
        'W..................W',
        'W..................W',
        'W...S..............W',
        'WFFFFFFFFFFFFFFFFFFW',
        'W..................W',
        'W..................W',
        'W..................W',
        'W........P.........W',
        'W..................W',
        'WFFFFFFFFFFFFFFFFFFW',
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
    PINK = (153, 0, 153)
    RED = (255, 0, 0)
    TILESIZE = 64
    GRAVITY = 1
    class createTile(pg.sprite.Sprite):
        def __init__(self,  x, y, group, tileWidth, tileLength, color, layer = 1):
            self.color = color
            self.x = x*TILESIZE
            self.y = y*TILESIZE
            self.groups = group, all_sprites
            if group == None:
                self.groups = all_sprites
            self._layer = layer
            self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(self.color)
            self.image = pg.transform.scale(self.image, (tileWidth, tileLength))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            super().__init__(self.groups)

    class Player(createTile):
        def __init__(self, x, y, group, tileWidth, tileLength, color):
            super().__init__(x, y, group, tileWidth, tileLength, color, 3)
            self.speed_x, self.speed_y = 0, 0
            self.jumped = False
            self.onStair = False
            self.climebed = False
            if self.rect.y <= 250:
                self.climebed = True
            
        def move(self):
            if self.rect.y <= 250:
                self.climebed = True
            else:
                self.climebed = False
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
            if player.onStair == False:
                self.speed_y += GRAVITY
            self.rect.y += self.speed_y
            spritesTouched = pg.sprite.spritecollide(self, floor, False)
            if self.speed_y > 0 and player.onStair == False:
                for sprite in spritesTouched:
                    self.rect.bottom = min(self.rect.bottom, sprite.rect.top)
                    self.jumped = False
                    self.speed_y = 0
            elif self.speed_y < 0 and player.onStair == False:
                for sprite in spritesTouched:
                    self.rect.top = max(self.rect.top, sprite.rect.bottom)
    class Stair(createTile):
        def __init__(self, x, y, group, tileWidth, tileLength, color):
            super().__init__(x, y, group, tileWidth, tileLength, color, 2)
        def clicked(self):
            player.rect.left = self.rect.centerx 
            if player.climebed == False:
                player.onStair = True
                player.speed_y = -2
            else:
                player.onStair = True
                player.speed_y = 2
    for i, row in enumerate(tileMap):
        for b, c in enumerate(row):
            if c == 'W':
                createTile(b, i, walls, 64, 64, BROWN)
            elif c == 'F':
                createTile(b, i, floor, 64, 64, BLACK)
            elif c == 'S':
                stair = Stair(b, i, None, 128, 448, PINK)
            elif c == 'P':
                player = Player(b, i, None, 40, 120, RED)
    while True:
        screen.fill((0, 255, 255))
        
        player.speed_x = 0
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        if player.onStair == True and player.rect.y == 586:
            player.onStair = False
        elif player.onStair == True and player.rect.y == 200:
            player.onStair = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    sys.exit()
                elif e.key == pg.K_f:
                    if player.rect.x - stair.rect.x <= 170 and player.rect.x - stair.rect.x >= -170 and player.rect.y >= 200:
                        player.onStair = True
                        stair.clicked()
        pressed = pg.key.get_pressed()
        if pressed[pg.K_d] and pressed[pg.K_a] == False and player.onStair == False:
            player.speed_x += 3
        if pressed[pg.K_a] and pressed[pg.K_d] == False and player.onStair == False:
            player.speed_x -= 3 
        if pressed[pg.K_SPACE] and player.jumped == False and player.onStair == False:
            player.jumped = True
            player.speed_y = -20
        player.move()
        pg.display.update()
        fps.tick(60)
if __name__ == '__main__':
    main()