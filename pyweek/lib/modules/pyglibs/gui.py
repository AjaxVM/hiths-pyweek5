import pygame, time
from pygame.locals import *

import image as gImage
from font import Font
import gui_util
try:
    import pixelperfect
    can_do_pp=True
except:
    print "module <gui>, pixelperfect not found, will ignore all pixelperfect calls"
    can_do_pp=False

class Panel(object):
    '''Non-interactive background panel object
        pos = [0,0]
        dim = [10,10]
        visible = True
        image_mode=scale
    ''' 
    def __init__(self, pos=[0,0], dim=[10,10], image=None,
                 visible=True, image_mode=None):

        self.pos=pos
        self.dim=dim

        self.kind="Panel"

        self.image=image

        self.image_mode=image_mode

        self.visible=visible
        self.refactor()

    def refactor(self):
        self.area = self.dim
        
        if isinstance(self.image, pygame.Surface):
            pass
        else:
            self.image=self.image.resize(self.area, self.image_mode)

##        if self.image.get_width() > self.area[0]:
##                self.area[0]=self.image.get_width()
##        if self.image.get_height() > self.area[1]:
##                self.area[1]=self.image.get_height()
        
        self.rect=pygame.Rect(self.pos, self.dim)

    def update(self, event):
        pass

    def render(self, surface):
        if self.visible:
            if isinstance(self.image, pygame.Surface):
                surface.blit(self.image, self.rect)
            else:
                self.image.render(surface, self.rect)

class Label(object):
    ''' Text Label Object
        init args:
        pos - list[x,y], font, message, image - image, wrap_text - bool,
        align ["left"/"right","top"/"bottom"], visible - bool,
        image_mode - scale,split,enlarge,multiply'''
    def __init__(self, pos=[0,0], font=None,
                 message="", image=None,
                 wrap_text=False, align=["left","top"],
                 visible=True, image_mode=None):

        self.pos=pos

        self.kind="Label"

        self.font=font
        if not font:
            self.font=Font()

        self.message=message
        self.lines=[]
        self.message_image=None

        self.image=image

        self.image_mode=image_mode
        self.wrap_text=wrap_text

        self.align=align

        self.visible=visible
        self.refactor()

    def refactor(self):
        self.lines, area=gui_util.wrap_text(self.font, self.message, self.wrap_text)

        self.area=list(area)

        if self.image:
            if isinstance(self.image, pygame.Surface):
                pass
            else:
                self.image=self.image.resize(self.area, self.image_mode)

            if self.image.get_width() > self.area[0]:
                self.area[0]=self.image.get_width()
            if self.image.get_height() > self.area[1]:
                self.area[1]=self.image.get_height()

        self.message_image=pygame.Surface(self.area).convert_alpha()
        self.message_image.fill([0,0,0,0])
        l=[self.font.render(i) for i in self.lines]
        for i in range(len(l)):
            line=l[i]
            r=line.get_rect()

            if self.align[0]=="left":
                r.left=0
            elif self.align[0]=="center":
                r.centerx=self.area[0]/2
            else:
                r.right=self.area[0]

            if self.align[1]=="top":
                r.top=0
            elif self.align[1]=="center":
                r.centery=self.area[1]/2
            else:
                r.right=self.area[1]

            r.top+=i*(self.font.fsize-(self.font.fsize/3))

            self.message_image.blit(line, r.topleft)

        self.rect=pygame.Rect(self.pos, self.area)

    def update(self, event):
        pass

    def render(self, surface):
        if self.visible:
            if self.image:
                if isinstance(self.image, pygame.Surface):
                    surface.blit(self.image, self.rect)
                else:
                    self.image.render(surface, self.rect)

            surface.blit(self.message_image, self.rect.topleft)

class ButtonCode(object):
    def __init__(self, function=None, args=[], kwargs={}):
        self.function=function

        if not isinstance(args, (list, tuple)):
            args=[args]

        self.args=args
        self.kwargs=kwargs

    def execute(self):
        self.function(*self.args, **self.kwargs)

