import pygame, sys, os, math, random
from globals import *
from COVID_Combat import *
from Battlefield import *
from Enemy import *
from Camera import *

class Player():
    def __init__(self, grid):
        self.x = 10
        self.y = 10
        self.direction = RIGHT
        self.curr_viewpoint_angle = 0
        self.grid = grid
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"),
                (GRID_SIDE, GRID_SIDE))
        self.gun_shot = pygame.mixer.Sound('sounds/gun_shot.wav')
        self.active_bullets = []

    def update(self):
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))
        # pygame.draw.circle(pygame.display.get_surface(), (0, 200, 200), (self.x, self.y), 10)
        bullets = []
        for b in self.active_bullets:
            i = int(b[0] / GRID_SIDE)
            j = int(b[1] / GRID_SIDE)
            if (self.grid[i][j] == 0):
                bullet_hit = False
                global enemies
                for enemy in enemies:
                    if enemy.x == i and enemy.y == j:
                        enemy.alive = False
                        bullet_hit = True
                        break
                if not bullet_hit:
                    pygame.draw.circle(pygame.display.get_surface(),
                            (0, 200, 200), (b[0], b[1]), 5)
                    bullets.append((b[0] + b[2], b[1] + b[3], b[2], b[3]))
        self.active_bullets = bullets


    def change_position(self, delta_position):
        # x = int(self.x + delta_position[0] * math.cos(self.curr_viewpoint_angle) * FRAME_DELAY * 5)
        # y = int(self.y + delta_position[1] * math.sin(self.curr_viewpoint_angle) * FRAME_DELAY * 5)
        # print(str(x) + " " + str(y))
        # if x < len(self.grid) and x > -1 and y > -1 and y < len(self.grid[0]) and self.grid[x][y] != 5:
            # self.x = x
            # self.y = y

        if ((self.direction + 2) % 4) == delta_position[2]:
            self.direction = delta_position[2]
            return
        x = self.x + delta_position[0]
        y = self.y + delta_position[1]

        if x < len(self.grid) and x > -1 and y > -1 and y < len(self.grid[0]) and self.grid[x][y] == 0:
            self.x = x
            self.y = y
        self.direction = delta_position[2]

    def shoot(self):
        self.gun_shot.play()
        dx = 0
        dy = 0
        speed = 5
        if self.direction == RIGHT:
            dx = speed
        elif self.direction == LEFT:
            dx = -speed
        elif self.direction == UP:
            dy = -speed
        elif self.direction == DOWN:
            dy = speed
        self.active_bullets.append((self.x * GRID_SIDE + GRID_SIDE/2,
                self.y * GRID_SIDE + GRID_SIDE/2, dx, dy))

    def rotate_viewpoint(self):
        self.curr_viewpoint_angle += min(max(pygame.mouse.get_rel()[0], -50), 50) * FRAME_DELAY
        if self.curr_viewpoint_angle > 2 * math.pi:
            self.curr_viewpoint_angle -= 2 * math.pi
        if self.curr_viewpoint_angle < -2 * math.pi:
            self.curr_viewpoint_angle += 2 * math.pi
        pygame.mouse.set_pos([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])