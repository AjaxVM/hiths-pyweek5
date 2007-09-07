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
        scenario=data['campaigns']['default'].current_scenario

        camera=isometric.Camera(world, data['camera_pos'],
                                rect=pygame.rect.Rect([10,10], [480, 320]),
                                background_image=data['images']['map_bg_image'])

        player=scenario.player

        normalfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(232,232,232))

        
        blackfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(16,16,16))
        
        buttonfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(255,255,255))
        


        rightpanel=gui.Container()
        
        rightpanel.add(gui.Panel([500,0], [200,480],
                        image=data['images']['mosaic_panel'],
                        image_mode="scale"),
                        "background")
        
        rightpanel.add(gui.Label([510,10],
                        normalfont,
                        message="food: %s"%player.food),
                        "info_food")
        rightpanel.add(gui.Label([510,70],
                        normalfont,
                        message="unit_name?"),
                        "unit_name")
        
        # portrait!
        rightpanel.add(gui.Panel([520,100], [100, 100],
                        image=data['images']['portrait_default'],
                        image_mode="scale"),
                        "portrait")
        
        # buttons
        rightpanel.add(gui.Button([510,220],buttonfont,'recruit',
                        image_normal=data['images']['button'],
                        codes=[]),
                        "recruit")
        rightpanel.add(gui.Button([510,250],buttonfont,'dance!',
                        image_normal=data['images']['button'],
                        codes=[]),
                        "dance!")
        rightpanel.add(gui.Button([510,280],buttonfont,'loiter',
                        image_normal=data['images']['button'],
                        codes=[]),
                        "loiter")
                        
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
                        if event.button == 1:
                            player.active_entity.leftClick(camera.get_mouse_pos())
                        if event.button == 3:
                            player.active_entity.rightClick(camera.get_mouse_pos())
                    else:
                        # send it to the gui
                        pass

            #lets handle the scenarios events...
            for event in scenario.events:
                trigger=False
                exec event.trigger
                if trigger:
                    exec event.event
                    scenario.events.remove(event)

            #clear the screen
            self.screen.fill((0,0,0,0))
            camera.render(self.screen, player)
            player.update()
            rightpanel.render(self.screen)
            rightpanel.get("info_food").message="food: %s"%player.food
            rightpanel.get("info_food").refactor()
            
            bottompanel.render(self.screen)
            pygame.display.flip()
