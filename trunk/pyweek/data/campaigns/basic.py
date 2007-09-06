
#load our assets
images['building/vamp_castle']=image.load_image(path('images', 'buildings', 'vamp_castle1.bmp'), -1)


#create basic map
import random
maps['default']=[]
for y in range(50):
    maps['default'].append([])
    for x in range(50):
        maps['default'][y].append(random.choice(["r", "g"]))

#basic isometric world: a campaign can specify a new one,
#or it can create a new class that inherets from World, that
#way they have access to every element of the engine :D
world=isometric.World(map=maps['default'],
                      tiles=terrain,
                      tile_size=[100, 50])

#the starting camera pos, change this to where you place
#the players first house, or to where you want them to start
camera_pos=[0,0]


#create basic race and other datas :)
#any of these things can be left blank, but it is recommended that you fill them ;)
races['default']=Race(name="default",#name and race['name'] should be the same
                      captain_image=images['player_mockup'],#the image for a unit that doesnt have your elder
                      elder_image=images['player_mockup'],#the image for your elder unit
                      house_image=images['building/vamp_castle'],
                      soldier_types={"Shock":{"speed":1,
                                              "attack":1,
                                              "defense":1,
                                              "dodge":1,
                                              'consumes':1}},#this will also create a basic Recruit
                                                             #soldier type, this is hte default and cannot
                                                             #be changed!
                      start_troops=100,
                      start_food=100,
                      house_food_production=2,#amount per 5 seconds
                      house_troop_production=10)#seconds


          
#the campaign stuff, which includes actually creating players and stuff will
#go here later, for now just make the races ;)


new_campaign=Campaign(name="basic")
scenario1=Scenario(name="scenario1",
                   events=[Event(trigger="if not player.active_entity.tile_pos==[0,0]:trigger=True",
                        event="bottompanel.get('messages').add_message('you moved your unit!')")],
                   player=Player("jimbob", races['default']))
scenario1.player.create_house(world, [0,0])
scenario1.player.houses[0].make_unit("bob II", {"Recruit":50})
scenario1.player.active_entity = scenario1.player.armies[0]

new_campaign.scenarios['scenario1']=scenario1
new_campaign.start_scenario='scenario1'
new_campaign.current_scenario=scenario1

campaigns['default']=new_campaign
