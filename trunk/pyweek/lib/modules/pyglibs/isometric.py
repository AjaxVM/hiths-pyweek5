import random

import pygame
from pygame.locals import *

import image


class Grid(object):
    def __init__(self, tile_size=[32,16],
                 mode="pure"):#can be map too, for AOE type map, with no black edges

        self.tile_size=tile_size
        self.mode=mode

    def convert_tile_to_pixel(self, x, y):
        if self.mode=="pure":
            return self.conv_pure(x, y)
        elif self.mode=="map":
            return self.conv_map(x, y)
        return [cx, cy]

    def conv_pure(self, x, y):
        cx = self.tile_size[0]*x
        cy = self.tile_size[1]*y

        cx -= (self.tile_size[1])*y
        cx -= (self.tile_size[1])*x

        cy -= (self.tile_size[1]/2)*y
        cy += (self.tile_size[1]/2)*x

        return [cx, cy]

    def conv_map(self, x, y):
        if y:odd=y%2
        else:odd=0

        cx=x*self.tile_size[0]
        cy=y*self.tile_size[1]/2
        if odd:
            cx+=self.tile_size[1]
        return [cx, cy]

    def get_tile_left(self, x, y):
        if self.mode=="pure":
            return [x-1, y]
        elif self.mode=="map":
            if y:odd=y%2
            else:odd=0

            if odd:
                return [x, y-1]
            return [x-1, y-1]

    def get_tile_right(self, x, y):
        if self.mode=="pure":
            return [x+1, y]
        elif self.mode=="map":
            if y:odd=y%2
            else:odd=0

            if odd:return [x+1, y+1]
            else:return [x, y+1]

    def get_tile_top(self, x, y):
        if self.mode=="pure":
            return [x, y-1]
        elif self.mode=="map":
            if y:odd=y%2
            else:odd=0

            if odd:return [x+1, y-1]
            else:return [x, y-1]

    def get_tile_bottom(self, x, y):
        if self.mode=="pure":
            return [x, y+1]
        elif self.mode=="map":
            if y:odd=y%2
            else:odd=0

            if odd:
                return [x, y+1]
            return [x-1, y+1]

    def get_tile_topleft(self, x, y):
        if self.mode=="pure":
            return [x-1, y-1]
        elif self.mode=="map":
            return [x, y-2]

    def get_tile_topright(self, x, y):
        if self.mode=="pure":
            return [x+1, y-1]
        elif self.mode=="map":
            return [x+1, y]

    def get_tile_bottomleft(self, x, y):
        if self.mode=="pure":
            return [x-1, y+1]
        elif self.mode=="map":
            return [x-1, y]

    def get_tile_bottomright(self, x, y):
        if self.mode=="pure":
            return [x+1, y+1]
        elif self.mode=="map":
            return [x, y+2]


class TileImage(object):
    def __init__(self, surf, split_color=[0,0,0,255]):
        a=image.AnimatedImage(surf, split_color)

        self.all_images=a.all_images
        a=self.all_images[0]

        self.tile=a[0].surface

        if len(a)>1:
            self.trans_left=a[1].surface
            self.trans_right=a[2].surface
            self.trans_top=a[3].surface
            self.trans_bottom=a[4].surface
        else:
            self.trans_left=None
            self.trans_right=None
            self.trans_top=None
            self.trans_bottom=None


class UnitContainer(object):
    def __init__(self):
        self.named_items={}
        self.unnamed_items=[]

        self.all=[]

    def add(self, item, name=None):
        self.all.append(item)
        if name:
            self.named_items[name]=item
        else:
            self.unnamed_items.append(item)
        return item

    def remove(self, name):
        if name in self.named_items:
            a=self.named_items[name]
            self.all.remove(a)
            del self.named_items[name]
        elif name in self.unnamed_items:
            self.all.remove(name)
            self.unnamed_items.remove(name)
        else:
            a=self.unnamed_items[name]
            self.all.remove(a)
            del self.unnamed_items[name]

    def get(self, name):
        if name in self.named_items:
            return self.named_items[name]
        elif name < len(self.unnamed_items):
            return self.unnamed_items[name]

    def get_units_in_area(self, rect):
        cur=[]
        for i in self.all:
            if rect.colliderect(i.rect):
                cur.append(i)
        return cur


