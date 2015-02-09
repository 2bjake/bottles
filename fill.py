import pygame, sys
from pygame.locals import *
from generate import GenerateTone

pygame.mixer.pre_init(44100, -16, 1, 2048)
pygame.init()

CHANNEL = pygame.mixer.Channel(0)

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Fill')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)

TOPX = 100
TOPY = 50
BOTTLE_HEIGHT = 200
BOTTLE_WIDTH = 100

fillPercent = 0
FILL_CHANGE_SIZE = 5
liquidHeight = 0 #this is derived on change, get rid of this global

BASE_FREQ = 175
tone = GenerateTone(freq=BASE_FREQ, vol=.5)
tonePlaying = False

sounds = [None, None]



def updateTone(fillPercent):
	global tone
	newFreq = BASE_FREQ +  (175 * fillPercent / 100)
	tone = GenerateTone(freq=newFreq, vol=.5)

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP and event.key == K_UP:
        	if fillPercent < 100:
        		fillPercent += FILL_CHANGE_SIZE
        	liquidHeight = BOTTLE_HEIGHT * fillPercent / 100
        	updateTone(fillPercent)
        elif event.type == KEYUP and event.key == K_DOWN:
        	if fillPercent > 0:
        		fillPercent -= FILL_CHANGE_SIZE
        	liquidHeight = BOTTLE_HEIGHT * fillPercent / 100 
        	updateTone(fillPercent)
        elif event.type == KEYDOWN and event.key == K_b:
        	tonePlaying = True
        elif event.type == KEYUP and event.key == K_b:
        	tonePlaying = False

    	DISPLAYSURF.fill(WHITE)
    	pygame.draw.rect(DISPLAYSURF, BLUE, (TOPX, TOPY + (BOTTLE_HEIGHT - liquidHeight) , BOTTLE_WIDTH, liquidHeight));
    	pygame.draw.rect(DISPLAYSURF, BLACK, (TOPX, TOPY, BOTTLE_WIDTH, BOTTLE_HEIGHT), 1);    	

    if tonePlaying:
    	if not CHANNEL.get_busy():
    		CHANNEL.play(tone)
    	else:
    		CHANNEL.queue(tone)

    pygame.display.update()
