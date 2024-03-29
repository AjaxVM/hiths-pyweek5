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
                 flag_image=None,
                 select_image=None,
                 bubbles={},
                 house_food_production=1,#seconds
                 house_troop_production=5):#seconds
        self.name=name

        self.captain_image=captain_image
        self.elder_image=elder_image
        self.house_image=house_image

        self.soldier_types=soldier_types

        self.flag_image=flag_image
        self.select_image=select_image
        self.bubbles=bubbles

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

        self.active_enemy=None

        self.getting_food=False
        self.food_counter=0

        self.goto=None

        self.image_action="still"
        self.image_on=0
        self.image_direction="bottom"
        self.image_last_time=time.time()


        self.action='loiter'#can be loiter, recruit, attack, forage, or move

        self.recruit_city=None
        self.recruit_counter=time.time()
        self.forage_counter=time.time()

        self.dead=False
        self.attack_counter=time.time()

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

    def get_attack_value(self):
        val=0
        for i in self.soldier_type_counts:
            val+=self.race.soldier_types[i]["attack"]*\
                self.soldier_type_counts[i]
        if self.captain_is_elder:
            val=int(val*1.5)
        return val

    def get_defense_value(self):
        val=0
        for i in self.soldier_type_counts:
            val+=self.race.soldier_types[i]["speed"]*\
                self.soldier_type_counts[i]
        return val

    def get_dodge_value(self):
        val=0
        for i in self.soldier_type_counts:
            val+=self.race.soldier_types[i]["dodge"]*\
                self.soldier_type_counts[i]
        return val

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

    def make_house(self):
        self.player.armies.remove(self)
        self.player.to_be_deleted.append(self)
        self.dead=True

        new=House(self.iso_world, self.player, self.tile_pos)
        new.soldier_count=self.get_num_troops()
        new.glyphs=self.glyphs
        new.leader_placed=True

        self.player.houses.append(new)

    def get_num_troops(self):
        soldiers=0
        for i in self.soldier_type_counts:
            soldiers+=self.soldier_type_counts[i]
        return soldiers

    def get_speed(self):
        speed=0
        num=0
        for i in self.soldier_type_counts:
            speed+=self.race.soldier_types[i]['speed']*self.soldier_type_counts[i]
            num+=self.soldier_type_counts[i]
        speed=float(speed)/100
        return spc_div(speed, num)

    def render(self, surface, camera_pos=[0,0]):
        if time.time()-self.image_last_time>self.image.frame_delay:
            self.image_last_time=time.time()
            self.image_on+=1
            if self.image_on>=len(self.image.actions[self.image_action]):
                self.image_on=0
        self.image.on=self.image_on
        self.image.direction=self.image_direction
        self.image.action=self.image_action
        x, y=self.rect.topleft
        x+=camera_pos[0]
        y+=camera_pos[1]
        if self.player.active_entity==self:
            self.player.select_image.render(surface, (x, y))
        if self.action in self.race.bubbles:
            self.race.bubbles[self.action].render(surface, (x, y-20))
        isometric.Unit.render(self, surface, camera_pos)
        self.player.flag_image.render(surface, (x, y))

    def update(self):
        if self.get_num_troops()==0:
            self.dead=True
            self.player.armies.remove(self)
            self.player.to_be_deleted.append(self)
        if self.getting_food:
            if time.time()-self.food_counter==1:
                self.player.food+=int(0.25*self.get_troop_count())

        if self.action=="recruit":
            if time.time()-self.recruit_counter >= 1.5:
                self.recruit_counter=time.time()
                if self.recruit_city.population>0:
                    self.recruit_city.population-=1
                    self.add_troops(1)
                else:
                    self.recruit_city.dead=True
                    self.recruit_city=None
                    self.action="loiter"
        if self.action=="forage":
            if time.time()-self.forage_counter >= self.race.house_food_prod:
                self.player.food+=1
                self.forage_counter=time.time()

        if self.active_enemy:
            self.action="fight"
            self.image_action="attack"
            pos=[0,0]
            pos[0]=self.active_enemy.offset[0]-self.offset[0]
            pos[1]=self.active_enemy.offset[1]-self.offset[1]

            if pos[0]>0:
                if pos[1]>0:self.image_direction="bottomright"
                elif pos[1]<0:self.image_direction="topright"
                else:self.image_direction="right"
            elif pos[0]<0:
                if pos[1]>0:self.image_direction="bottomleft"
                elif pos[1]<0:self.image_direction="topleft"
                else:self.image_direction="left"
            else:
                if pos[1]>0:self.image_direction="bottom"
                elif pos[1]<0:self.image_direction="top"
                else:pass#I hope this doesn't happen...

            if self.active_enemy.dead==True:
                self.active_enemy=None
                self.army_xp+=1
                self.captain_xp+=1
                self.action="loiter"
                self.image_action="still"
                self.image_on=0
            else:
                if time.time()-self.attack_counter>=0.25:
                    self.attack_counter=time.time()
                    self.active_enemy.damage(self.get_attack_value())

        spd=self.get_speed()
        if self.goto==self.tile_pos:
            self.goto=None

        if not self.goto:
            if self.offset[0]==0.5 and self.offset[1]==0.5:
                if self.image_action=="moving":
                    self.image_action="still"
                    self.image_on=0
                    self.action="loiter"

        if self.goto:
            self.image_action="moving"
            self.action="move"
            if self.goto[0]<self.tile_pos[0]:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((-spd, -spd))
                    self.image_direction="topleft"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((-spd, spd))
                    self.image_direction="bottomleft"
                else:
                    self.move((-spd, 0))
                    self.image_direction="left"
            elif self.goto[0]>self.tile_pos[0]:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((spd, -spd))
                    self.image_direction="topright"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((spd, spd))
                    self.image_direction="bottomright"
                else:
                    self.move((spd, 0))
                    self.image_direction="right"
            else:
                if self.goto[1]<self.tile_pos[1]:
                    self.move((0, -spd))
                    self.image_direction="top"
                elif self.goto[1]>self.tile_pos[1]:
                    self.move((0, spd))
                    self.image_direction="bottom"
                else:
                    pass#I mean come on!, why should this ever happen? :P

        else:
            if self.action=="move":
                o_dir=self.image_direction
                self.image_direction=""
                if not self.offset[0]==0.5:
                    if abs(self.offset[0]-0.5) < spd:
                        self.offset[0]=0.5
                    else:
                        if self.offset[0]<0.5:
                            self.move((spd, 0))
                            self.image_direction="right"
                        elif self.offset[0]>0.5:
                            self.move((-spd, 0))
                            self.image_direction="left"
                if not self.offset[1]==0.5:
                    if abs(self.offset[1]-0.5) < spd:
                        self.offset[1]=0.5
                    else:
                        if self.offset[1]<0.5:
                            self.move((0, spd))
                            self.image_direction="bottom"+self.image_direction
                        elif self.offset[1]>0.5:
                            self.move((0, -spd))
                            self.image_direction="top"+self.image_direction
                if not self.image_direction:
                    self.image_direction=o_dir

    def add_troops(self, num):
        tot_troops=0
        for i in self.race.soldier_types:
            new_num = random.randint(0, num-tot_troops)
            if self.soldier_type_counts[i]>=num:
                pass
            else:
                new_num=self.soldier_type_counts[i]
            self.soldier_type_counts[i]+=new_num
            tot_troops+=new_num
        if tot_troops < num:
            choice=random.choice(list(self.race.soldier_types))
            new_num=num-tot_troops
            if new_num > self.soldier_type_counts[i]:
                new_num=self.soldier_type_counts[i]
            self.soldier_type_counts[i]+=new_num
    
    def rightClick(self, tile_position):
        if tile_position:self.goto=tile_position

    def damage(self, amount):
        defense=self.get_defense_value()
        defense+=int(defense*float(2*random.randint(1, 100)*0.02))
        dodge=self.get_dodge_value()
        amount-=defense
        amount-=int(random.randint(0, dodge)*0.1)
        if amount<0:
            amount=1

        self.lose_troops(amount)

    def lose_troops(self, num_troops):
        tot_troops=0

        if num_troops <= 0:
            return

        for i in self.race.soldier_types:
            new_num = random.randint(0, num_troops-tot_troops)
            if self.soldier_type_counts[i]>=new_num:
                pass
            else:
                new_num=self.soldier_type_counts[i]
            self.soldier_type_counts[i]-=new_num
            tot_troops+=new_num
        if tot_troops < num_troops:
            choice=random.choice(list(self.race.soldier_types))
            new_num=num_troops-tot_troops
            if self.soldier_type_counts[choice]>=new_num:
                pass
            else:
                new_num=self.soldier_type_counts[i]
            self.soldier_type_counts[choice]-=new_num
            tot_troops+=new_num

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

        self.soldier_count=self.race.start_troops

        self.glyphs=[]
        self.move([0.5, 0.5])

        self.dead=False

        self.active_enemy=None
        self.attack_counter=time.time()

    def get_glyph_by_name(self, name):
        for i in self.glyphs:
            if i.name==name:
                return i

    def get_attack_value(self):
        return self.soldier_count*self.race.soldier_types.itervalues().next()['attack']

    def get_defense_value(self):
        return self.soldier_count*self.race.soldier_types.itervalues().next()['defense']

    def get_dodge_value(self):
        return self.soldier_count*self.race.soldier_types.itervalues().next()['dodge']

    def render(self, surface, camera_pos=[0,0]):
        x, y=self.rect.topleft
        x+=camera_pos[0]
        y+=camera_pos[1]

        if self.player.active_entity==self:
            self.player.select_image.render(surface, (x, y+18))

        self.image.render(surface, (x,y))
        self.player.flag_image.render(surface, (x, y))

    def make_unit(self, captain_name="None",num_troops=10):
        soldier_type_counts={}
        tot_troops=0

        if num_troops <= 0:
            return

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

        if new_num <= 0:
            return

        a = Unit(self.iso_world, self.player, captain_name,
                 not self.player.elder_placed, 0, 0,
                 soldier_type_counts, self.tile_pos)
        a.move([0.5, 0.5])
        self.player.elder_placed=True
        self.player.armies.append(a)

    def update(self):
        if self.soldier_count<=0:
            self.dead=True
            self.player.houses.remove(self)
            self.player.to_be_deleted.append(self)
        if time.time()-self.food_counter >= 5:
            self.player.food+=self.race.house_food_prod
            self.food_counter=time.time()

        if time.time()-self.troop_counter >= self.race.house_troop_prod:
            self.soldier_count+=1
            self.troop_counter=time.time()

        if self.active_enemy:
            if self.active_enemy.dead:
                self.active_enemy=None
            else:
                if time.time()-self.attack_counter>=0.25:
                    self.attack_counter=time.time()
                    self.active_enemy.damage(self.get_attack_value())

    def rightClick(self, tile_position):
        pass

    def damage(self, amount):
        defense=self.get_defense_value()
        defense+=int(defense*1.5)
        defense+=int(defense*float(2*random.randint(1, 100)*0.02))
        dodge=int(self.get_dodge_value()*0.1)

        amount-=defense
        amount-=random.randint(0, dodge)
        if amount<0:
            amount=1

        self.lose_troops(amount)

    def lose_troops(self, num_troops):
        self.soldier_count-=num_troops

