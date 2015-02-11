import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone as generate_tone
from colors import * #TODO figure out the right way to do modules
from notes import *
from bottle import Bottle
from song import Song

BOTTLE_BORDER = BLACK
EMPTY_BOTTLE = (255, 255, 240)
BACKGROUND   = (205, 200, 177)

VOLUME = 0.5

def play_bottle_tone(bottle):
    pg.mixer.Channel(0).queue(generate_tone(freq=bottle.blow_frequency, vol=VOLUME))

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
        liquid_color = get_frequency_color(bottle.blow_frequency)
        pg.draw.rect(screen, liquid_color, (liquid_pos_x, liquid_pos_y, liquid_width, liquid_height))

def render_song(screen, song):
    song_pos_x = 25
    note_spacing_x = 25
    song_pos_y = 400
    note_size = 50
    phrase_size = 8
    current_note_border = 3

    notes = song.get_current_phrase(phrase_size)
    for index, note in enumerate(notes['notes']):
        color = get_frequency_color(note)
        pos_x = song_pos_x + (index * (note_spacing_x + note_size))
        pg.draw.rect(screen, color, (pos_x, song_pos_y, note_size, note_size))
        if index == notes['cur_idx']:
            pg.draw.rect(screen, BOTTLE_BORDER, (pos_x, song_pos_y, note_size, note_size), current_note_border)

def render(screen, bottles, song):
    screen.fill(BACKGROUND)
    render_song(screen, song)
    for bottle_key in bottles:
        render_bottle(screen, bottles[bottle_key]['position'], bottles[bottle_key]['bottle'])

def add_bottle(bottles, position_tuple, bottle):
    rect = pg.Rect(position_tuple, (bottle.width, bottle.height))
    bottles[tuple(rect)] = {'bottle': bottle, 'position': position_tuple} #rect in tuple because rect isn't hashable

def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    clock = pg.time.Clock()

    # set up the window
    screen = pg.display.set_mode((650, 500), 0, 32)
    pg.display.set_caption('Bottle Music')

    bottles = {}
    add_bottle(bottles, (50, 50), Bottle(100, 200))
    add_bottle(bottles, (200, 50), Bottle(100, 200))
    add_bottle(bottles, (350, 50), Bottle(100, 200))
    add_bottle(bottles, (500, 50), Bottle(100, 200))

    song = Song()

    fill_rate = 1 # percentage to fill per cycle, range from 1 - 100

    fill_adjust = 0

    tone_playing = False
    is_new_note = False
    # run the game loop
    while True:
        clock.tick(50)
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
                is_new_note = not tone_playing
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
                if is_new_note:
                    song.play_note(current_bottle.blow_frequency)
                    is_new_note = False

        render(screen, bottles, song)
        pg.display.update()

if __name__ == '__main__': main()
