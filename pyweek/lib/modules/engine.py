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
        pygame.mixer.pre_init(22050, -16, 1, 2048)
        pygame.init()
        self.screen=pygame.display.set_mode((640, 480))# FULLSCREEN)

        self.core_data=elements.load_file(os.path.join('data', 'game_core.py'))

    def run(self):
        while 1:
            if self.state=="game":
                self.play_game()
            elif self.state=="mainmenu":
                self.play_mainmenu()
            elif self.state=="QUIT":
                pygame.quit()
                return


    def play_mainmenu(self):
        data=elements.load_file(elements.path(self.campaign),
                                self.core_data)        
        # sound for buttons
        clicksound = data['sfx']['click'].play
        
        background=gui.Panel([0,0],[640,480],
                            image=data['images']['title'])
        
        buttons = gui.Container()

        buttonfont = pyglibs.font.Font(size=30, antialias=True)
        
        buttons.add(gui.Button([250,380],buttonfont,'Play Game',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[gui.ButtonCode(clicksound, [])],
                    image_mode="scale"),
                    "play_game")
        buttons.add(gui.Button([250,415],buttonfont,'Credits',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[gui.ButtonCode(clicksound, [])],
                    image_mode="scale"),
                    "credits")
        buttons.add(gui.Button([250,450],buttonfont,'Quit',
                    image_normal=data['images']['button'],
                    image_hover=data['images']['buttonh'],
                    image_click=data['images']['buttonc'],
                    align=["center","center"],
                    codes=[gui.ButtonCode(clicksound, [])],
                    image_mode="scale"),
                    "quit")
        
        
        
        pygame.key.set_repeat(5)

        pygame.mixer.music.load(data['music']['darktheme'])
        pygame.mixer.music.play(-1)

        clock=pygame.time.Clock()

        while 1:
            clock.tick(45)

            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    return

                buttons.update(event)

                if event.type==KEYDOWN:
                    if event.key==K_s:
                        pygame.image.save(self.screen, os.path.join("data", "screens",
                                            "screenie--%s.bmp"%time.strftime("%d-%m-%Y-%H-%M")))
                    elif event.key ==K_ESCAPE:
                        pygame.quit()

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
        enemies=scenario.enemies

        normalfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(232,232,232))

        
        blackfont = pyglibs.font.Font(size=24,
                                    antialias=True,
                                    color=(16,16,16))
        
        buttonfont = pyglibs.font.Font(size=20,
                                    antialias=True,
                                    color=(255,255,125))
        
        infofont = pyglibs.font.Font(size=20, antialias=True,
                                    color=(255,255,255))

        # sound for buttons
        clicksound = data['sfx']['click'].play

        rightpanel=gui.Container()
        
        rightpanel.add(gui.Panel([500,0], [200,480],
                        image=data['images']['mosaic_panel'],
                        image_mode="scale"),
                        "background")
        
        rightpanel.add(gui.Label([510,5],
                        normalfont,
                        message="food: %s"%player.food),
                        "info_food")
        rightpanel.add(gui.Label([510,50],
                        normalfont,
                        message="captain: "),
                        "unit_name")
        rightpanel.add(gui.Label([510,75],
                        normalfont,
                        message="captain xp: "),
                        "unit_captain_xp")
        rightpanel.add(gui.Label([510,100],
                        normalfont,
                        message="army xp: "),
                        "unit_army_xp")
        
        # portrait!
        rightpanel.add(gui.Panel([520,125], [100, 100],
                        image=data['images']['blank'],
                        image_mode="scale"),
                        "portrait")
        
        # unit stats
        rightpanel.add(gui.Label([510, 245],infofont,
                        align=['center','center'],
                        message='Soldiers:'),
                        "unit_soldiers")
        rightpanel.add(gui.Label([510, 200],infofont,
                        align=['center','center'],
                        message='AV: ??'),
                        "unit_attack")
        rightpanel.add(gui.Label([510, 220],infofont,
                        align=['center','center'],
                        message='DV: ??'),
                        "unit_defense")
        
        # buttons
        rightpanel.add(gui.Button([535,450],buttonfont,'    Quit    ',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        image_mode="scale",
                        align=["center","center"],
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "quit")


        toppanel_unit=gui.Container()
        toppanel_unit.add(gui.Button([10,335],buttonfont,'recruit',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "recruit")
        toppanel_unit.add(gui.Button([53,335],buttonfont,'forage',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "forage")
        toppanel_unit.add(gui.Button([95,335],buttonfont,'loiter',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "loiter")
        toppanel_unit.add(gui.Button([130,335],buttonfont,'found house',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        image_mode="scale",
                        align=["center","center"],
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "found_house")
        toppanel_unit.set_visible(False)

        toppanel_house=gui.Container()
        toppanel_house.add(gui.Button([10,335],buttonfont,'create unit',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        image_mode="scale",
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "make_unit")
        toppanel_house.add(gui.InputBox(pos=[80,335], font=buttonfont,
                        width=250, start_text="Captain Name",
                        image_normal=data['images']['input_box'],
                        image_hover=data['images']['input_box'],
                        image_click=data['images']['input_box'],
                        image_mode="enlarge", cache_on_KEY=K_RETURN,
                        text_padding=[10,2], ignore_events=["RETURN", "TAB"]),
                        "captain_name")
        #make sure to add a + and a - button up there, so you can click them ;)
        toppanel_house.add(gui.InputBox(pos=[335,335], font=buttonfont,
                        width=50, start_text="50",
                        image_normal=data['images']['input_box'],
                        image_hover=data['images']['input_box'],
                        image_click=data['images']['input_box'],
                        image_mode="scale", cache_on_KEY=K_RETURN,
                        text_padding=[10,2], ignore_events=["RETURN", "TAB"]),
                        "troops")
        toppanel_house.add(gui.Button([390,335],normalfont,' + ',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        image_mode="scale",
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "increase_troops")
        toppanel_house.add(gui.Button([410,335],normalfont,' - ',
                        image_normal=data['images']['button'],
                        image_hover=data['images']['buttonh'],
                        image_click=data['images']['buttonc'],
                        align=["center","center"],
                        image_mode="scale",
                        codes=[gui.ButtonCode(clicksound, [])]),
                        "decrease_troops")
        toppanel_house.set_visible(False)


        bottompanel=gui.Container()
        bottompanel.add(gui.MessageBox([10,360],
                        normalfont,
                        image=data['images']['cloth_panel'],
                        area=[480,120],
                        messages=["Welcome to Scions of Darkness!","Left-Click to select units","Right-click to move them","Have fun and try to destroy all enemies!"]),
                        "messages")

        pygame.key.set_repeat(10, 200)

        pygame.mixer.music.load(data['music']['warm_strings'])
        pygame.mixer.music.play(-1)

        clock=pygame.time.Clock()

        selected_object=None

        arrow_keys=[0,0,0,0]

        while 1:
            clock.tick(999)#the fastest we can go, change to something reasonable, like 40-50 later

            for event in pygame.event.get():
                if event.type==QUIT:
                    self.state="QUIT"
                    return

                rightpanel.update(event)
                toppanel_unit.update(event)
                toppanel_house.update(event)

                if event.type==KEYDOWN:
                    if event.key==K_s:
                        pygame.image.save(self.screen, os.path.join("data", "screens",
                                            "screenie--%s.bmp"%time.strftime("%d-%m-%Y-%H-%M")))
                    elif event.key ==K_ESCAPE:
                        self.state="mainmenu"
                        return
                    elif event.key == K_f:
                        bottompanel.get("messages").add_message("fps: %s"%str(clock.get_fps()))

                    elif event.key == K_LEFT:
                        arrow_keys[0]=1
                    elif event.key == K_UP:
                        arrow_keys[1]=1
                    elif event.key == K_RIGHT:
                        arrow_keys[2]=1
                    elif event.key == K_DOWN:
                        arrow_keys[3]=1

                if event.type==KEYUP:
                    if event.key == K_LEFT:
                        arrow_keys[0]=0
                    elif event.key == K_UP:
                        arrow_keys[1]=0
                    elif event.key == K_RIGHT:
                        arrow_keys[2]=0
                    elif event.key == K_DOWN:
                        arrow_keys[3]=0
                    
                if event.type == MOUSEBUTTONDOWN:
                    if camera.rect.collidepoint(event.pos):
                        # test if one of the player's units or buildings was clicked
                        clicked_tile = camera.get_mouse_pos()

                        cx, cy = camera.convert_pos()

                        mx, my = event.pos
                        mx-=cx
                        my-=cy

                        mpos=(mx, my)
                            
                        # make the unit do something
                        # we really need to send unit what tile was clicked...
                        if event.button == 1:
                            gotit=False
                            for entity in player.armies+player.houses:
                                if entity.check_collision(mpos):
                                    player.active_entity = entity
                                    gotit=True
                                    selected_object=entity
                                    break
                            if not gotit:
                                player.active_entity=None
                                for city in cities.all:
                                    if city.check_collision(mpos):
                                        selected_object=city
                                        gotit=True
                            if not gotit:
                                player.active_entity=None
                                for enemy in enemies:
                                    for entity in enemy.armies+enemy.houses:
                                        if entity.check_collision(mpos):
                                            selected_object=entity
                                            gotit=True
                            if not gotit:
                                selected_object=None
                        if event.button == 3:
                            if player.active_entity:
                                player.active_entity.rightClick(clicked_tile)

            #lets handle the scenarios events...
            for event in scenario.events:
                trigger=False
                exec event.trigger
                if trigger:
                    exec event.event
                    scenario.events.remove(event)

            if rightpanel.get("quit").was_clicked:
                self.state="mainmenu"
                return

            if toppanel_house.get("make_unit").was_clicked:
                try:
                    valname=toppanel_house.get("captain_name").message
                    valtroops=int(toppanel_house.get("troops").message)
                    player.active_entity.make_unit(valname, valtroops)
                    player.active_entity=player.armies[-1]
                except:
                    pass
                toppanel_house.get("captain_name").message="Captain Name"
                toppanel_house.get("troops").message="50"
                toppanel_house.get("make_unit").was_clicked=False

            if toppanel_unit.get("recruit").was_clicked:
                gotone=None
                for city in cities.all:
                    if city.check_collision(player.active_entity):
                        gotone=city
                        break
                if gotone:
                    player.active_entity.goto=None
                    player.active_entity.action="recruit"
                    player.active_entity.recruit_city=gotone
                    player.active_entity=None
                    selected_object=gotone
                toppanel_unit.get("recruit").was_clicked=False

            if toppanel_unit.get("forage").was_clicked:
                player.active_entity.action="forage"
                player.active_entity.goto=None
                toppanel_unit.get("forage").was_clicked=False

            if toppanel_unit.get("loiter").was_clicked:
                player.active_entity.goto=None
                player.active_entity.action="loiter"
                player.active_entity.image_action="still"
                player.active_entity.image_on=0
                toppanel_unit.get("loiter").was_clicked=False

            if toppanel_unit.get("found_house").was_clicked:
                if len(player.armies)>1:
                    ok=True
                    for i in player.houses+cities.all:
                        if i.tile_pos==player.active_entity.tile_pos:
                            ok=False
                            break
                    if ok:
                        for i in enemies:
                            for x in i.houses:
                                if x.tile_pos==player.active_entity.tile_pos:
                                    ok=False
                                    break
                    if ok:
                        player.active_entity.make_house()
                        player.active_entity=None
                toppanel_unit.get("found_house").was_clicked=False

            if toppanel_house.get("increase_troops").am_clicked:
                try:
                    old=int(toppanel_house.get("troops").message)
                except:
                    old=50
                old+=1
                toppanel_house.get("troops").message=str(old)
            if toppanel_house.get("decrease_troops").am_clicked:
                try:
                    old=int(toppanel_house.get("troops").message)
                except:
                    old=50
                old-=1
                if old < 0:
                    old=0
                toppanel_house.get("troops").message=str(old)


            all_enemy=[]
            for i in enemies:
                for x in i.houses+i.armies:
                    all_enemy.append(x)
            all_player=player.armies+player.houses
            for i in all_enemy:
                for x in all_player:
                    if i.race==x.race:
                        pass
                    else:
                        if i.tile_pos==x.tile_pos and\
                           abs(i.offset[0]-x.offset[0]) < 0.25 and\
                           abs(i.offset[1]-x.offset[1]) < 0.25:
                            i.goto=None
                            x.goto=None
                            i.active_enemy=x
                            x.active_enemy=i


            #move the map
            mpos=pygame.mouse.get_pos()
            if mpos[0] < 3 or arrow_keys[0]:     #left
                camera.move([0.1, -0.1])
            if mpos[1] < 3 or arrow_keys[1]:     #up
                camera.move([0.1, 0.1])

            if mpos[0] > 637 or arrow_keys[2]:   #right
                camera.move([-0.1, 0.1])
            if mpos[1] > 477 or arrow_keys[3]:   #down
                camera.move([-0.1, -0.1])

            ##Update panel and buttons:
            if selected_object:
                if selected_object==player.active_entity:
                    unit=player.active_entity
                    if isinstance(unit, entities.Unit):
                        rightpanel.get("unit_name").message="captain: %s"%unit.captain_name
                        rightpanel.get("unit_name").refactor()

                        rightpanel.get("unit_captain_xp").message="captain xp: %s"%unit.captain_xp
                        rightpanel.get("unit_captain_xp").refactor()

                        rightpanel.get("unit_army_xp").message="army xp: %s"%unit.army_xp
                        rightpanel.get("unit_army_xp").refactor()

                        rightpanel.get("portrait").image=unit.image.all_images[0][0]

                        rightpanel.get("unit_soldiers").message="soldiers:\n"
                        for i in unit.soldier_type_counts:
                            rightpanel.get("unit_soldiers").message+="    %s: %s"%(i,
                                                        unit.soldier_type_counts[i])
                        rightpanel.get("unit_soldiers").refactor()

                        rightpanel.get("unit_attack").message="AV: %s"%unit.get_attack_value()
                        rightpanel.get("unit_attack").refactor()
                        rightpanel.get("unit_defense").message="DV: %s"%unit.get_defense_value()
                        rightpanel.get("unit_defense").refactor()
                        toppanel_unit.set_visible(True)
                        toppanel_house.set_visible(False)
                    else:
                        rightpanel.get("unit_name").message=""
                        rightpanel.get("unit_name").refactor()

                        rightpanel.get("unit_captain_xp").message=""
                        rightpanel.get("unit_captain_xp").refactor()

                        rightpanel.get("unit_army_xp").message=""
                        rightpanel.get("unit_army_xp").refactor()

                        rightpanel.get("portrait").image=unit.image

                        rightpanel.get("unit_soldiers").message="soldiers: %s"%unit.soldier_count
                        rightpanel.get("unit_soldiers").refactor()

                        rightpanel.get("unit_attack").message=""
                        rightpanel.get("unit_attack").refactor()
                        rightpanel.get("unit_defense").message=""
                        rightpanel.get("unit_defense").refactor()
                        toppanel_unit.set_visible(False)
                        toppanel_house.set_visible(True)
                else:
                    if isinstance(selected_object, entities.Unit):
                        unit=selected_object
                        rightpanel.get("unit_name").message="captain: %s"%unit.captain_name
                        rightpanel.get("unit_name").refactor()

                        rightpanel.get("unit_captain_xp").message="captain xp: %s"%unit.captain_xp
                        rightpanel.get("unit_captain_xp").refactor()

                        rightpanel.get("unit_army_xp").message="army xp: %s"%unit.army_xp
                        rightpanel.get("unit_army_xp").refactor()

                        rightpanel.get("portrait").image=unit.image.all_images[0][0]

                        rightpanel.get("unit_soldiers").message="soldiers:\n"
                        for i in unit.soldier_type_counts:
                            rightpanel.get("unit_soldiers").message+="    %s: %s"%(i,
                                                        unit.soldier_type_counts[i])
                        rightpanel.get("unit_soldiers").refactor()

                        rightpanel.get("unit_attack").message="AV: %s"%unit.get_attack_value()
                        rightpanel.get("unit_attack").refactor()
                        rightpanel.get("unit_defense").message="DV: %s"%unit.get_defense_value()
                        rightpanel.get("unit_defense").refactor()
                        toppanel_unit.set_visible(True)
                        toppanel_house.set_visible(False)
                    elif isinstance(selected_object, entities.House):
                        unit=selected_object
                        rightpanel.get("unit_name").message=""
                        rightpanel.get("unit_name").refactor()

                        rightpanel.get("unit_captain_xp").message=""
                        rightpanel.get("unit_captain_xp").refactor()

                        rightpanel.get("unit_army_xp").message=""
                        rightpanel.get("unit_army_xp").refactor()

                        rightpanel.get("portrait").image=unit.image

                        rightpanel.get("unit_soldiers").message="soldiers: %s"%unit.soldier_count
                        rightpanel.get("unit_soldiers").refactor()

                        rightpanel.get("unit_attack").message=""
                        rightpanel.get("unit_attack").refactor()
                        rightpanel.get("unit_defense").message=""
                        rightpanel.get("unit_defense").refactor()
                        toppanel_unit.set_visible(False)
                        toppanel_house.set_visible(True)
                    if isinstance(selected_object, entities.City):
                        rightpanel.get("unit_name").message="city name: %s"%selected_object.name
                        rightpanel.get("unit_name").refactor()

                        rightpanel.get("unit_captain_xp").message=""
                        rightpanel.get("unit_captain_xp").refactor()

                        rightpanel.get("unit_army_xp").message=""
                        rightpanel.get("unit_army_xp").refactor()

                        rightpanel.get("portrait").image=selected_object.image

                        rightpanel.get("unit_soldiers").message="population: %s"%\
                                                        selected_object.population
                        rightpanel.get("unit_soldiers").refactor()
                        rightpanel.get("unit_attack").message=""
                        rightpanel.get("unit_attack").refactor()
                        rightpanel.get("unit_defense").message=""
                        rightpanel.get("unit_defense").refactor()
                        toppanel_unit.set_visible(False)
                        toppanel_house.set_visible(False)
            else:
                rightpanel.get("unit_name").message=""
                rightpanel.get("unit_name").refactor()

                rightpanel.get("unit_captain_xp").message=""
                rightpanel.get("unit_captain_xp").refactor()

                rightpanel.get("unit_army_xp").message=""
                rightpanel.get("unit_army_xp").refactor()

                rightpanel.get("portrait").image=data['images']['blank']

                rightpanel.get("unit_soldiers").message=""
                rightpanel.get("unit_soldiers").refactor()
                rightpanel.get("unit_attack").message=""
                rightpanel.get("unit_attack").refactor()
                rightpanel.get("unit_defense").message=""
                rightpanel.get("unit_defense").refactor()
                toppanel_unit.set_visible(False)
                toppanel_house.set_visible(False)
            ##End Panel


            #clear the screen
            self.screen.fill((0,0,0,0))
            camera.render(self.screen, [player, cities]+enemies)
            player.update()
            for badGuy in enemies:
                badGuy.update()
                if 'ai' in dir(badGuy):
                    badGuy.ai.update()
            rightpanel.render(self.screen)
            rightpanel.get("info_food").message="food: %s"%player.food
            rightpanel.get("info_food").refactor()

            for i in cities.all:
                i.update()
                if i.dead:
                    cities.remove(i)
            
            bottompanel.render(self.screen)
            toppanel_unit.render(self.screen)
            toppanel_house.render(self.screen)
            pygame.display.flip()