class Player(isometric.UnitContainer):
    def __init__(self, name=None, race=None, color=[255,255,255,255]):
        self.name=name

        self.race=race

        self.houses=[]
        self.armies=[]
        self.to_be_deleted=[]

        self.food=int(race.start_food)
        self.food_counter=time.time()
        self.active_entity = None

        self.flag_image=self.race.flag_image.copy()
        self.select_image=self.race.select_image.copy()
        self.color=color

        self.elder_placed=False

        for x in xrange(self.flag_image.get_width()):
            for y in xrange(self.flag_image.get_height()):
                a = tuple(self.flag_image.get_at((x, y)))
                if a[0]>=100 and a[1]==0 and a[2]==0 and a[3]==255:
                    amount=spc_div(float(a[0]), 255)
                    r, g, b, a = self.color
                    r=r*amount
                    g=g*amount
                    b=b*amount
                    self.flag_image.set_at((x, y), (r, g, b, a))

        for x in xrange(self.select_image.get_width()):
            for y in xrange(self.select_image.get_height()):
                a = tuple(self.select_image.get_at((x, y)))
                if a[0]>=100 and a[1]==0 and a[2]==0 and a[3]==255:
                    amount=spc_div(float(a[0]), 255)
                    r, g, b, a = self.color
                    r=r*amount
                    g=g*amount
                    b=b*amount
                    self.select_image.set_at((x, y), (r, g, b, a))

    def create_house(self, iso_world, pos=[0,0]):
        a=House(iso_world, self, pos)
        self.houses.append(a)
        return a

    def flush(self):
        for i in self.to_be_deleted:
            self.to_be_deleted.remove(i)
            del i

    def update(self):
        for i in self.houses:
            i.update()
        if self.armies:
            self.armies[0].captain_is_elder=True
            self.armies[0].image=self.race.elder_image
        else:
            self.elder_placed=False
        for i in self.armies:
            i.update()
        if time.time()-self.food_counter>=5:
            for i in self.armies:
                self.food-=i.get_consumption()
            self.food_counter=time.time()

        self.flush()

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
        self.render_priority=1

        self.dead=False

class City(isometric.Unit):
    def __init__(self, iso_world, name="None", population=100,
                 image=None, pos=[0,0]):

        isometric.Unit.__init__(self, iso_world, image, pos)

        self.rect.center=tuple(self.pos)

        self.name=name
        self.population=population

        self.render_priority=1

        self.dead=False

        self.counter=time.time()

    def update(self):
        if self.population <= 0:
            self.dead=True
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
        
        
