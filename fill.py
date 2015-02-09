import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone as generate_tone

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)

#sound settings #TODO: move these frequency settings into bottle Class
BASE_FREQ = 175
FREQ_RANGE = 175
VOLUME = 0.5

def get_tone(fill_percent):
    new_freq = BASE_FREQ +  (FREQ_RANGE * fill_percent / 100)
    return generate_tone(freq=new_freq, vol=VOLUME)

def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()

    # set up the window
    screen = pg.display.set_mode((400, 300), 0, 32)
    pg.display.set_caption('Bottle Music')

    #bottle position
    bottle_pos_x = 100
    bottle_pos_y = 50

    #bottle size
    bottle_height = 200
    bottle_width = 100

    fill_rate = 1 # percentage to fill per cycle, range from 1 - 100

    fill_percent = 0
    fill_adjust = 0
    liquid_height = 0

    tone_playing = False

    # run the game loop
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
                fill_adjust = 0
            elif event.type == KEYDOWN and event.key == K_UP:
                fill_adjust = fill_rate
            elif event.type == KEYDOWN and event.key == K_DOWN:
                fill_adjust = -fill_rate
            elif (event.type == KEYDOWN and event.key == K_b) or event.type == MOUSEBUTTONDOWN:
                tone_playing = True
            elif (event.type == KEYUP and event.key == K_b) or event.type == MOUSEBUTTONUP:
                tone_playing = False

        if fill_adjust != 0:
            fill_percent += fill_adjust
            if fill_percent > 100:
                fill_percent = 100
            elif fill_percent < 0:
                fill_percent = 0
        liquid_height = bottle_height * fill_percent / 100

        screen.fill(WHITE)
        pg.draw.rect(screen, BLACK, (bottle_pos_x, bottle_pos_y, bottle_width, bottle_height), 1);
        pg.draw.rect(screen, BLUE, (bottle_pos_x, bottle_pos_y + (bottle_height - liquid_height) , bottle_width, liquid_height));

        if tone_playing:
            pg.mixer.Channel(0).queue(get_tone(fill_percent))

        pg.display.update()

if __name__ == '__main__': main()
