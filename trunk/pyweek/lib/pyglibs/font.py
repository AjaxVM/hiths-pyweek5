import pygame

class Font(object):
    def __init__(self, name=None, size=32,
                 antialias=False, color=[255,255,255,255]):

        self.name=name
        self.fsize=size
        self.antialias=antialias
        self.color=color

        self.font=pygame.font.Font(name, size)

    def size(self, text=""):
        return self.font.size(text)

    def set_font(self, name=None):
        self.font=pygame.font.Font(name, self.size)
        self.name=name

    def set_size(self, size=32):
        self.font=pygame.font.Font(self.name, size)
        self.size=size

    def render(self, text=""):
        return self.font.render(text, self.antialias, self.color)

class FontLoader(object):
    def __init__(self):
        self.fonts={}

    def load_font(self, name=None, size=32,
                  antialias=False, color=[255,255,255,255],
                  proxy="default"):
        if proxy in self.fonts:
            return self.fonts[proxy]
        else:
            a=Font(name, size, antialias, color)
            self.fonts[proxy]=a
            return a
