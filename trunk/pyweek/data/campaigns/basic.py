#create basic map
##import random
##maps['default']=[]
##for y in range(50):
##    maps['default'].append([])
##    for x in range(50):
##        maps['default'][y].append(random.choice(["d", "g", "l", "s"]))


maps['default']=load_map(path('maps','theroad.py'))

#basic isometric world: a campaign can specify a new Two,
#or it can create a new class that inherets from World, that
#way they have access to every element of the engine :D
world=isometric.World(map=maps['default'],
                      tiles=terrain,
                      tile_size=[100, 50])

#the starting camera pos, change this to where you place
#the players first house, or to where you want them to start
camera_pos=[-10,-10]


#create basic race and other datas :)
#any of these things can be left blank, but it is recommended that you fill them ;)
races['default']=Race(name="default",#name and race['name'] should be the same
                      captain_image=images['coil_captain'],#the image for a unit that doesnt have your elder
                      elder_image=images['coil_elder'],#the image for your elder unit
                      house_image=images['building/coil_tower'],
                      soldier_types={"Shock":{"speed":1,
                                              "attack":2,
                                              "defense":1,
                                              "dodge":1,
                                              'consumes':1}},
                      flag_image=images['flag'],
                      select_image=images['select'],
                      bubbles=images['bubbles'],
                      start_troops=100,
                      start_food=100,
                      house_food_production=2,#amount per 5 seconds
                      house_troop_production=10)#seconds

# and a race for the baddies
races['frostlen']=Race(name="frostlen",#name and race['name'] should be the same
                      captain_image=images['frostlen_captain'],#the image for a unit that doesnt have your elder
                      elder_image=images['frostlen_elder'],#the image for your elder unit
                      house_image=images['building/frostlen_castle'],
                      soldier_types={"Shock":{"speed":1,
                                              "attack":1,
                                              "defense":1,
                                              "dodge":1,
                                              'consumes':1}},
                      flag_image=images['flag'],
                      select_image=images['select'],
                      bubbles=images['bubbles'],
                      start_troops=75,
                      start_food=75,
                      house_food_production=2,#amount per 5 seconds
                      house_troop_production=10)#seconds

races['vampire']=Race(name="vampire",#name and race['name'] should be the same
                      captain_image=images['vampire_captain'],#the image for a unit that doesnt have your elder
                      elder_image=images['vampire_elder'],#the image for your elder unit
                      house_image=images['building/lycan_lair'],
                      soldier_types={"Shock":{"speed":1,
                                              "attack":1,
                                              "defense":1,
                                              "dodge":1,
                                              'consumes':1}},
                      flag_image=images['flag'],
                      select_image=images['select'],
                      bubbles=images['bubbles'],
                      start_troops=65,
                      start_food=65,
                      house_food_production=2,#amount per 5 seconds
                      house_troop_production=10)#seconds
          
#the campaign stuff, which includes actually creating players and stuff will
#go here later, for now just make the races ;)


new_campaign=Campaign(name="basic")

thePlayer = Player("jimbob", races['default'], color=[125,0,175,255])
thePlayer.create_house(world, [11,9])
thePlayer.create_house(world, [12,11])
thePlayer.houses[0].make_unit("bob II", 50)
thePlayer.houses[1].make_unit("bob III", 50)

badGuyOne = Player("evilDoer", races['frostlen'])
badGuyOne.create_house(world, [8,16])
badGuyOne.create_house(world, [20,25])
badGuyOne.houses[0].make_unit("Evil Minion",65)
badGuyOne.houses[1].make_unit("Bad Mr. Frosty",15)
badGuyOne.houses[1].make_unit("Mr. Snow-Evils",15)
badGuyOne.armies[0].goto = [11,9]

badGuyTwo = Player("vampy", races['vampire'])
badGuyTwo.create_house(world, [20,8])
badGuyTwo.houses[0].make_unit("Vampireguy",65)
badGuyTwo.ai = ChaserAI(badGuyTwo,enemies=[thePlayer, badGuyOne])

badGuyOne.ai = ChaserAI(badGuyOne,enemies=[badGuyTwo])

event1_trigger = """if player.active_entity and not player.active_entity.tile_pos==[0,0]:trigger=True"""
event1_event = "bottompanel.get('messages').add_message('You moved your unit! Great Job!')"
event1 = Event(trigger = event1_trigger, event = event1_event)

scenario1=Scenario(name="scenario1", events=[event1], player=thePlayer, enemies = [badGuyOne, badGuyTwo])

scenario1.cities=[]
scenario1.cities.append(City(world, 'Hello', 150,
                             images['city/camp'],
                             [2,1]))

new_campaign.scenarios['scenario1']=scenario1
new_campaign.start_scenario='scenario1'
new_campaign.current_scenario=scenario1

campaigns['default']=new_campaign
