import os, random, time

import pygame
from pygame.locals import *

import pyglibs, entities, elements, engine
from pyglibs import isometric, image, gui

def spc_div(a, b):
    if a and b:
        return a/b
    return 0

class Engine(object):
    def __init__(self, state="game"):
        self.state=state
        self.campaign="basic.py"
        self.scenario=None#we'll add this later when you can actually do somthing with the campaigns

        self.init()
        
        self.run()

    def init(self):
        pygame.init()
        self.screen=pygame.display.set_mode((640, 480))

        self.core_data=elements.load_file(os.path.join('data', 'game_core.py'))

    def run(self):
        while 1:
            if self.state=="game":
                self.play_game()
            elif self.state=="QUIT":
                return

    def play_game(self):
        self.screen.fill((0,0,0,0))

        data=elements.load_file(elements.path(self.campaign),
                                self.core_data)

        world=data['world']

        camera=isometric.Camera(world, data['camera_pos'],
                                rect=pygame.rect.Rect([10,10], [480, 320]),
                                background_image=data['images']['map_bg_image'])

        basic_player=entities.Player("jimbob", data['races']['default'])
        basic_player.create_house(world, [0,0])
        basic_player.houses[0].make_unit("bob II", {"Recruit":50})
        basic_player.active_entity = basic_player.armies[0]

        normalfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(232,232,232))

        rightpanel=gui.Container()
        
        rightpanel.add(gui.Panel([490,0], [200,480],
                        image=data['images']['mosaic_panel'],
                        image_mode="scale"),
                        "background")
        
        rightpanel.add(gui.Label([500,10],
                        normalfont,
                        message="food: %s"%basic_player.food),
                        "info_food")
        rightpanel.add(gui.Label([500,80],
                        normalfont,
                        message="unit_name?"),
                        "unit_name")

        bottompanel=gui.Container()
        bottompanel.add(gui.MessageBox([0,340],
                        normalfont,
                        image=data['images']['cloth_panel'],
                        area=[500,140],
                        messages=["here","is","a","multiline","message","box"]),
                        "messages")

        pygame.key.set_repeat(5)

        clock=pygame.time.Clock()

        while 1:
            clock.tick(999)#the fastest we can go, change to something reasonable, like 40-50 later

            for event in pygame.event.get():
                if event.type==QUIT:
                    print clock.get_fps()
                    pygame.quit()
                    return

                if event.type==KEYDOWN:
                    if event.key==K_s:
                        pygame.image.save(self.screen, os.path.join("data", "screens",
                                            "screenie--%s.bmp"%time.strftime("%d-%m-%Y-%H-%M")))
                    elif event.key ==K_ESCAPE:
                        pygame.quit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if camera.rect.collidepoint(event.pos):
                        # make the unit do something
                        # we really need to send unit what tile was clicked...
                        basic_player.active_entity.handleClick(camera.get_mouse_pos())
                    else:
                        # send it to the gui
                        pass

            #clear the screen
            self.screen.fill((0,0,0,0))
            camera.render(self.screen, basic_player)
            basic_player.update()
            rightpanel.render(self.screen)
            rightpanel.get("info_food").message="food: %s"%basic_player.food
            rightpanel.get("info_food").refactor()
            
            bottompanel.render(self.screen)
            pygame.display.flip()