class Camera(object):
    def __init__(self, world, pos=[0,0],
                 offset=[0.5, 0.5], rect=None,
                 lock_to_map=True,
                 background_image=None):
        self.rect=rect

        self.lock_to_map=lock_to_map

        self.world=world

        self.background_image=background_image

        self.pos=pos
        self.offset=offset

    def convert_pos(self):
        pos=self.world.grid.convert_tile_to_pixel(*self.pos)
        n=self.world.grid.conv_pure(*self.offset)
        pos[0]+=n[0]
        pos[1]+=n[1]
        if self.rect:
            pos[0]+=int(self.rect.width/2)
            pos[1]+=int(self.rect.height/2)
        return pos

    def check_pos(self):
        if self.lock_to_map:
            if self.offset[0] < 0:
                self.pos[0]-=1
                self.offset[0]+=1
            if self.offset[0] > 1:
                self.pos[0]+=1
                self.offset[0]-=1

            if self.offset[1] < 0:
                self.pos[1]-=1
                self.offset[1]+=1
            if self.offset[1] > 1:
                self.pos[1]+=1
                self.offset[1]-=1

            if self.pos[0] > 0:
                self.pos[0]=0
            if self.pos[0]<-self.world.map_width:
                self.pos[0]=-self.world.map_width

            if self.pos[1] > 0:
                self.pos[1]=0
            if self.pos[1]<-self.world.map_height:
                self.pos[1]=-self.world.map_height

    def to_pos(self, pos=[0,0], offset=[0,0]):
        self.pos=pos
        self.offset=offset

    def move(self, pos):
        self.pos[0]+=pos[0]
        self.pos[1]+=pos[1]
        self.check_pos()

    def mysort(self, a, b):
        if int(a.tile_pos[1])<int(b.tile_pos[1]):
            return -1
        elif int(a.tile_pos[1])>int(b.tile_pos[1]):
            return 1

        elif int(a.tile_pos[0])<int(b.tile_pos[0]):
            return -1
        elif int(a.tile_pos[0])>int(b.tile_pos[0]):
            return 1

        elif a.render_priority>b.render_priority:
            return 1
        elif a.render_priority<b.render_priority:
            return -1
        return 0

    def get_mouse_pos(self, mouse_pos=None):
        if not mouse_pos:
            mx, my=pygame.mouse.get_pos()
        else:
            mx, my=mouse_pos

        cpos=self.convert_pos()
        mx -= cpos[0]
        my -= cpos[1]

        d=self.world.comp_data

        for x in range(len(d)):
            c=d[x]
            if c.rect.collidepoint((mx, my)):
                nmx, nmy = int(mx-c.rect.left), int(my-c.rect.top)

                if not c.image.get_at((nmx, nmy)) == c.blank_color:
                    return c.tile_pos
        return None

    def render(self, surface, unit_group=[]):
        ret_clip=surface.get_clip()
        if self.rect:
            new_clip=pygame.Rect(self.rect)
            new_clip.clip(ret_clip)
            surface.set_clip(new_clip)

        if self.background_image:
            surface.blit(self.background_image, new_clip.topleft)

        pos=self.convert_pos()
        r=pygame.Rect((-pos[0], -pos[1]), [self.rect.width, self.rect.height+50])
        big=self.world.get_tiles_in_area(r)

        for i in big:
            i.render(surface, pos)

        big=[]
        if isinstance(unit_group, list):
            for i in unit_group:
                big.extend(i.get_units_in_area(r))
        else:
            big=unit_group.get_units_in_area(r)

        for i in big:
            if i.pos[0] < 0 or i.pos[0] > self.rect.width:
                del i
            elif i.pos[1] < 0 or i.pos[1] > self.rect.height:
                del i

        big.sort(self.mysort)

        for i in big:
            i.render(surface, pos)

        surface.set_clip(ret_clip)


class Tile(object):
    def __init__(self, iso_world, pos, tile_sheet,
                 type, tile_pos):

        self.iso_world=iso_world

        self.render_priority=0

        self.pos=pos
        self.tile_pos=tile_pos
        self.tile_sheet=tile_sheet
        self.image=self.tile_sheet.tile
        self.comp_image=[self.image]
        self.rect=self.image.get_rect()
        self.rect.midtop=tuple(self.pos)
        self.type=type

        self.priority=0

        self.blank_color=self.image.get_at((0,0))
        self.use_trans=[]

    def get_transitions(self):
        tl, tr, tt, tb = self.iso_world.get_side_tiles(self.tile_pos)

        if tl:
            if not tl.type==self.type:
                if "right" in tl.use_trans:
                    self.comp_image.append(tl.tile_sheet.trans_right)
                else:
                    tl.comp_image.append(self.tile_sheet.trans_left)

        if tt:
            if not tt.type==self.type:
                if "bottom" in tt.use_trans:
                    self.comp_image.append(tt.tile_sheet.trans_top)
                else:
                    tt.comp_image.append(self.tile_sheet.trans_bottom)

        if tr:
            if not tr.type==self.type:
                choice=random.choice([True, False])
                if choice:
                    self.use_trans.append("right")
        if tb:
            if not tb.type==self.type:
                choice=random.choice([True, False])
                if choice:
                    self.use_trans.append("bottom")


    def render(self, surface, camera_pos=[0,0]):
        x, y=self.rect.topleft
        x+=camera_pos[0]
        y+=camera_pos[1]
        for i in self.comp_image:
            surface.blit(i, (x, y))

