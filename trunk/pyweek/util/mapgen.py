import sys

if len(sys.argv) != 3:
    print 'usage: '
    print 'mapgen.py <width> <height>'
    print 'where width and height are each a number of tiles'
    sys.exit()

width=int(sys.argv[1])
height=int(sys.argv[2])
TILESIZE = 20
brush = 'd'

map = []
for y in range(height):
    map.append([])
    for x in range(width):
        map[y].append('g')

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((TILESIZE*width,TILESIZE*height))

colors = {'g':(0,200,0,0),'d':(100,50,50,0),'l':(200,0,0,0),'s':(200,200,200,0)}

def draw():
    for y in range(height):
        for x in range(width):
            color = colors[map[x][y]]
            rect= pygame.Rect((x*TILESIZE, y*TILESIZE), (TILESIZE, TILESIZE))
            screen.fill(color, rect)
    pygame.display.flip()

draw()
running = True 
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_g:
            brush = 'g'
        elif event.type == KEYDOWN and event.key == K_d:
            brush = 'd'  
        elif event.type == KEYDOWN and event.key == K_l:
            brush = 'l'
        elif event.type == KEYDOWN and event.key == K_s:
            brush = 's' 
        elif event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE):
            running = False
        elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION and event.buttons[0]:
            x,y = event.pos[0]/TILESIZE,event.pos[1]/TILESIZE
            map[x][y] = brush
            draw()

#output map to a file
mapstring = str(map).replace('], [','],\n[')
mapfile = open('mapfile.py','w')
mapfile.write('m = '+mapstring)
mapfile.close()