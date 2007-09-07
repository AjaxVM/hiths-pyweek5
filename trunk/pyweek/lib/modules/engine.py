import os, random, time

import pygame
from pygame.locals import *

import pyglibs, entities, elements, engine
from pyglibs import isometric, image, gui

def spc_div(a, b):
    if a and b:
        return a/b
    return 0

#FIXME: just a dummy function
def dummy(arg1):
    pass

class Engine(object):
    def __init__(self, state="game"):
        self.state=state
        self.possiblestates = ["game", "mainmenu", "QUIT"]
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
            elif self.state=="mainmenu":
                self.play_mainmenu()
            elif self.state=="QUIT":
                return


    def play_mainmenu(self):
        data=elements.load_file(elements.path(self.campaign),
                                self.core_data)        
        
        background=gui.Panel([0,0],[640,480],
                            image=data['images']['mosaic_panel'])
        
        buttons = gui.Container()

        buttonfont = pyglibs.font.Font(size=48, antialias=True)
        
        buttons.add(gui.Button([250,200],buttonfont,'Play Game',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[]),
                    "play_game")
        buttons.add(gui.Button([250,250],buttonfont,'Credits',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[]),
                    "credits")
        buttons.add(gui.Button([250,300],buttonfont,'Quit',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[]),
                    "quit")
        
        
        
        pygame.key.set_repeat(5)

        pygame.mixer.music.load(data['music']['darktheme'])
        pygame.mixer.music.play(-1)

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
                    # send it to the gui
                    buttons.update(event)

                    # quit/play game
                    if buttons.get("play_game").was_clicked:
                        self.state="game"
                        return
                    if buttons.get("quit").was_clicked:
                        self.state="QUIT"
                        return

            #clear the screen
            self.screen.fill((0,0,0,0))
            
            background.render(self.screen)
            buttons.render(self.screen)
            
            pygame.display.flip()


    def play_game(self):
        self.screen.fill((0,0,0,0))

        data=elements.load_file(elements.path(self.campaign),
                                self.core_data)

        world=data['world']
        scenario=data['campaigns']['default'].current_scenario

        cities=isometric.UnitContainer()
        for i in scenario.cities:
            cities.add(i)
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
                                    color=(240,255,132))
        
        infofont = pyglibs.font.Font(size=16, antialias=True,
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
        
        # unit stats
        rightpanel.add(gui.Label([550, 210],infofont,
                        align=['center','center'],
                        message='HP: (??/??)'),
                        "unit_hp")
        rightpanel.add(gui.Label([510, 230],infofont,
                        align=['center','center'],
                        message='AV: ??'),
                        "unit_attack")
        rightpanel.add(gui.Label([550, 230],infofont,
                        align=['center','center'],
                        message='DV: ??'),
                        "unit_defense")
        
        # buttons
        rightpanel.add(gui.Button([510,250],buttonfont,'recruit',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(dummy, ['foo'])]),
                        "recruit")
        rightpanel.add(gui.Button([510,280],buttonfont,'harvest',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(dummy, ['foo'])]),
                        "harvest")
        rightpanel.add(gui.Button([510,310],buttonfont,'loiter',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(dummy, ['foo'])]),
                        "loiter")
                        
        bottompanel=gui.Container()
        bottompanel.add(gui.MessageBox([0,340],
                        normalfont,
                        image=data['images']['cloth_panel'],
                        area=[500,140],
                        messages=["here","is","a","multiline","message","box"]),
                        "messages")

        pygame.key.set_repeat(5)

        pygame.mixer.music.load(data['music']['warm_strings'])
        pygame.mixer.music.play(-1)

        clock=pygame.time.Clock()

        while 1:
            clock.tick(999)#the fastest we can go, change to something reasonable, like 40-50 later

            for event in pygame.event.get():
                if event.type==QUIT:
                    print clock.get_fps()
                    pygame.quit()
                    return

                rightpanel.update(event)

                if event.type==KEYDOWN:
                    if event.key==K_s:
                        pygame.image.save(self.screen, os.path.join("data", "screens",
                                            "screenie--%s.bmp"%time.strftime("%d-%m-%Y-%H-%M")))
                    elif event.key ==K_ESCAPE:
                        pygame.quit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if camera.rect.collidepoint(event.pos):
                        # test if one of the player's units or builings was clicked
                        clicked_tile = camera.get_mouse_pos()
                        for entity in player.armies+player.houses:
                            if entity.tile_pos == clicked_tile:
                                player.active_entity = entity
                                break
                            
                        # make the unit do something
                        # we really need to send unit what tile was clicked...
                        if event.button == 1:
                            player.active_entity.leftClick(clicked_tile)
                        if event.button == 3:
                            player.active_entity.rightClick(clicked_tile)
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


            mpos=pygame.mouse.get_pos()
            if mpos[0] < 5:     #left
                camera.move([0.1, -0.1])
            if mpos[1] < 5:     #up
                camera.move([0.1, 0.1])

            if mpos[0] > 635:   #right
                camera.move([-0.1, 0.1])
            if mpos[1] > 475:   #down
                camera.move([-0.1, -0.1])

            #clear the screen
            self.screen.fill((0,0,0,0))
            camera.render(self.screen, [player, cities])
            player.update()
            rightpanel.render(self.screen)
            rightpanel.get("info_food").message="food: %s"%player.food
            rightpanel.get("info_food").refactor()
            
            bottompanel.render(self.screen)
            pygame.display.flip()
