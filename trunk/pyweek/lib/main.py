
import os, random

import pygame
from pygame.locals import *

#load pyglibs
import pyglibs
from pyglibs import isometric
from pyglibs import image

#a special divide that allows division by 0
def spc_div(a, b):
    if a and b:
        return a/b
    return 0

def main():
    #setup pygame
    pygame.init()
    screen=pygame.display.set_mode((320,240))

    #load assets
    red=image.load_image(os.path.join("data","images","red_tile.bmp"),-1)
    green=image.load_image(os.path.join("data","images","green_tile.bmp"), -1)

    #create a map
    m=[]
    #50x50 is a lttle too large to use well at 640x480 screen size
    #you will probably want no more than 25x25
    for y in range(50):
        m.append([])
        for x in range(50):
            m[y].append(random.choice(["r", "g"]))

    #create our world
    world=isometric.World(map=m, tiles={"r":red,
                                        "g":green},
                          tile_size=[100,50])

    #create a camera
    camera=isometric.Camera(world, [0,0], rect=screen.get_rect())

    #to allow holding keys
    pygame.key.set_repeat(5)

    clock=pygame.time.Clock()

    while 1:
        #lets see how fast we are going
        clock.tick(999)

        for event in pygame.event.get():
            if event.type==QUIT:
                print clock.get_fps()
                pygame.quit()
                return

            if event.type==KEYDOWN:
                #move our hero
                if event.key==K_LEFT:
                    unit.move((-0.025,0))
                if event.key==K_RIGHT:
                    unit.move((0.025,0))

                if event.key==K_UP:
                    unit.move((0,-0.025))
                if event.key==K_DOWN:
                    unit.move((0,0.025))


        #clear the screen
        screen.fill((0,0,0,0))

        camera.render(screen, [])
        pygame.display.flip()

if __name__=="__main__":
    main()