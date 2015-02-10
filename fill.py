import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone as generate_tone
from bottle import Bottle

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)

#TODO: these frequency settings should be derived from the shape and air volume in the bottle
# see: http://physics.stackexchange.com/questions/44601/frequency-of-the-sound-when-blowing-in-a-bottle
BASE_FREQ = 175
FREQ_RANGE = 175
VOLUME = 0.5

def get_tone(fill_percent):
    new_freq = BASE_FREQ + (FREQ_RANGE * fill_percent / 100)
    return generate_tone(freq=new_freq, vol=VOLUME)

def draw_bottle(screen, bottle_pos_x, bottle_pos_y, bottle):
    pg.draw.rect(screen, BLACK, (bottle_pos_x, bottle_pos_y, bottle.width, bottle.height), 1);
    if bottle.liquid_height() > 0:
        pg.draw.rect(screen, BLUE, (bottle_pos_x, bottle_pos_y + (bottle.height - bottle.liquid_height()) , bottle.width, bottle.liquid_height()));

def play_bottle_tone(bottle):
    pg.mixer.Channel(0).queue(get_tone(bottle.percent_filled))

def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()

    # set up the window
    screen = pg.display.set_mode((600, 450), 0, 32)
    pg.display.set_caption('Bottle Music')

    my_bottle = Bottle(200, 100, 20)

    #bottle position
    bottle_pos_x = 100
    bottle_pos_y = 50

    fill_rate = 1 # percentage to fill per cycle, range from 1 - 100

    fill_adjust = 0

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

        my_bottle.adjust_liquid(fill_adjust)

        screen.fill(WHITE)
        draw_bottle(screen, bottle_pos_x, bottle_pos_y, my_bottle)

        if tone_playing:
            play_bottle_tone(my_bottle)

        pg.display.update()

if __name__ == '__main__': main()