class Button(Label):
    def __init__(self, pos=[0,0], font=None,
                 message="", wrap_text=False,
                 align=["left","top"], visible=True,

                 image_normal=None, image_hover=None,
                 image_click=None, image_mode=None,
                 use_pp=False, codes=[]):

        self.image_normal=image_normal
        self.image_hover=image_hover
        self.image_click=image_click

        if self.image_normal:
            self.rect=self.image_normal.get_rect()

        self.use_pp=use_pp
        if not can_do_pp:
            self.use_pp=False

        Label.__init__(self, pos, font, message,
                       None,
                       wrap_text, align, visible,
                       image_mode)

        self.image=self.image_normal

        self.kind="Button"

        self.codes=codes

        if self.use_pp:
            self.hitmask_image=None
            if self.image:
                self.hitmask_image=pixelperfect.Hitmask(self.image, pos=self.pos)
            self.hitmask_text=pixelperfect.Hitmask(self.message_image, pos=self.pos)

        self.hovering=False
        self.mouse_button_down=False
        self.am_clicked=False
        self.was_clicked=False

    def refactor(self):

        self.lines, area=gui_util.wrap_text(self.font, self.message, self.wrap_text)

        self.area=list(area)

        if self.image_normal:
            if isinstance(self.image_normal, pygame.Surface):
                pass
            else:
                self.image_normal=self.image_normal.resize(area,self.image_mode)
                if self.image_normal.get_width() > self.area[0]:
                    self.area[0]=self.image_normal.get_width()
                if self.image_normal.get_height() > self.area[1]:
                    self.area[1]=self.image_normal.get_height()

        if self.image_hover:
            if isinstance(self.image_hover, pygame.Surface):
                pass
            else:
                self.image_hover=self.image_hover.resize(area,
                                                         self.image_mode)

        if self.image_click:
            if isinstance(self.image_click, pygame.Surface):
                pass
            else:
                self.image_click=self.image_click.resize(area,self.image_mode)

        self.message_image=pygame.Surface(self.area).convert_alpha()
        self.message_image.fill([0,0,0,0])
        l=[self.font.render(i) for i in self.lines]
        for i in range(len(l)):
            line=l[i]
            r=line.get_rect()

            if self.align[0]=="left":
                r.left=0
            elif self.align[0]=="center":
                r.centerx=self.area[0]/2
            else:
                r.right=self.area[0]

            if self.align[1]=="top":
                r.top=0
            elif self.align[1]=="center":
                r.centery=self.area[1]/2
            else:
                r.right=self.area[1]

            self.message_image.blit(line, r.topleft)

        self.image=self.image_normal

        self.rect=pygame.Rect(self.pos, self.area)
        if self.use_pp:
            self.hitmask_text=pixelperfect.Hitmask(self.message_image, pos=self.pos)
            self.hitmask_image=pixelperfect.Hitmask(self.image,
                                                    pos=self.pos)

    def update(self, event):
        mouse_pos=pygame.mouse.get_pos()
        if self.visible:

            if self.use_pp:
                if (self.hitmask_image and self.hitmask_image.collidepoint(mouse_pos))or\
                    self.hitmask_text.collidepoint(mouse_pos):
                    if event.type==MOUSEBUTTONDOWN:
                        if event.button==1:
                            self.mouse_button_down=True
                        else:
                            self.mouse_button_down=False
                    elif event.type==MOUSEBUTTONUP:
                        if event.button==1:
                            self.mouse_button_down=False
                            if self.am_clicked:
                                self.was_clicked=True
                                if type(self.codes) is type(list()):
                                    for i in self.codes:
                                        i.execute()
                                else:
                                    self.codes.execute()
                            self.am_clicked=False

                    else:
                        pass

                    if self.mouse_button_down:
                        self.am_clicked=True
                    self.hovering=True
                else:
                    self.am_clicked=False
                    self.hovering=False

            else:
                if self.rect.collidepoint(mouse_pos):
                    if event.type==MOUSEBUTTONDOWN:
                        if event.button==1:
                            self.mouse_button_down=True
                        else:
                            self.mouse_button_down=False
                    elif event.type==MOUSEBUTTONUP:
                        if event.button==1:
                            self.mouse_button_down=False
                            if self.am_clicked:
                                self.was_clicked=True
                                for i in self.codes:
                                    i.execute()
                            self.am_clicked=False

                    else:
                        pass

                    if self.mouse_button_down:
                        self.am_clicked=True
                    self.hovering=True
                else:
                    self.am_clicked=False
                    self.hovering=False

    def render(self, surface):
        if self.am_clicked:
            self.image=self.image_click
        elif self.hovering:
            self.image=self.image_hover
        else:
            self.image=self.image_normal

        Label.render(self, surface)


class StateButton(object):
    def __init__(self, pos=[0,0], font=None,
                 message="", wrap_text=False,
                 align=["left","top"], visible=True,
                 state_images=[], state=0,
                 image_mode=None, use_pp=False):
        self.buttons=[]
        for i in state_images:
            self.buttons.append(Button(pos, font,
                                message, wrap_text,
                                align, visible,
                                i[0], i[1], i[2],
                                image_mode, use_pp, []))
        self.state=0

        self.visible=visible

        self.kind="StateButton"

    def refactor(self):
        for i in self.buttons:
            i.refactor()

    def update(self, event):
        for i in self.buttons:
            i.visible=self.visible
        self.buttons[self.state].update(event)
        if self.buttons[self.state].was_clicked:
            self.buttons[self.state].was_clicked=False
            self.state+=1
            if self.state>=len(self.buttons):
                self.state=0

    def render(self, surface):
        self.buttons[self.state].render(surface)

