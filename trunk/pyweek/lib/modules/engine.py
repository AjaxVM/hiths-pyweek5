import os, random, time

import pygame
from pygame.locals import *

import pyglibs, entities, elements, engine
from pyglibs import isometric, image, gui

def spc_div(a, b):
    if a and b:
        return a/b
    return 0

class Engine(object):
    def __init__(self, state="game"):
        self.state=state

        self.init()

        
        self.run()

    def init(self):
        pygame.init()
        self.screen=pygame.display.set_mode((640, 480))

    def run(self):
        while 1:
            if self.state=="game":
                self.play_game()
            elif self.state=="QUIT":
                return

    def play_game(self):
        self.screen.fill((0,0,0,0))

        self.core_content=elements.load_content()
