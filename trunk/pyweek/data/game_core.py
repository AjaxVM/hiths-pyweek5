
#load our assets
images['blank']=image.Image(pygame.Surface((5,5), SRCALPHA).convert_alpha())
images['blank'].surface.fill((0,0,0,0))

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
images['select']=image.load_image(path('images', 'misc', 'selected_unit.png'), alpha=True)


images['vampire_captain']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'vamp_captain.png'),
                                                           alpha=True),
                                                frame_delay=0.15)
images['vampire_elder']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'vamp_elder.png'),
                                                           alpha=True),
                                                frame_delay=0.15)

images['frostlen_captain']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'frostlen_captain.png'),
                                                           alpha=True),
                                                frame_delay=0.15)
images['frostlen_elder']=image.UnitAnimatedImage(image.load_image(path('images',
                                                                'units',
                                                                'frostlen_elder.png'),
                                                           alpha=True),
                                                frame_delay=0.15)

images['city/camp']=image.load_image(path('images', 'forts', 'human_camp.png'), alpha=True)
images['city/fortified']=image.load_image(path('images', 'forts', 'human_fort.png'), alpha=True)
images['city/settle']=image.load_image(path('images', 'forts', 'human_settlement.png'), alpha=True)

images['bubble/fight']=image.load_image(path('images', 'misc', 'bubble-fight.png'), alpha=True)
images['bubble/forage']=image.load_image(path('images', 'misc', 'bubble-forage.png'), alpha=True)
images['bubble/recruit']=image.load_image(path('images', 'misc', 'bubble-recruit.png'), alpha=True)
images['bubble/move']=image.load_image(path('images', 'misc', 'bubble-movement.png'), alpha=True)
images['bubbles']={"fight":images['bubble/fight'],
                   "forage":images['bubble/forage'],
                   "recruit":images['bubble/recruit'],
                   "loiter":images['blank'],
                   "move":images['bubble/move']}


images['map_bg_image']=None#image.load_surface(path('images', 'map_bg.bmp'))
#we really shouldn't use map_bg_image right now...

images['button']=image.load_image(path('images', 'gui', 'button.bmp'), -1)
images['buttonh']=image.load_image(path('images', 'gui', 'button_bright.bmp'), -1)
images['buttonc']=image.load_image(path('images', 'gui', 'button_dark.bmp'), -1)
images['mosaic_panel']=image.load_image(path('images', 'gui', 'mosaic_panel.bmp'))
images['cloth_panel']=image.load_image(path('images', 'gui', 'cloth_panel.bmp'))
images['input_box']=image.load_image(path('images', 'gui', 'input.bmp'), -1)
images['title']=image.load_image(path('images', 'gui', 'title.png'), -1)

music['darktheme']=path('music', 'darktheme.ogg')
music['kreuzzug']=path('music', 'kreuzzug.ogg')
music['monkses']=path('music', 'monkses.ogg')
music['mystery']=path('music', 'mystery.ogg')
music['peasantry']=path('music', 'peasantry.ogg')
music['warm_strings']=path('music', 'warm_strings.ogg')


sfx['blank']=Sound(None)#put your file name where None is, eg path('sfx', 'mysfx.wav')
sfx['click']=Sound(path('sfx', 'click.wav'))


#load our buildings
images['building/vamp_manor']=image.load_image(path('images', 'buildings',
                                                     'vamp_manor.png'),
                                                alpha=True)
images['building/frostlen_castle']=image.load_image(path('images', 'buildings',
                                                         'frostlen_castle.png'),
                                                    alpha=True)
images['building/coil_tower']=image.load_image(path('images', 'buildings',
                                                         'coil_tower.png'),
                                                    alpha=True)
images['building/lycan_fort']=image.load_image(path('images', 'buildings',
                                                         'lycan_fort.png'),
                                                    alpha=True)
images['building/lycan_lair']=image.load_image(path('images', 'buildings',
                                                         'lycan_lair.png'),
                                                    alpha=True)


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
