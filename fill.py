import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone as generate_tone
from bottle import Bottle

BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
BLUE       = (  0,   0, 255)
PURPLE     = (160,  32, 240)
GREEN      = (  0, 100,   0)
YELLOW     = (255, 215,   0)

BOTTLE_BORDER = BLACK
EMPTY_BOTTLE = (255, 255, 240)
BACKGROUND   = (205, 200, 177)

#TODO: the frequency should be derived from the shape and air volume in the bottle
# see: http://physics.stackexchange.com/questions/44601/frequency-of-the-sound-when-blowing-in-a-bottle
BASE_FREQ = 175
FREQ_RANGE = 175
VOLUME = 0.5

def play_bottle_tone(bottle):
    freq = BASE_FREQ + (FREQ_RANGE * bottle.percent_filled / 100)
    pg.mixer.Channel(0).queue(generate_tone(freq=freq, vol=VOLUME))

def render_bottle(screen, position_tuple, bottle):
    border_width = 1
    pos_x = position_tuple[0]
    pos_y = position_tuple[1]
    pg.draw.rect(screen, EMPTY_BOTTLE, (pos_x, pos_y, bottle.width, bottle.height))
    pg.draw.rect(screen, BLACK, (pos_x, pos_y, bottle.width, bottle.height), border_width)
    if bottle.liquid_height > 0:
        liquid_pos_x = pos_x + border_width
        liquid_pos_y = pos_y + border_width + bottle.height - bottle.liquid_height
        liquid_width = bottle.width - border_width * 2
        liquid_height = bottle.liquid_height - border_width * 2
        pg.draw.rect(screen, bottle.liquid_color, (liquid_pos_x, liquid_pos_y, liquid_width, liquid_height))

def render(screen, bottles):
    screen.fill(BACKGROUND)
    for bottle_key in bottles:
        render_bottle(screen, bottles[bottle_key]['position'], bottles[bottle_key]['bottle'])

def add_bottle(bottles, position_tuple, bottle):
    rect = pg.Rect(position_tuple, (bottle.width, bottle.height))
    bottles[tuple(rect)] = {'bottle': bottle, 'position': position_tuple} #rect in tuple because rect isn't hashable

def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()

    # set up the window
    screen = pg.display.set_mode((650, 300), 0, 32)
    pg.display.set_caption('Bottle Music')

    bottles = {}
    add_bottle(bottles, (50, 50), Bottle(100, 200, 35, PURPLE))
    add_bottle(bottles, (200, 50), Bottle(100, 200, 50, BLUE))
    add_bottle(bottles, (350, 50), Bottle(100, 200, 70, GREEN))
    add_bottle(bottles, (500, 50), Bottle(100, 200, 100, YELLOW))

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

        cursor_rect = pg.Rect(pg.mouse.get_pos(), (0, 0))
        bottle_keyval = cursor_rect.collidedict(bottles)

        if bottle_keyval is not None:
            current_bottle = bottle_keyval[1]['bottle']
            current_bottle.adjust_liquid(fill_adjust)

            if tone_playing:
                play_bottle_tone(current_bottle)

        render(screen, bottles)
        pg.display.update()

if __name__ == '__main__': main()