class VStatusBar(object):
    def __init__(self, pos=[0,0], font=None,
                 message="", box_color=(255,255,255),
                 status_color=(0,0,0), box_image=None,
                 size=[32, 100],
                 align=['left','top'], states=5,
                 visible=True, padding=[0,0]):

        self.pos=pos
        self.font=font
        if not self.font:
            self.font=Font()
        self.message=message

        self.padding=padding

        self.kind="VScrollBar"

        self.size=size

        self.status_color=status_color
        self.box_color=box_color

        self.box_image=box_image
        if self.box_image:
            if isinstance(self.box_image, pygame.Surface):
                self.box_image=image.Image(self.box_image)
            self.box_image=self.box_image.resize(self.size, "split")
            self.size=list(self.box_image.get_size())

        self.rect=pygame.Rect(self.pos, self.size)

        self.label=Label(self.rect.midtop, self.font,
                         message, None,
                         False, align,
                         visible, None)

        self.align=align

        self.states=states
        self.value=0

        self.visible=visible

    def update_status(self, min_value, max_value):
        if min_value==0 or max_value==0:
            self.value=0
        else:
            if min_value>max_value:min_value=max_value
            tot=float(min_value)/float(max_value)
            area=self.states*tot
            self.value=area

    def update(self, event):
        pass

    def render(self, surface):
        if self.visible:
            if self.box_image:
                self.box_image.render(surface, self.rect)
            r=pygame.Rect(self.rect)
            if self.box_color:
                pygame.draw.rect(surface, self.box_color, r, max(self.padding)+1)

            if self.value and self.status_color:
                r.top+=self.padding[1]
                r.height=self.value*(self.size[1]/self.states)
                r.height-=self.padding[1]*1.5

                r.left+=self.padding[0]
                r.width-=self.padding[0]*1.5
                pygame.draw.rect(surface, self.status_color, r)

            self.label.render(surface)

class HStatusBar(VStatusBar):
    def __init__(self, pos=[0,0], font=None,
                 message="", box_color=(255,255,255),
                 status_color=(0,0,0), box_image=None,
                 size=[100, 32],
                 align=['left','top'], states=5,
                 visible=True, padding=[0,0]):

        VStatusBar.__init__(self, pos, font, message, box_color,
                            status_color, box_image, size,
                            align, states, visible, padding)
        self.label.rect.center=self.rect.center

        self.kind="HScrollBar"

    def render(self, surface):
        if self.visible:
            if self.box_image:
                self.box_image.render(surface, self.rect)
            r=pygame.Rect(self.rect)
            if self.box_color:
                pygame.draw.rect(surface, self.box_color, r, max(self.padding)+1)

            if self.value and self.status_color:
                r.top+=self.padding[1]
                r.height-=self.padding[1]*1.5

                r.left+=self.padding[0]
                r.width=self.value*(self.size[0]/self.states)
                r.width-=self.padding[0]*1.5
                pygame.draw.rect(surface, self.status_color, r)

            self.label.render(surface)

