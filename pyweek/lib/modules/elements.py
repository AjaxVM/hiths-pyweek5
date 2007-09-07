import os

import pygame
from pygame.locals import *

from entities import *
import pyglibs
from pyglibs import *
from assets import *

def path(*f):
    a=os.path.join('data', *f)
    if os.path.isfile(a):return a
    a=os.path.join('data', 'campaigns', *f)
    if os.path.isfile(a):return a
    raise AttributeError, "File '%s' not found"%str(f)

def load_file(filename, other=None):
    a=open(filename, 'rU').read()
    if other:
        world=other['world']#the isometric.World or decendant of one
        camera_pos=other['camera_pos']#the isometric.camera
        races=other['races']#these are any races found in the file
        glyphs=other['glyphs']#glyphs
        ground_glyphs=other['ground_glyphs']#glyphs that are placed
        glyph_spawn_rate=other['glyph_spawn_rate']#how quickly new glyphs are created
        fortifications=other['forts']#placed forts
        maps=other['maps']#any maps found in the file
        campaigns=other['campaigns']#any campaigns found in this file
        terrain=other['terrain']#the terrain types found in this file
        images=other['images']
        music=other['music']
        sfx=other['sfx']
    else:
        world=None#the isometric.World or decendant of one
        camera_pos=[0,0]#the isometric.camera
        races={}#these are any races found in the file
        glyphs=[]#glyphs
        ground_glyphs=[]#glyphs that are placed
        glyph_spawn_rate=0#how quickly new glyphs are created
        fortifications=[]#placed forts
        maps={}#any maps found in the file
        campaigns={}#any campaigns found in this file
        terrain={}#the terrain types found in this file
        images={}
        music={}
        sfx={}
    exec a
    return {'world':world,
            'camera_pos':camera_pos,
            'races':races,
            'glyphs':glyphs,
            'ground_glyphs':ground_glyphs,
            'glyph_spawn_rate':glyph_spawn_rate,
            'maps':maps,
            'forts':fortifications,
            'terrain':terrain,
            'campaigns':campaigns,
            'images':images,
            'music':music,
            'sfx':sfx}
