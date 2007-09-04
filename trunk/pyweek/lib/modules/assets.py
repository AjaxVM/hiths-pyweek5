import pygame
from pygame.locals import *

class Sound:
    def __init__(self,fname,vol=1):
        self.sound = None
        try:
            if pygame.mixer.get_init():
                self.sound = pygame.mixer.Sound(fname)
                self.vol = vol
        except:
            pass
    def play(self):
        if self.sound:
            try:
                if pygame.mixer.get_init():
                    self.sound.set_volume(self.vol)#*Sound.sfx*0.5/100)
                    self.sound.play()
            except:
                pass
