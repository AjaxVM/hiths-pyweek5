
import os, random, time

import pygame
from pygame.locals import *

import modules

from modules import pyglibs, entities, elements
from modules.pyglibs import isometric
from modules.pyglibs import image
from modules.pyglibs import gui

#a special divide that allows division by 0
def spc_div(a, b):
    if a and b:
        return a/b
    return 0

def main():
    #setup pygame
    pygame.init()
    screen=pygame.display.set_mode((320,240))
    pygame.display.set_caption("Scions of Darkness")

    #load assets
    red=image.load_image(os.path.join("data","images","red_tile.bmp"),-1)#-1 uses a colorkey
    green=image.load_image(os.path.join("data","images","green_tile.bmp"), -1)

    mud=image.load_image(os.path.join("data","images","mud.bmp"), -1)
    bg_image=image.load_surface(os.path.join("data", "images", "map_bg.bmp"))

    button=image.load_image(os.path.join("data", "images", "button.bmp"), -1)

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
    camera=isometric.Camera(world, [0,0], rect=screen.get_rect(),
                            background_image=bg_image)


    #create basic units/races/etc.
    race1=entities.Race()
    race1.house_image=button
    race1.elder_image = race1.captain_image = mud
    glyph1=entities.Glyph()

    basic_player=entities.Player("jimbob", race1)
    basic_player.create_house(world, [0,0])
    basic_player.houses[0].make_unit("bob II", {"Recruit":50})
    basic_player.active_entity = basic_player.armies[0]

    info_food=gui.Label([10,0],
                        pyglibs.font.Font(antialias=True),
                        message="food: 100")

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
                if event.key==K_s:
                    pygame.image.save(screen, os.path.join("data", "screens",
                                        "screenie--%s.bmp"%time.strftime("%d-%m-%Y-%H-%M")))
                elif event.key ==K_ESCAPE:
                    pygame.quit()
                
            if event.type == MOUSEBUTTONDOWN:
                if camera.rect.collidepoint(event.pos):
                    # make the unit do something
                    basic_player.active_entity.handleClick(event)
                else:
                    # send it to the gui
                    pass

        #clear the screen
        screen.fill((0,0,0,0))
##        camera.center_at(basic_player.houses[0].pos)
        camera.render(screen, basic_player)
        basic_player.update()
        info_food.render(screen)
        pygame.display.flip()

if __name__=="__main__":
    main()
