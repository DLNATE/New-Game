import pygame as pg
import sys 

def main():
    health = 100
    hunger = 100
    stress = 0
    temp = 0
    energy = 100
    fps = pg.time.Clock()
    screen = pg.display.set_mode((1280, 720))
    while True:
        screen.fill((0, 255, 255))
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
        pg.display.update()
        fps.tick(60)
if __name__ == '__main__':
    main()