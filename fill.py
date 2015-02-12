import sys
import pygame as pg
from pygame.locals import *
from generate import GenerateTone as generate_tone
import colors
import music
import bottle as bottle_mod

BOTTLE_BORDER = colors.BLACK
EMPTY_BOTTLE = (255, 255, 240)
BACKGROUND   = (205, 200, 177)

VOLUME = 0.5

def play_bottle_tone(bottle):
    pg.mixer.Channel(0).queue(generate_tone(freq=bottle.blow_frequency, vol=VOLUME))

def render_bottle(screen, bottle, current=False):
    border_width = 1

    pos_x = bottle.position[0]
    pos_y = bottle.position[1]

    pg.draw.rect(screen, EMPTY_BOTTLE, bottle.get_rect())
    pg.draw.rect(screen, BOTTLE_BORDER, bottle.get_rect(), border_width)
    if current:
        pg.draw.circle(screen, colors.RED, (pos_x + bottle.width / 2, pos_y + bottle.height + 25), 5)
    if bottle.liquid_height > 0:
        liquid_pos_x = pos_x + border_width
        liquid_pos_y = pos_y + border_width + bottle.height - bottle.liquid_height
        liquid_width = bottle.width - border_width * 2
        liquid_height = bottle.liquid_height - border_width * 2
        liquid_color = music.get_frequency_color(bottle.blow_frequency)
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
        color = music.get_frequency_color(note)
        pos_x = song_pos_x + (index * (note_spacing_x + note_size))
        pg.draw.rect(screen, color, (pos_x, song_pos_y, note_size, note_size))
        if index == notes['cur_idx']:
            pg.draw.rect(screen, colors.BLACK, (pos_x, song_pos_y, note_size, note_size), current_note_border)

def render(screen, cur_bottle_idx, bottles, song):
    screen.fill(BACKGROUND)
    render_song(screen, song)
    for idx, bottle in enumerate(bottles):
        current = (idx == cur_bottle_idx)
        render_bottle(screen, bottle, current)

def is_key_event(event, type, *args):
    return event.type == type and event.key in args

def main():
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    clock = pg.time.Clock()

    screen = pg.display.set_mode((650, 500), 0, 32)
    pg.display.set_caption('Bottle Music')

    bottle_list = []
    for i in range(0, 4):
        x_pos = 50 + (i * 150)
        bottle_list.append(bottle_mod.Bottle((x_pos, 50), 100, 200))
    cur_bottle_idx = 0;

    song = music.Song()

    fill_rate = 2 # percentage to fill per cycle, range from 1 - 100

    fill_adjust = 0

    tone_playing = False
    is_new_note = False

    while True:
        clock.tick(50)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif is_key_event(event, KEYUP, K_r):
                song = music.Song()
            elif is_key_event(event, KEYUP, K_UP, K_DOWN):
                fill_adjust = 0
            elif is_key_event(event, KEYDOWN, K_UP):
                fill_adjust = fill_rate
            elif is_key_event(event, KEYDOWN, K_DOWN):
                fill_adjust = -fill_rate
            elif is_key_event(event, KEYDOWN, K_b, K_SPACE):
                is_new_note = not tone_playing
                tone_playing = True
            elif is_key_event(event, KEYUP, K_b, K_SPACE):
                tone_playing = False
            elif is_key_event(event, KEYUP, K_LEFT):
                cur_bottle_idx -= 1
                if cur_bottle_idx < 0:
                    cur_bottle_idx = 0
            elif is_key_event(event, KEYUP, K_RIGHT):
                cur_bottle_idx += 1
                if cur_bottle_idx >= len(bottle_list):
                    cur_bottle_idx = len(bottle_list) - 1

        current_bottle = bottle_list[cur_bottle_idx]
        current_bottle.adjust_liquid(fill_adjust)

        if tone_playing:
            play_bottle_tone(current_bottle)
            if is_new_note:
                song.play_note(current_bottle.blow_frequency)
                is_new_note = False

        render(screen, cur_bottle_idx, bottle_list, song)
        pg.display.update()

if __name__ == '__main__': main()
