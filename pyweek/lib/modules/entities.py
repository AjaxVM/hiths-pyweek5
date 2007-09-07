import time, random
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
                 house_troop_production=5):#seconds
        self.name=name

        self.captain_image=captain_image
        self.elder_image=elder_image
        self.house_image=house_image

        self.soldier_types=soldier_types

        self.start_troops=start_troops
        self.start_food=start_food

        self.house_food_prod=house_food_production
        self.house_troop_prod=house_troop_production

class Selectable(object):
    def rightClick(self, tile_position):
        pass

    def leftClick(self, tile_position):
        pass
    

class Unit(isometric.Unit, Selectable):
    def __init__(self, iso_world, player,
                 captain_name="No-name",
                 captain_is_elder=False,
                 captain_xp=0, army_xp=0,
                 soldier_type_counts={},
                 pos=[0,0]):

        if captain_is_elder:
            cap_image=player.race.elder_image
        else:
            cap_image=player.race.captain_image

        isometric.Unit.__init__(self, iso_world, cap_image,
                                pos)

        self.render_priority=3

        self.captain_name=captain_name

        self.iso_world=iso_world
        self.player=player
        self.race=player.race

        self.captain_is_elder=captain_is_elder

        self.captain_xp=captain_xp
        self.army_xp=army_xp

        self.soldier_type_counts=soldier_type_counts

        self.glyphs=[]

        self.getting_food=False
        self.food_counter=0

        self.goto=None

    def get_troop_count(self):
        c=0
        for i in self.soldier_type_counts:
            c+=self.soldier_type_counts[i]
        return c

    def get_consumption(self):
        con=0
        for i in self.soldier_type_counts:
            con+=self.race.soldier_types[i]["consumes"]*\
                  self.soldier_type_counts[i]
        return spc_div(con, 100)

    def get_glyph_by_name(self, name):
        for i in self.glyphs:
            if i.name==name:
                return i

    def get_food(self):
        self.food_counter=time.time()
        self.getting_food=True

    def transport_glyph(self, glyph_group, glyph_name, pos=[0,0]):
        a=self.get_glyph_by_name(glyph_name)
        glyph_group.append(GlyphGround(self.iso_world, a, pos))
        self.glyphs.remove(a)

    def make_army(self, captain_name="None", num_troops=10):
        soldier_type_counts={}
        tot_troops=0

        for i in self.soldier_type_counts:
            new_num = random.randint(0, num_troops-tot_troops)
            if self.soldier_type_counts[i]>=new_num:
                pass
            else:
                new_num=self.soldier_type_counts[i]
            soldier_type_counts[i]=new_num
            self.soldier_type_counts[i]-=new_num
            tot_troops+=new_num
        if tot_troops < num_troops:
            choice=random.choice(list(self.soldier_type_counts))
            new_num=num_troops-tot_troops
            if new_num > self.soldier_type_counts[choice]:
                new_num=self.soldier_type_counts[choice]
            soldier_type_counts[i]+=new_num
            self.soldier_type_counts[i]-=new_num

        a = Unit(self.iso_world, self.player, captain_name,
                 False, int(spc_div(self.army_xp,2)),
                 int(spc_div(self.army_xp,2)),
                 soldier_type_counts, self.tile_pos)
        a.move([0.5, 0.5])
        self.player.armies.append(a)

    def make_house(self):
        self.player.armies.remove(self)
        self.player.to_be_deleted.append(self)

        new=House(self.iso_world, self.player, self.tile_pos)
        new.move([0.5, 0.5])
        new.soldier_type_count=self.soldier_type_count
        new.glyphs=self.glyphs
        new.leader_placed=True

        self.player.houses.append(new)

    def get_speed(self):
        speed=0
        num=0
        for i in self.soldier_type_counts:
            speed+=self.race.soldier_types[i]['speed']*self.soldier_type_counts[i]
            num+=self.soldier_type_counts[i]
        speed=float(speed)/100
        return spc_div(speed, num)

    def update(self):
        if self.getting_food:
            if time.time()-self.food_counter==1:
                self.player.food+=int(0.25*self.get_troop_count())

        spd=self.get_speed()
        if self.goto==self.tile_pos:
            self.goto=None

        if not self.goto:
            if self.offset[0]==0.5 and self.offset[1]==0.5:
                self.image.action="still"
                self.image.on=0
            else:
                self.image.action="moving"
        else:
            self.image.action="moving"

        if self.goto:
            if self.goto[0]<self.tile_pos[0]:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((-spd, -spd))
                    self.image.direction="topleft"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((-spd, spd))
                    self.image.direction="bottomleft"
                else:
                    self.move((-spd, 0))
                    self.image.direction="left"
            elif self.goto[0]>self.tile_pos[0]:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((spd, -spd))
                    self.image.direction="topright"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((spd, spd))
                    self.image.direction="bottomright"
                else:
                    self.move((spd, 0))
                    self.image.direction="right"
            else:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((0, -spd))
                    self.image.direction="top"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((0, spd))
                    self.image.direction="bottom"
                else:
                    pass#I mean come on!, why should this ever happen? :P

        else:
            if not self.offset[0]==0.5:
                if abs(self.offset[0]-0.5) < spd:
                    self.offset[0]=0.5
                else:
                    if self.offset[0]<0.5:
                        self.move((spd, 0))
                    elif self.offset[0]>0.5:
                        self.move((-spd, 0))
            if not self.offset[1]==0.5:
                if abs(self.offset[1]-0.5) < spd:
                    self.offset[1]=0.5
                else:
                    if self.offset[1]<0.5:
                        self.move((0, spd))
                    elif self.offset[1]>0.5:
                        self.move((0, -spd))

    def train_unit(self, amount, to_type):
        if to_type in self.soldier_type_counts:
            if amount <= self.soldier_type_counts["Recruit"]:
                self.soldier_type_counts["Recruit"]-=amount
            else:
                amount=self.soldier_type_counts["Recruit"]
                self.soldier_type_counts["Recruit"]=0
            self.soldier_type_counts[to_type]+=amount
    
    def rightClick(self, tile_position):
        if tile_position:self.goto=tile_position

