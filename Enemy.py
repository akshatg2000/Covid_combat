'''
Enemy class
'''

import pygame, sys, os, math, random
from globals import *
from COVID_Combat import *
from Battlefield import *
from Player import *
from Camera import *

class Enemy:
    def __init__(self, x, y, direction, grid):
        self.counter = 0
        self.x = x
        self.alive = True
        self.y = y
        self.grid = grid
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load("images/enemy.png"),
                (GRID_SIDE, GRID_SIDE))

    def update(self):
        if self.counter == 0:
            speed = 1
            x = self.x
            y = self.y
            self.direction = random.randint(0, 3)
            if self.direction == 0:
                x += speed
            elif self.direction == 1:
                y -= speed
            elif self.direction == 2:
                x -= speed
            elif self.direction == 3:
                y += speed
            if x < len(self.grid) and x > -1 and y > -1 and y < len(self.grid[0]) and self.grid[x][y] == 0:
                self.x = x
                self.y = y
            self.counter = 30
        else:
            self.counter -= 1
        pygame.display.get_surface().blit(self.image,
                (GRID_SIDE * self.x, GRID_SIDE * self.y))