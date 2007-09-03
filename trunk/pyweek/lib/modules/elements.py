"""this is where the map/campaign/unit/race parser will reside

main calls methods in this, that will for now just return a
mock-up of races, units, soldier types, etc."""

import unit

"""
races will be layed out like this:
    __main_dir__/.../race.cfg
    |-> race_name
    |-> race_icon
    |-> good_vs -> a list of other races this race gets an
        advantage against
    |-> bad_vs -> opposite of good_vs(wait, no need for this)

    |->soldier_types -> [{attack, defense, speed, dodge, consumes},
                         {attack, etc.}, etc....]
"""
def load_race(filename):
    #return a mock-up race for now
    #will later call the parser function and generate a Race from the filename
    new=unit.Race()#this will set the race to default settings, ie - no images
    #also only 1 kind of troop, etc.
    return new

def get_std_races():
    #returns same as load_race, but a list of len 1 for now.
    #used to return all races in data/game_assets/races/
    return [load_race(None)]

def get_campaign_races(campaign_folder):
    #this will return all races in user_data/campaign_folder/races/
    #for now returns get_std_races()
    return get_std_races()


"""
glyphs will be layed out like this:
    __main_dir__/.../glyph.cfg
    |-> glyph_name
    |-> glyph_image
    |-> attack_boost, defense_boost, dodge_boost,
        speed_boost, food_production,
        troop_production
    |-> house_effect_multiplier -- should really be smaller than 1
        used to make a glyph stored at a house give a smaller boost, but
        it affects all units, whereas, if it is with a unit, the unit will
        get a bigger boost, but no other units will get a benefit
"""
def load_glyph(filename):
    return unit.Glyph()

def get_std_glyphs():
    return [load_glyph()]

def get_campaign_glyphs(campaign_folder):
    return get_std_glyphs()