class House(isometric.Unit, Selectable):
    def __init__(self, iso_world, player, pos=[0,0]):

        isometric.Unit.__init__(self, iso_world,
                                player.race.house_image,
                                pos)

        self.iso_world=iso_world
        self.player=player
        self.race=player.race

        self.troops=int(self.race.start_troops)

        self.food_counter=time.time()
        self.troop_counter=time.time()

        self.leader_placed=False

        self.soldier_count=self.race.start_troops

        self.glyphs=[]

    def get_glyph_by_name(self, name):
        for i in self.glyphs:
            if i.name==name:
                return i

    def make_unit(self, captain_name="None",num_troops=10):
        soldier_type_counts={}
        tot_troops=0

        for i in self.race.soldier_types:
            new_num = random.randint(0, num_troops-tot_troops)
            if self.soldier_count>=new_num:
                pass
            else:
                new_num=self.soldier_count
            soldier_type_counts[i]=new_num
            self.soldier_count-=new_num
            tot_troops+=new_num
        if tot_troops < num_troops:
            choice=random.choice(list(self.race.soldier_types))
            new_num=num_troops-tot_troops
            if new_num > self.soldier_count:
                new_num=self.soldier_count
            soldier_type_counts[i]+=new_num
            self.soldier_count-=new_num


        a = Unit(self.iso_world, self.player, captain_name,
                 not self.leader_placed, 0, 0,
                 soldier_type_counts, self.tile_pos)
        a.move([0.5, 0.5])
        self.leader_placed=True
        self.player.armies.append(a)

    def update(self):
        if time.time()-self.food_counter >= 5:
            self.player.food+=self.race.house_food_prod
            self.food_counter=time.time()

        if time.time()-self.troop_counter >= self.race.house_troop_prod:
            self.soldier_count+=1
            self.troop_counter=time.time()

