import sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print """
    usage: 
        mapgen.py <width> <height>
        or
        mapgen.py <mapfile>
        width and height are each a number of tiles
        the created map will be in mapfile.py
        """
    sys.exit()

elif len(sys.argv) == 3:
    width=int(sys.argv[1])
    height=int(sys.argv[2])
    themap = []
    for y in range(height):
        themap.append([])
        for x in range(width):
            themap[y].append('g')
    
elif len(sys.argv) == 2:
    execfile(sys.argv[1])
    width = len(themap[0])
    height = len(themap)
    
TILESIZE = 20
brush = 'd'



import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((TILESIZE*width,TILESIZE*height))

colors = {'g':(0,200,0,0),'d':(100,50,50,0),'l':(200,0,0,0),'s':(200,200,200,0)}

def draw():
    for y in range(height):
        for x in range(width):
            color = colors[themap[x][y]]
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
            themap[x][y] = brush
            draw()

#output themap to a file
themapstring = str(themap).replace('], [','],\n[')
themapfile = open('mapfile.py','w')
themapfile.write('themap = '+themapstring)
themapfile.close()