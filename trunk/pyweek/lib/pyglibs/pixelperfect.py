import pygame
from image import Image, AnimatedImage

class Hitmask(object):
    def __init__(self, image, format=None,
                 rect=None, pos=[0,0]):

        self.image=image
        self.format=format

        self.pos=pos

        if rect:
            self.rect=rect
            self.pos=self.rect.topleft
        else:
            self.rect=image.get_rect()
            self.rect.topleft=self.pos

        self.mask=[]
        self.animated=False

        if self.image:
            self.compile()

    def __make__(self, image):
        if self.format:f=self.format
        else:
            if image.get_alpha() and image.get_colorkey():
                f="c+a"
            elif image.get_colorkey():
                f="c"
            elif image.get_alpha():
                f="a"
            else:
                f="f"

        mask=[]

        for y in range(self.rect.height):
            mask.append([])
            for x in range(self.rect.width):
                if f=="c":
                    mask[y].append(not image.get_at((x,y)) == image.get_colorkey())
                elif f=="a":
                    mask[y].append(not image.get_at((x,y))[3] == 0)
                elif f=="c+a":
                    mask[y].append(not (image.get_at((x,y)) == image.get_colorkey() or\
                                        image.get_at((x,y))[3] == 0))
                elif f=="f":
                    mask[y].append(True)
                else:
                    mask[y].append(False)
        return mask

    def __comp__(self):
        if isinstance(self.image, AnimatedImage):
            self.animated=True
            cur=[]
            for y in xrange(len(self.image.all_images)):
                cur.append([])
                for x in xrange(len(self.image.all_images[y])):
                    cur[y].append(self.__make__(self.image.all_images[y][x].surface))
            self.mask=cur
        elif isinstance(self.image, pygame.Surface):
            image=self.image
            self.mask=self.__make__(image)
        else:
            image=self.image.surface
            self.mask=self.__make__(image)

    def get_mask(self):
        if self.animated:
            return self.mask[self.image.on_y][self.image.on_x]
        return self.mask

    def compile(self, image=None, format=None, rect=None):
        if image:
            self.image=image
            if rect:
                self.rect=rect
            else:
                self.rect=image.get_rect()
        if rect:self.rect=rect
        if format:self.format=format

        self.__comp__()

    def collidemask(self, other):
        r1, r2, hm1, hm2 = self.rect, other.rect, self.get_mask(), other.get_mask()

        rect=r1.clip(r2)
        if rect.width==0 or rect.height==0:
            return False

        x1,y1,x2,y2 = rect.x-r1.x,rect.y-r1.y,rect.x-r2.x,rect.y-r2.y
        for y in xrange(rect.height-1):
            for x in xrange(rect.width-1):
                if hm1[y1+y][x1+x] and hm2[y2+y][x2+x]:return True
                else:continue
        return False

    def colliderect(self, other):
        rect=self.rect.clip(other)
        if rect.width==0 or rect.height==0:
            return False
        offset_x=rect.left-self.rect.left
        offset_y=rect.top-self.rect.top
        mask=self.get_mask()
        for y in xrange(rect.height):
            for x in xrange(rect.width):
                if mask[y+offset_y][x+offset_x]:return True
                else:continue
        return False 

    def collidepoint(self, other):
        p=other[0]-self.rect.left,other[1]-self.rect.top
        if p[0]<0 or p[1]<0:
            return False
        if p[0]>self.rect.width-1 or p[1]>self.rect.height-1:
            return False
        if self.get_mask()[p[1]][p[0]]:
            return True
        return False

    def collide(self, other):
        if isinstance(other, Hitmask):
            return self.collidemask(other)
        elif isinstance(other, pygame.Rect):
            return self.colliderect(other)
        else:
            return self.collidepoint(other)
