import time
from pyglibs import isometric

def spc_div(a, b):
    if a and b:
        return a/b
    return 0

class Race(object):
    def __init__(self, name="None",
                 captain_image=None,
                 elder_image=None,
                 house_image=None,
                 soldier_types={},
                 start_troops=100,
                 start_food=100,
                 house_food_production=1,#seconds
                 house_troop_production_speed=5):#seconds
        self.name=name

        self.captain_image=captain_image
        self.elder_image=elder_image
        self.house_image=house_image

        self.soldier_types=soldier_types
        self.soldier_types["Recruit"]= {"speed":1,
                                        "attack":1,
                                        "defense":1,
                                        "dodge":1,
                                        "consumes":1}

        self.start_troops=start_troops
        self.start_food=start_food

        self.house_food_prod=house_food_production
        self.house_troop_prod=house_troop_production

class Unit(isometric.Unit):
    def __init__(self, iso_world, player,
                 captain_name="No-name",
                 captain_is_elder=False,
                 captain_xp=0, army_xp=0,
                 soldier_type_counts={},
                 pos=[0,0]):

        if captain_is_elder:
            cap_image=race.elder_image
        else:
            cap_image=race.captain_image

        isometric.Unit.__init__(self, iso_world, cap_image,
                                pos)

        self.captain_name=captain_name

        self.iso_world=iso_world
        self.player=player
        self.race=player.race

        self.captain_is_elder=captain_is_elder

        self.captain_xp=captain_xp
        self.army_xp=army_xp

        self.soldier_type_counts=soldier_type_counts

        self.glyphs=[]

    def get_consumption(self):
        con=0
        for i in self.soldier_type_counts:
            con+=i["consumes"]*self.soldier_type_counts[i]
        return con

    def get_glyph_by_name(self, name):
        for i in self.glyphs:
            if i.name==name:
                return i

    def transport_glyph(self, glyph_group, glyph_name, pos=[0,0]):
        a=self.get_glyph_by_name(glyph_name)
        glyph_group.append(GlyphGround(self.iso_world, a, pos))
        self.glyphs.remove(a)

    def make_army(self, captain_name="None", soldier_counts={}):
        for i in soldier_counts:
            if i in self.soldier_type_count:
                if soldier_counts[i]>self.soldier_type_counts[i]:
                    soldier_counts[i]=self.soldier_type_counts[i]
                self.soldier_type_counts[i]-=soldier_counts[i]
            else:
                del soldier_counts[i]
        a = Unit(self.iso_world, self.player, captain_name,
                 False, int(spc_div(self.army_xp,2)),
                 int(spc_div(self.army_xp,2)),
                 soldier_counts, self.tile_pos)
        self.player.armies.append(a)

    def make_house(self):
        self.player.armies.remove(self)
        self.player.to_be_deleted.append(self)

        new=House(self.iso_world, self.player, self.pos)
        new.soldier_type_count=self.soldier_type_count
        new.glyphs=self.glyphs
        new.leader_placed=True

        self.player.houses.append(new)

class House(isometric.Unit):
    def __init__(self, iso_world, player, pos=[0,0]):

        isometric.Unit.__init__(self, iso_world, race.house_image, pos)

        self.iso_world=iso_world
        self.player=player
        self.race=player.race

        self.troops=int(race.start_troops)

        self.food_counter=time.time()
        self.troop_counter=time.time()

        self.leader_placed=False

        self.soldier_type_count={"Recruit":self.race.start_troops}

        self.glyphs=[]

    def get_glyph_by_name(self, name):
        for i in self.glyphs:
            if i.name==name:
                return i

    def make_unit(self, captain_name="None", soldier_counts={}):
        for i in soldier_counts:
            if i in self.soldier_type_count:
                if soldier_counts[i]>self.soldier_type_counts[i]:
                    soldier_counts[i]=self.soldier_type_counts[i]
                self.soldier_type_counts[i]-=soldier_counts[i]
            else:
                del soldier_counts[i]
        a = Unit(self.iso_world, self.player, captain_name,
                 not self.leader_placed, 0, 0,
                 soldier_counts, self.tile_pos)
        self.leader_placed=True
        self.player.armies.append(a)

    def update(self):
        if time.time()-self.food_counter >= self.race.house_food_prod:
            self.player.food+=1
            self.food_counter=time.time()

        if time.time()-self.troop_counter >= self.race.house_troop_prod:
            self.soldier_type_count["Recruit"]+=1
            self.troop_counter=time.time()

class Player(object):
    def __init__(self, name=None, race=None):
        self.name=name

        self.race=race

        self.houses=[]
        self.armies=[]
        self.to_be_deleted=[]

        self.food=int(race.start_food)
        self.food_counter=time.time()

    def create_house(self, iso_world, pos=[0,0]):
        self.houses.append(House(iso_world, self, pos))

    def flush(self):
        for i in self.to_be_deleted:
            self.to_be_deleted.remove(i)
            del i

    def update(self):
        self.flush()
        for i in self.houses:
            i.update()
        if time.time()-self.food_counter>=self.race.house_food_prod:
            for i in self.armies:
                self.food-=i.get_consumption()
            self.food_counter=time.time()

class Glyph(object):
    def __init__(self, attack_boost=0, defense_boost=0,
                 dodge_boost=0, speed_boost=0,
                 consumption_reduction=0,
                 food_production=0, troop_production=0,
                 name="None", image=None):
        self.name=name
        self.image=image

        self.attack_boost=attack_boost
        self.defense_boost=defense_boost
        self.dodge_boost=dodge_boost
        self.speed_boost=speed_boost

        self.consumption_reduction=consumption_reduction
        self.food_production=food_production
        self.troop_production=troop_production

class GlyphGround(isometric.Unit):
    def __init__(self, iso_world, glyph, pos=[0,0]):
        isometric.Unit.__init__(self, iso_world, glyph.image, pos)

        self.glyph=glyph

    def pickup(self, unit):
        unit.glyphs.append(self.glyph)
        del self
        
        
        
