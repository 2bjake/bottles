import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

# set up the window
DISPLAY_SURFACE = pg.display.set_mode((400, 300), 0, 32)
pg.display.set_caption('Fill')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)

#bottle position
TOPX = 100
TOPY = 50

#bottle size
BOTTLE_HEIGHT = 200
BOTTLE_WIDTH = 100

FILL_RATE = 1

fill_percent = 0
fill_adjust = 0
liquid_height = 0 #this is derived on change, get rid of this global

#sound settings
BASE_FREQ = 175
FREQ_RANGE = 175
VOLUME = 0.5
tone = GenerateTone(freq=BASE_FREQ, vol=.5)
tone_playing = False

def getTone(fill_percent):
    new_freq = BASE_FREQ +  (FREQ_RANGE * fill_percent / 100)
    return GenerateTone(freq=new_freq, vol=VOLUME)

# run the game loop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
            fill_adjust = 0
        elif event.type == KEYDOWN and event.key == K_UP:
            fill_adjust = FILL_RATE
        elif event.type == KEYDOWN and event.key == K_DOWN:
            fill_adjust = -FILL_RATE
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
        liquid_height = BOTTLE_HEIGHT * fill_percent / 100

    DISPLAY_SURFACE.fill(WHITE)
    pg.draw.rect(DISPLAY_SURFACE, BLACK, (TOPX, TOPY, BOTTLE_WIDTH, BOTTLE_HEIGHT), 1);
    pg.draw.rect(DISPLAY_SURFACE, BLUE, (TOPX, TOPY + (BOTTLE_HEIGHT - liquid_height) , BOTTLE_WIDTH, liquid_height));

    if tone_playing:
        pg.mixer.Channel(0).queue(getTone(fill_percent))

    pg.display.update()
