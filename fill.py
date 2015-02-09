import pygame, sys
from pygame.locals import *
from generate import GenerateTone

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

CHANNEL = pygame.mixer.Channel(0)

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Fill')

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

fillPercent = 0
fillAdjust = 0
liquidHeight = 0 #this is derived on change, get rid of this global

#sound settings
BASE_FREQ = 175
FREQ_RANGE = 175
VOLUME = 0.5
tone = GenerateTone(freq=BASE_FREQ, vol=.5)
tonePlaying = False

def getTone(fillPercent):
    newFreq = BASE_FREQ +  (FREQ_RANGE * fillPercent / 100)
    return GenerateTone(freq=newFreq, vol=VOLUME)

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
            fillAdjust = 0
        elif event.type == KEYDOWN and event.key == K_UP:
            fillAdjust = FILL_RATE
        elif event.type == KEYDOWN and event.key == K_DOWN:
            fillAdjust = -FILL_RATE
        elif event.type == KEYDOWN and event.key == K_b:
            tonePlaying = True
        elif event.type == KEYUP and event.key == K_b:
            tonePlaying = False

    if fillAdjust != 0:
        fillPercent += fillAdjust
        if fillPercent > 100:
            fillPercent = 100
        elif fillPercent < 0:
            fillPercent = 0
        liquidHeight = BOTTLE_HEIGHT * fillPercent / 100

    DISPLAYSURF.fill(WHITE)
    pygame.draw.rect(DISPLAYSURF, BLUE, (TOPX, TOPY + (BOTTLE_HEIGHT - liquidHeight) , BOTTLE_WIDTH, liquidHeight));
    pygame.draw.rect(DISPLAYSURF, BLACK, (TOPX, TOPY, BOTTLE_WIDTH, BOTTLE_HEIGHT), 1);


    if tonePlaying:
        CHANNEL.queue(getTone(fillPercent))

    pygame.display.update()
