
#load our assets
images['tile/dirt']=image.load_image(path('images', 'tiles', 'dirt.bmp'), -1)
images['tile/grass']=image.load_image(path('images', 'tiles', 'grass.bmp'), -1)
images['tile/lava']=image.load_image(path('images', 'tiles', 'lava.bmp'), -1)
images['tile/snow']=image.load_image(path('images', 'tiles', 'snow.bmp'), -1)

images['coil_captain']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'coil_captain.png'),
                                                           alpha=True),
                                                frame_delay=0.15)
images['coil_elder']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'coil_elder.png'),
                                                           alpha=True),
                                                frame_delay=0.15)


images['flag']=image.load_image(path('images', 'misc', 'flag.png'), alpha=True)


images['vampire_captain']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'vamp_captain.png'),
                                                           alpha=True),
                                                frame_delay=0.05)

images['frostlen_captain']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'frostlen_captain.png'),
                                                           alpha=True),
                                                frame_delay=0.05)

images['city/camp']=image.load_image(path('images', 'forts', 'human_camp.png'), alpha=True)
images['city/fortified']=image.load_image(path('images', 'forts', 'human_fort.png'), alpha=True)
images['city/settle']=image.load_image(path('images', 'forts', 'human_settlement.png'), alpha=True)

images['blank']=image.Image(pygame.Surface((5,5), SRCALPHA).convert_alpha())


images['map_bg_image']=None#image.load_surface(path('images', 'map_bg.bmp'))
#we really shouldn't use map_bg_image right now...

images['button']=image.load_image(path('images', 'gui', 'button.bmp'), -1)
images['buttonh']=image.load_image(path('images', 'gui', 'button_bright.bmp'), -1)
images['buttonc']=image.load_image(path('images', 'gui', 'button_dark.bmp'), -1)
images['mosaic_panel']=image.load_image(path('images', 'gui', 'mosaic_panel.bmp'))
images['cloth_panel']=image.load_image(path('images', 'gui', 'cloth_panel.bmp'))
images['input_box']=image.load_image(path('images', 'gui', 'input.bmp'), -1)

music['darktheme']=path('music', 'darktheme.ogg')
music['kreuzzug']=path('music', 'kreuzzug.ogg')
music['monkses']=path('music', 'monkses.ogg')
music['mystery']=path('music', 'mystery.ogg')
music['peasantry']=path('music', 'peasantry.ogg')
music['warm_strings']=path('music', 'warm_strings.ogg')


sfx['blank']=Sound(None)#put your file name where None is, eg path('sfx', 'mysfx.wav')
sfx['click']=Sound(path('sfx', 'click.wav'))


#create basic terrain
terrain['d']=images['tile/dirt']
terrain['g']=images['tile/grass']
terrain['l']=images['tile/lava']
terrain['s']=images['tile/snow']


#create basic map
import random
maps['default']=[]
for y in range(50):
    maps['default'].append([])
    for x in range(50):
        maps['default'][y].append(random.choice(["d", "g"]))

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
                      captain_image=images['coil_elder'],#the image for a unit that doesnt have your elder
                      elder_image=images['coil_captain'],#the image for your elder unit
                      house_image=images['button'],
                      soldier_types={"Shock":{"speed":1,#speed of unit, number is divided by 100 later
                                              "attack":1,
                                              "defense":1,
                                              "dodge":1,
                                              'consumes':1}},
                      flag_image=images['flag'],
                      start_troops=100,
                      start_food=100,
                      house_food_production=2,#amount per 5 seconds
                      house_troop_production=10)#seconds


          
#the campaign stuff, which includes actually creating players and stuff will
#go here later, for now just make the races ;)
