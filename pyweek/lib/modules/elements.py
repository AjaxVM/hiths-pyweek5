from unit import *
import pygame
from pygame.locals import *
import pyglibs

def load_file(filename, iso_world):
    a=open(filename, 'rU').read()
    races=[]#these are any races found in the file
    units=[]#these are units from file
    houses=[]#houses
    players=[]#players
    glyphs=[]#glyphs
    ground_glyphs=[]#glyphs that are placed
    glyph_spawn_rate=0#how quickly new glyphs are created
    cities=[]#human cities
    fortifications=[]#placed forts
    monster_spawn_points=[]#this is where nasties apwn when oyu pick up a glyph!
    map=None#any maps found in the file
    ancient_temples=[]#this is where teh Rendth spawn from
    campaigns=[]#any campaigns found in this file
    terrains={}#the terrain types found in this file
    exec a
    return {'races':races,
            'units':units,
            'houses':houses,
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
            'campaigns':campaigns}