class InputBox(object):
    def __init__(self, pos=[0,0], font=None,
                 prompt="", width=250,
                 start_text="", visible=True,
                 image_normal=None, image_hover=None,
                 image_click=None, image_mode=None,
                 cache_on_KEY=None, ignore_active=False,

                 align=["left","top"],
                 text_padding=[0,0]):

        self.kind="InputBox"

        #TODO: allow area, istead of width, and allow multiple lines of input

        self.pos=pos

        self.image_mode=image_mode

        self.align=align
        self.text_padding=text_padding

        self.ignore_active=ignore_active

        self.width=width

        self.font=font
        if not self.font:
            self.font=Font()

        self.rect=pygame.Rect(self.pos, [width, self.font.fsize])

        self.prompt=prompt
        self.message=start_text
        self.cached_messages=[]

        self.text_pos=len(self.message)

        self.cache_on_KEY=cache_on_KEY

        self.blink_speed=0.5
        self.blink_last=time.time()

        self.image_normal=image_normal
        self.image_hover=image_hover
        self.image_click=image_click

        if self.image_normal:
            if isinstance(self.image_normal, pygame.Surface):
                pass
            else:
                self.image_normal=self.image_normal.resize(self.rect.size,
                                                           self.image_mode)

                self.rect=self.image_normal.get_rect()
                self.rect.topleft=self.pos
                self.width=self.rect.width-self.text_padding[0]*2

        if self.image_hover:
            if isinstance(self.image_hover, pygame.Surface):
                pass
            else:
                self.image_hover=self.image_hover.resize(self.rect.size,
                                                         self.image_mode)

        if self.image_click:
            if isinstance(self.image_click, pygame.Surface):
                pass
            else:
                self.image_click=self.image_click.resize(self.rect.size,
                                                         self.image_mode)

        self.hovering=False
        self.mouse_button_down=False
        self.am_clicked=False
        self.active=False

        self.visible=visible

    def update(self, event):
        mouse_pos=pygame.mouse.get_pos()
        if self.visible:
            if event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.rect.collidepoint(mouse_pos):
                        self.mouse_button_down=True
                    else:
                        self.mouse_button_down=False
            elif event.type==MOUSEBUTTONUP:
                self.mouse_button_down=False
                if event.button==1:
                    if self.rect.collidepoint(mouse_pos):
                        self.was_clicked=True
                        self.active=True
                        self.am_clicked=True
                    else:
                        self.was_clicked=False
                        self.active=False
                        self.am_clicked=False

            elif event.type==KEYDOWN:
                if self.active or self.ignore_active:
                    a=gui_util.convert_event_to_key(event)
                    if not a:
                        return

                    if self.cache_on_KEY:
                        if a==self.cache_on_KEY:
                            self.cached_messages.append(self.message)
                            self.message=""
                            self.text_pos=0
                            return
                        if event.type==KEYDOWN:
                            if event.key==self.cache_on_KEY:
                                self.cached_messages.append(self.message)
                                self.message=""
                                self.text_pos=0
                                return
                    if a=="BACK":
                        if self.text_pos:
                            self.message=self.message[:len(self.message)-1]
                            self.text_pos-=1
                    elif a=="DEL":
                        if len(self.message) > self.text_pos:
                            self.message=self.message[:self.text_pos]+\
                                          self.message[self.text_pos+1:]
                    elif a=="HOME":
                        self.text_pos=0

                    elif a=="END":
                        self.text_pos=len(self.message)
                    elif a=="LEFT":
                        if self.text_pos>0:
                            self.text_pos-=1
                    elif a=="RIGHT":
                        if self.text_pos<len(self.message):
                            self.text_pos+=1
                    elif a=="RETURN":
                        b=self.message[:self.text_pos]+"\n"+self.message[self.text_pos+1:]
                        if self.font.size(self.prompt+b)[0]<self.width:
                            self.message=b
                            self.text_pos+=1
                    elif a=="TAB":
                        b=self.message[:self.text_pos]+"    "+self.message[self.text_pos+1:]
                        if self.font.size(self.prompt+b)[0]<self.width:
                            self.message=b
                            self.text_pos+=4
                    else:
                        b=self.message[:self.text_pos]+a+self.message[self.text_pos+1:]

                        if self.font.size(self.prompt+b)[0]<self.width:
                            self.message=b
                            self.text_pos+=1

            if self.rect.collidepoint(mouse_pos):
                self.hovering=True
                if self.mouse_button_down:
                    self.am_clicked=True
                else:
                    self.am_clicked=False
            else:
                self.hovering=False

    def empty_cache(self):
        a=self.cached_messages[::]
        self.cached_messages=[]
        return a

    def render(self, surface):
        if self.visible:
            if self.am_clicked:
                image=self.image_click
            elif self.hovering:
                image=self.image_hover
            else:
                image=self.image_normal

            if image:
                if isinstance(image, pygame.Surface):
                    surface.blit(image, self.rect.topleft)
                else:
                    image.render(surface, self.rect.topleft)

            text=self.font.render(self.prompt+self.message)
            r=text.get_rect()
            if self.align[0]=="left":
                r.left=self.rect.left
            elif self.align[0]=="center":
                r.centerx=self.rect.centerx
            else:
                r.right=self.rect.right

            if self.align[1]=="top":
                r.top=self.rect.top
            elif self.align[1]=="center":
                r.centery=self.rect.centery
            else:
                r.bottom=self.rect.bottom

            r.left+=self.text_padding[0]
            r.top+=self.text_padding[1]

            surface.blit(text, r.topleft)

            if time.time()>=self.blink_last+self.blink_speed:
                r.left=r.right
                r.left-=self.font.size(self.message[self.text_pos::])[0]
                r.left-=self.font.fsize/15
                if self.active or self.ignore_active:
                    surface.blit(self.font.render("|"), r)
            if time.time()>=self.blink_last+self.blink_speed*2:
                self.blink_last=time.time()