class World(object):
    def __init__(self, map=None, tiles={},
                 tile_size=[32, 16],
                 tile_split_color=(0,0,0,255)):

        self.map=map

        self.grid=Grid(tile_size)

        self.map_width, self.map_height=[len(self.map[0]), len(self.map)]

        self.tiles=tiles
        self.__make_tiles__(tile_split_color)
        self.tile_size=tile_size

        self.data=[]
        self.comp_data=[]

        self.build()

    def in_bounds(self, pos):
        if pos[0]>=0 and pos[0]<self.map_width and\
           pos[1]>=0 and pos[1]<self.map_height:
            return True
        return False

    def get_side_tiles(self, pos):
        left=self.grid.get_tile_left(*pos)
        right=self.grid.get_tile_right(*pos)
        top=self.grid.get_tile_top(*pos)
        bottom=self.grid.get_tile_bottom(*pos)
        if self.in_bounds(left):
            left=self.data[left[1]][left[0]]
        else:
            left=None
        if self.in_bounds(right):
            right=self.data[right[1]][right[0]]
        else:
            right=None
        if self.in_bounds(top):
            top=self.data[top[1]][top[0]]
        else:
            top=None
        if self.in_bounds(bottom):
            bottom=self.data[bottom[1]][bottom[0]]
        else:
            bottom=None

        return left, right, top, bottom

    def __make_tiles__(self, scolor):
        if self.tiles:
            if isinstance(self.tiles.itervalues().next(), TileImage):
                pass
            else:
                for x in self.tiles:
                    self.tiles[x]=TileImage(self.tiles[x], scolor)

    def get_tiles_in_area(self, rect):
        cur=[]
        for i in self.comp_data:
            if rect.colliderect(i.rect):
                cur.append(i)
        return cur

    def get_pos(self, x, y):
        return self.grid.convert_tile_to_pixel(x, y)

    def build(self):
        self.data=[]
        self.comp_data=[]
        for y in range(len(self.map)):
            self.data.append([])
            for x in range(len(self.map[0])):
                type=self.map[y][x]
                image=self.tiles[type]
                a=Tile(self, self.get_pos(x,y),
                                         image, type, [x,y])
                self.data[y].append(a)
                self.comp_data.append(a)
        for t in self.comp_data:
            t.get_transitions()


class Unit(object):
    def __init__(self, iso_world,image=None,
                 pos=[0,0], rect=None,
                 lock_to_map=True,
                 render_priority=1):
        self.image=image

        self.iso_world=iso_world

        self.render_priority=render_priority

        self.tile_pos=pos
        self.pos=iso_world.get_pos(*self.tile_pos)
        self.offset=[0,0]

        self.lock_to_map=lock_to_map

        if rect:
            self.rect=rect
            self.rect.midbottom=iso_world.get_pos(*self.pos)
        else:
            self.rect=self.image.get_rect()
            self.rect.midbottom=iso_world.get_pos(*self.pos)

        self.move()

    def check_collision(self, other):
        if isinstance(other, Unit):
            return self.rect.colliderect(other.rect)
        elif isinstance(other, UnitContainer):
            for other in other.group:
                if self.rect.colliderect(other.rect):
                    return True
            return False

        elif isinstance(other, pygame.Rect):
            return self.rect.colliderect(other)

        else:
            return self.rect.collidepoint(other)

    def render(self, surface, camera_pos=[0,0]):
        x, y=self.rect.topleft
        x+=camera_pos[0]
        y+=camera_pos[1]
        if isinstance(self.image, pygame.Surface):
            surface.blit(self.image, (x,y))
        else:
            self.image.render(surface, (x,y))

    def move(self, direction=[0,0]):
        if self.lock_to_map:
            old_off=list(self.offset)
            old_tile=list(self.tile_pos)
        self.offset[0]+=direction[0]
        self.offset[1]+=direction[1]

        if self.offset[0]<0:
            self.tile_pos=self.iso_world.grid.get_tile_left(*self.tile_pos)
            self.offset[0]=1+self.offset[0]
        elif self.offset[0]>=1:
            self.tile_pos=self.iso_world.grid.get_tile_right(*self.tile_pos)
            self.offset[0]=self.offset[0]-1

        if self.offset[1]<0:
            self.tile_pos=self.iso_world.grid.get_tile_top(*self.tile_pos)
            self.offset[1]=1+self.offset[1]
        elif self.offset[1]>=1:
            self.tile_pos=self.iso_world.grid.get_tile_bottom(*self.tile_pos)
            self.offset[1]=self.offset[1]-1

        if self.lock_to_map:
            if self.tile_pos[0]<0 or self.tile_pos[0]>=self.iso_world.map_width or\
               self.tile_pos[1]<0 or self.tile_pos[1]>=self.iso_world.map_height:
                self.offset=old_off
                self.tile_pos=old_tile

        self.pos=self.iso_world.get_pos(*self.tile_pos)
        n=self.iso_world.grid.conv_pure(*self.offset)
        self.pos[0]+=n[0]
        self.pos[1]+=n[1]
        self.rect.midbottom=tuple(self.pos)
