
import os, random, time

import pygame
from pygame.locals import *

import modules
from modules import pyglibs, entities, elements, engine
from modules.pyglibs import isometric, image, gui

def spc_div(a, b):
    if a and b:
        return a/b
    return 0

def main():
    engine=engine.Engine(state="game")
