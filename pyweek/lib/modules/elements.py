from entities import *
import pygame
from pygame.locals import *
import pyglibs
from pyglibs import *
from assets import *

def path(*f):
    return os.path.join('data', *f)

def load_file(filename):
    a=open(filename, 'rU').read()
    world=None#the isometric.World or decendant of one
    camera_pos=[0,0]#the isometric.camera
    races=[]#these are any races found in the file
    players=[]#players
    glyphs=[]#glyphs
    ground_glyphs=[]#glyphs that are placed
    glyph_spawn_rate=0#how quickly new glyphs are created
    cities=[]#human cities
    fortifications=[]#placed forts
    monster_spawn_points=[]#this is where nasties apwn when oyu pick up a glyph!
    maps={}#any maps found in the file
    ancient_temples=[]#this is where teh Rendth spawn from
    campaigns=[]#any campaigns found in this file
    terrain={}#the terrain types found in this file
    images={}
    music={}
    sfx={}
    exec a
    return {'world':world,
            'camera_pos':camera_pos,
            'races':races,
            'players':players,
            'glyphs':glyphs,
            'ground_glyphs':ground_glyphs,
            'glyph_spawn_rate':glyph_spawn_rate,
            'cities':cities,
            'ms_points':monster_spawn_points,
            'map':map,
            'forts':fortifications,
            'terrain':terrains,
            'temples':ancient_temples,
            'campaigns':campaigns,
            'images':images,
            'music':music,
            'sfx':sfx}