class Player(isometric.UnitContainer):
    def __init__(self, name=None, race=None):
        self.name=name

        self.race=race

        self.houses=[]
        self.armies=[]
        self.to_be_deleted=[]

        self.food=int(race.start_food)
        self.food_counter=time.time()
        self.active_entity = None

    def create_house(self, iso_world, pos=[0,0]):
        a=House(iso_world, self, pos)
        a.move([0.5, 0.5])
        self.houses.append(a)
        return a

    def flush(self):
        for i in self.to_be_deleted:
            self.to_be_deleted.remove(i)
            del i

    def update(self):
        self.flush()
        for i in self.houses:
            i.update()
        for i in self.armies:
            i.update()
        if time.time()-self.food_counter>=5:
            for i in self.armies:
                self.food-=i.get_consumption()
            self.food_counter=time.time()

    def get_units_in_area(self, rect):
        cur=[]
        for i in self.armies+self.houses:
            if rect.colliderect(i.rect):
                cur.append(i)
        return cur

class Glyph(object):
    def __init__(self, attack_boost=0, defense_boost=0,
                 dodge_boost=0, speed_boost=0,
                 food_production=0, troop_production=0,
                 name="None", image=None):
        self.name=name
        self.image=image

        self.attack_boost=attack_boost
        self.defense_boost=defense_boost
        self.dodge_boost=dodge_boost
        self.speed_boost=speed_boost

        self.food_production=food_production
        self.troop_production=troop_production

class GlyphGround(isometric.Unit):
    def __init__(self, iso_world, glyph, pos=[0,0]):
        isometric.Unit.__init__(self, iso_world, glyph.image, pos)

        self.glyph=glyph

    def pickup(self, unit):
        unit.glyphs.append(self.glyph)
        del self

class FortificationType(object):
    def __init__(self, attack_boost=0, defense_boost=0,
                 image=None, name="None"):
        self.name=name
        self.image=image

        self.attack_boost=attack_boost
        self.defense_boost=defense_boost

class Fortification(isometric.Unit):
    def __init__(self, iso_world, fort, pos=[0,0]):
        isometric.Unit.__init__(self, iso_world, fort.image, pos)

        self.rect.center=tuple(self.pos)

        self.fort=fort

class City(isometric.Unit):
    def __init__(self, iso_world, name="None", population=100,
                 defences=100, image=None, pos=[0,0]):

        isometric.Unit.__init__(self, iso_world, image, pos)

        self.name=name
        self.population=population
        self.defences=defences

        self.render_priority=1

        self.counter=time.time()

    def update(self):
        if time.time()-self.counter > 1:
            self.population+=(((self.population/2)/2)/10)
            self.counter=time.time()

class Campaign(object):
    def __init__(self, name="Noname",
                 scenarios={}, start_scenario=None):
        self.name=name

        self.scenarios=scenarios
        self.start_scenario=start_scenario

        if start_scenario:
            self.current_scenario=self.scenarios[self.start_scenario]
        else:
            self.current_scenario=None

class Event(object):
    def __init__(self, trigger, event):
        self.trigger=trigger
        self.event=event

class Scenario(object):
    def __init__(self, name="Noname",
                 events=[], player=None,
                 enemies=None, map=None,
                 next_scenario=None,
                 cities=[], glyphs=[],
                 random_glyph_speed=None,#turns this feature off at None
                 random_city_speed=None):#turns feature off at None
        self.name=name

        self.events=events

        self.player=player
        self.enemies=enemies

        self.map=map
        self.next_scenario=next_scenario

        self.cities=cities
        self.glyphs=glyphs

        self.random_glyph_speed=random_glyph_speed
        self.random_city_speed=random_city_speed
        
        
