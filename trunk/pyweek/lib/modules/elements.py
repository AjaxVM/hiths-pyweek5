from unit import *

def load_file(filename):
    a=open(filename, 'rU').read()
    races=[]
    units=[]
    houses=[]
    players=[]
    glyphs=[]
    ground_glyphs=[]
    exec a
    return {'races':races,
            'units':units,
            'houses':houses,
            'players':players,
            'glyphs':glyphs,
            'ground_glyphs':ground_glyphs}
