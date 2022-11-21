import pygame, sys, os, math, random
from globals import *
from COVID_Combat import *
from Battlefield import *
from Player import *
from Enemy import *
from Camera import *

def debug(s):
    pygame.display.set_caption(s)
    print(s)

COVID_Combat().run()

