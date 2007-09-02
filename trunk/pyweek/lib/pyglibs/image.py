import pygame
from pygame.locals import *

import time

def load_surface(name, colorkey=None, alpha=None):
    image=pygame.image.load(name)
    if alpha:
        image=image.convert_alpha()
    else:
        image=image.convert()
    if isinstance(alpha, int):
        image.set_alpha(alpha)

    if not colorkey==None:
        if colorkey==-1:
            image.set_colorkey(image.get_at([0,0]),RLEACCEL)
        elif len(colorkey)==2:
            image.set_colorkey(image.get_at(colorkey),RLEACCEL)
        elif len(colorkey)==3 or len(colorkey)==4:
            image.set_colorkey(colorkey,RLEACCEL)
        else:
            raise AttributeError, "Invalid colorkey: %s"%colorkey
    return image

def load_image(name, colorkey=None, alpha=None):
    return Image(load_surface(name, colorkey, alpha))

def load_animated_image(name, colorkey=None, alpha=None,
                        split_color=[0,0,0,255],
                        frame_delay=0.25, cycle_rows=False):
    return AnimatedImage(load_surface(name, colorkey, alpha),
                         split_color,
                         frame_delay, cycle_rows)

class ImageLoader(object):
    def __init__(self):
        self.loaded_images={}

    def get_image(self, proxy=None):
        return self.loaded_images[proxy]

    def load_surface(self, filename, colorkey=None, alpha=None,
                     proxy=None):
        if proxy==None:
            if filename in self.loaded_images:
                return self.loaded_images[filename]
        else:
            if proxy in self.loaded_images:
                return self.loaded_images[proxy]

        surface=load_surface(filename, colorkey, alpha)
        if proxy:
            self.loaded_images[proxy]=surface
            return surface
        else:
            self.loaded_images[filename]=surface
            return surface

    def load_image(self, filename, colorkey=None, alpha=None,
                   proxy=None):
        if proxy==None:
            if filename in self.loaded_images:
                return self.loaded_images[filename]
        else:
            if proxy in self.loaded_images:
                return self.loaded_images[proxy]

        image=load_image(filename, colorkey, alpha)
        if proxy:
            self.loaded_images[proxy]=image
            return image
        else:
            self.loaded_images[filename]=image
            return image

    def load_animated_image(self, filename, colorkey=None, alpha=None,
                            split_color=(0,0,0,255), frame_delay=0.25,
                            cycle_rows=True, proxy=None):
        if proxy==None:
            if filename in self.loaded_images:
                return self.loaded_images[filename]
        else:
            if proxy in self.loaded_images:
                return self.loaded_images[proxy]

        image=load_animated_image(filename, colorkey, alpha, split_color,
                                  frame_delay, cycle_rows, on_x, on_y)
        if proxy:
            self.loaded_images[proxy]=image
            return image
        else:
            self.loaded_images[filename]=image
            return image

    
class Image(object):
    def __init__(self, surface):
        self.surface=surface
        self.base_surface=surface.copy()

    def get_size(self):
        return self.surface.get_size()

    def get_at(self, pos):
        return self.surface.get_at(pos)

    def set_at(self, pos, color):
        self.surface.set_at(pos, color)

    def get_rect(self):
        return self.surface.get_rect()

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

    def render(self, surface, pos=[0,0]):
        surface.blit(self.surface, pos)

    def copy(self):
        return Image(self.surface.copy())

    def blit(self, other, dest, rect=None):
        if isinstance(other, pygame.Surface):
            pass
        else:
            other=other.surface
        if rect:
            self.surface.blit(other, dest, rect)
        else:
            self.surface.blit(other, dest)

    def resize(self, size, mode=None):
        size=list(size)
        surf=self.surface.copy()
        if size[0]<self.surface.get_width():
##            size[0]=self.surface.get_width()
            surf=pygame.transform.scale(surf, [size[0], surf.get_height()])
        if size[1]<self.surface.get_height():
##            size[1]=self.surface.get_height()
            surf=pygame.transform.scale(surf, [surf.get_width(), size[1]])