class MessageBox(object):
    def __init__(self, pos=[0,0], font=None,
                 area=[50,50], align=["left","top"],
                 visible=True,
                 image=None, image_mode=None,
                 messages=[], max_lines=None,
                 wrap=False,
                 text_padding=[0,0]):

        self.kind="MessageBox"

        self.pos=pos
        self.font=font
        if not self.font:self.font=Font()

        self.text_padding=text_padding

        self.area=area
        self.align=align

        self.visible=visible

        self.image=image
        self.image_mode=image_mode
        if self.image:
            if isinstance(self.image, pygame.Surface):
                pass
            else:
                self.image=self.image.resize(self.area,
                                             self.image_mode)
                self.area=[self.image.get_width(),
                           self.image.get_height()]

        self.messages=[]
        self.max_lines=max_lines

        self.max_width=0

        self.wrap=wrap

        for i in messages:
            self.add_message(i)

        self.vscroll=0
        self.hscroll=0

    def add_message(self, mess):
        if self.wrap:
            for x in gui_util.wrap_text(self.font, mess, self.wrap)[0]:
                self.messages.append(x)
        else:
            self.messages.append(mess)

        if self.max_lines:
            while len(self.messages)>self.max_lines:
                del self.messages[0]

        self.max_width=0
        for i in self.messages:
            w=self.font.size(i)[0]
            if w>self.max_width:
                self.max_width=w

    def update(self, event):
        pass

    def scroll(self, v=0, h=0):
        self.vscroll+=v
        if self.vscroll<0:
            self.vscroll=0
        if (len(self.messages)+1)*(self.font.fsize-(self.font.fsize/3))>self.area[1]:
            max=(self.font.fsize-(self.font.fsize/3))*(len(self.messages)+1)
            max-=self.area[1]
            if self.vscroll>max:
                self.vscroll=max
        else:
            self.vscroll=0

        self.hscroll+=h
        if self.hscroll<0:
            self.hscroll=0

        if self.max_width > self.area[0]:
            if self.hscroll>self.max_width-self.area[1]:
                self.hscroll=self.max_width-self.area[1]
        else:
            self.hscroll=0

    def render(self, surface):
        if self.visible:
            ret_clip=surface.get_clip()
            new_clip=pygame.Rect((self.pos[0]+self.text_padding[0],
                                  self.pos[1]+self.text_padding[1]),
                                 (self.area[0]-self.text_padding[0]*2,
                                  self.area[1]-self.text_padding[1]*2))
            new_clip.clip(ret_clip)

            if self.image:
                if isinstance(self.image, pygame.Surface):
                    surface.blit(self.image, self.pos)
                else:
                    self.image.render(surface, self.pos)

            surface.set_clip(new_clip)

            lines=[self.font.render(i) for i in self.messages]

            fs=self.font.fsize-(self.font.fsize/3)

            for l in xrange(len(lines)):
                line=lines[l]
                r=line.get_rect()

                y=self.pos[1]+self.text_padding[1]+\
                       (fs*l)+\
                       self.vscroll-(fs*(len(self.messages)+1)-self.area[1])

                x=self.pos[0]+self.text_padding[0]-self.hscroll

                if self.align[0]=="left":
                    r.left=x
                elif self.align[0]=="center":
                    r.centerx=x+self.area[0]/2-self.text_padding[0]
                else:
                    r.right=x+self.area[0]-self.text_padding[0]*2

                if self.align[1]=="top":
                    r.top=y
                elif self.align[1]=="center":
                    r.centery=y
                else:
                    r.bottom=y

                surface.blit(line, r.topleft)
            surface.set_clip(ret_clip)

class Container(object):
    def __init__(self):
        self.named_items={}
        self.unnamed_items=[]
        self.named_list=[]

        self.all=[]

    def add(self, item, name=None):
        self.all.append(item)
        if name:
            self.named_items[name]=item
            return item
        else:
            self.unnamed_items.append(item)
            return item

    def remove(self, name):
        if name in self.named_items:
            self.all.remove(self.named_items[name])
            del self.named_items[name]
        elif name in self.unnamed_items:
            del self.unnamed_items[name]
            del self.all[name]

    def get(self, name):
        if name in self.named_items:
            return self.named_items[name]
        elif name < len(self.unnamed_items):
            return self.unnamed_items[name]

    def render(self, surface):
        for i in self.all:
            i.render(surface)

    def update(self, event):
        for i in self.all:
            i.update(event)