##        if size[0]==self.surface.get_width() and\
##           size[1]==self.surface.get_height():
##            return

        colorkey=surf.get_colorkey()
        surf.set_colorkey(None)

        if mode==None:
            surf.set_colorkey(colorkey, RLEACCEL)
            return Image(surf)

        elif mode=="scale":
            nsurf=pygame.transform.scale(surf, size)

        elif mode=="split" or mode=="enlarge":
            image=surf.copy()

            rect=image.get_rect()

            nw=int(rect.width/3)
            nh=int(rect.height/3)
            image=pygame.transform.scale(image, (nw*3, nh*3))

            topleft=image.subsurface([0,0], [nw, nh]).copy()
            midtop=image.subsurface([nw,0],[nw, nh]).copy()
            topright=image.subsurface([nw*2,0],[nw,nh]).copy()

            midleft=image.subsurface([0,nh], [nw, nh]).copy()
            center=image.subsurface([nw,nh], [nw,nh]).copy()
            midright=image.subsurface([nw*2,nh], [nw,nh]).copy()

            bottomleft=image.subsurface([0,nh*2], [nw, nh]).copy()
            midbottom=image.subsurface([nw,nh*2],[nw, nh]).copy()
            bottomright=image.subsurface([nw*2,nh*2],[nw,nh]).copy()

            width=(int(size[0]/nw)+1)*nw
            height=(int(size[1]/nh)+1)*nh

            num_x=(width/nw)-1
            num_y=(height/nh)-1

            nsurf=pygame.transform.scale(surf.copy(), (width, height))
            r=nsurf.get_rect()
            nsurf.fill((0,0,0,0))

            nsurf.blit(topleft, [0,0])
            nsurf.blit(topright, [num_x*nw, 0])
            nsurf.blit(bottomleft, [0, num_y*nh])
            nsurf.blit(bottomright, [num_x*nw, num_y*nh])

            for x in range(1, num_x):
                nsurf.blit(midtop, [x*nw, 0])
                nsurf.blit(midbottom, [x*nw, num_y*nh])

            for y in range(1, num_y):
                nsurf.blit(midleft, [0, y*nh])
                nsurf.blit(midright, [num_x*nw, y*nh])

            if mode=="split":
                for y in range(1, num_y):
                    for x in range(1, num_x):
                        nsurf.blit(center, [x*nw, y*nh])
            else:
                center=pygame.transform.scale(center, [nw*(num_x-1), nh*(num_y-1)])
                nsurf.blit(center, [nw, nh])

        elif mode=="multiply":
            image=surf.copy()
            ns=[0,0]
            while ns[0] < size[0]:
                ns[0]+=image.get_width()
            while ns[1] < size[1]:
                ns[1]+=image.get_height()

            nsurf=pygame.transform.scale(image, ns)
            nsurf.fill([0,0,0,0])

            for y in range(ns[1]/image.get_height()):
                for x in range(ns[0]/image.get_width()):
                    nsurf.blit(image, [x*image.get_width(),
                                       y*image.get_height()])
        else:
            surf.set_colorkey(colorkey)
            return Image(surf)

        surf.set_colorkey(colorkey, RLEACCEL)
        nsurf=nsurf.copy()
        nsurf.set_colorkey(colorkey, RLEACCEL)
        return Image(nsurf)

class AnimatedImage(object):
    def __init__(self, surface, split_color=[0,0,0,255],
                 frame_delay=0.25, cycle_rows=False):
        self.surface=surface
        if isinstance(self.surface, pygame.Surface):
            pass
        else:
            self.surface=surface.surface
        self.base_surface=surface.copy()

        self.split_color=tuple(split_color)

        self.frame_delay=frame_delay
        self.last_time=time.time()

        self.cycle_rows=cycle_rows

        self.all_images=[]

        self.on_x=0
        self.on_y=0
        self.compile()

    def get_size(self):
        return self.all_images[self.on_y][self.on_x].get_size()

    def get_rect(self):
        return self.all_images[self.on_y][self.on_x].get_rect()

    def copy(self):
        a=AnimatedImage(self.surface, self.split_color,
                        self.frame_delay, self.cycle_rows)
        a.on_x=int(self.on_x)
        a.on_y=int(self.on_y)
        return a

    def get_at(self, pos):
        return self.all_images[self.on_y][self.on_x].get_at(pos)

    def set_at(self, pos, color):
        for y in self.all_images:
            for x in y:
                x.set_at(pos, color)

    def get_width(self):
        return self.all_images[self.on_y][self.on_x].get_width()

    def get_height(self):
        return self.all_images[self.on_y][self.on_x].get_height()

    def blit(self, other, dest, rect=None):
        for y in self.all_images:
            for x in y:
                x.blit(other, pos, rect)

    def resize(self, size, mode=None):
        cur=[]
        for y in xrange(len(self.all_images)):
            cur.append([])
            for x in self.all_images[y]:
                cur[y].append(x.resize(size, mode))
        return cur

    def find_dimensions(self):
        width=0
        height=0

        #get width
        for x in range(self.base_surface.get_width()):
            ok=True
            for y in range(self.base_surface.get_height()):
                if not self.base_surface.get_at((x,y)) == self.split_color:
                    ok=False
                else:
                    continue
            if ok:
                width=x
                break

        #get height
        for y in range(self.base_surface.get_height()):
            ok=True
            for x in range(width):
                if not self.base_surface.get_at((x,y)) == self.split_color:
                    ok=False
                else:
                    continue
            if ok:
                height=y
                break

        if width==0:width = self.base_surface.get_width()
        if height==0:height = self.base_surface.get_height()
        return width, height

    def compile(self):
        new_images=[]
        dimensions=self.find_dimensions()
        for y in range((self.surface.get_height())/dimensions[1]):
            new_images.append([])
            for x in range((self.surface.get_width())/dimensions[0]):
                new_image=pygame.transform.scale(self.surface.copy(),
                                                 dimensions)
                if self.surface.get_colorkey():
                    new_image.fill(self.surface.get_colorkey())
                else:
                    new_image.fill(self.surface.get_at((0,0)))
                r=pygame.Rect(x+x*dimensions[0], y+y*dimensions[1],
                              dimensions[0], dimensions[1])
                new_image.blit(self.surface.subsurface(r), [0,0])
                new_images[y].append(Image(new_image))
        self.all_images=new_images
        self.last_time=time.time()
        return None

    def render(self, surface, pos=[0,0]):
        if time.time()-self.last_time>self.frame_delay:
            self.last_time=time.time()
            self.on_x+=1
            if self.cycle_rows:
                if self.on_x>=len(self.all_images[self.on_y]):
                    self.on_x=0
                    self.on_y+=1
                    if self.on_y>=len(self.all_images):
                        self.on_y=0
            else:
                if self.on_x>=len(self.all_images[self.on_y]):
                    self.on_x=0
        self.all_images[self.on_y][self.on_x].render(surface, pos)
        return None
