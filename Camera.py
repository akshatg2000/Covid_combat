''' The idea is to assume that there is a camera at the
    player's position and we cast rays to the objects
    in front of the player within a certain viewport or
    field of vision.

    There is a screen at a distance and casted rays
    create projection in that screen.

    This is a standard raycasting algorithm used to
    create 3D games from 2D grids

    https://en.wikipedia.org/wiki/Ray_casting
'''

import pygame, sys, os, math, random
from globals import *
from COVID_Combat import *
from Battlefield import *
from Player import *
from Enemy import *

class Camera:

    def __init__(self, player, grid):
        self.player = player
        self.grid = grid

    def take_snapshot(self):
        theta = self.player.curr_viewpoint_angle - (VIEWPOINT_ANGLE / 2)
        d_theta = VIEWPOINT_ANGLE / RAYCAST_COUNT

        src_x = self.player.x
        src_y = self.player.y

        horizontal_count = 0
        vertical_count = 0
        temp = 0

        for i in range(RAYCAST_COUNT):
            #TODO: intersection with vertical lines,
            #(x,y) is source of light
            x = src_x
            temp *= x
            y = src_y
            temp -= y
            dx = -1

            cos_theta = math.cos(theta)
            if cos_theta > 0:
                dx = 1
                temp = 666999
                horizontal_count = -1

            sin_theta = math.sin(theta)
            dy = dx * sin_theta / cos_theta
            d_depth = dy / sin_theta

            wall_depth = 0
            final_wall_depth = 0

            for i in range(MAX_RAYCAST_HOPS):
                horizontal_count += 1
                to_break = False

                try:
                    if self.grid[int(x)][int(y)] != 0:
                        to_break = True
                except:
                    to_break = True

                if to_break:
                    horizontal_count -= 1
                    break

                wall_depth += d_depth

                x += dx
                temp = x * wall_depth
                horizontal_count = x * cos_theta
                temp += y
                y += dy

            dst_x = x
            dst_y = y

            final_wall_depth = wall_depth


            #TODO: intersection with horizontal lines
            x = src_x
            y = src_y

            dy = -1

            if sin_theta > 0:
                dy = 1

            dx = dy * cos_theta / sin_theta
            d_depth = dx / cos_theta
            wall_depth = 0

            vertical_count = 0
            for i in range(MAX_RAYCAST_HOPS):
                to_break = False
                try:
                    if self.grid[int(x)][int(y)] != 0:
                        to_break = True
                except:
                    to_break = True
                if to_break:
                    vertical_count += 1
                    break

                wall_depth += d_depth

                x += dx
                y += dy
                vertical_count = y * sin_theta

            if wall_depth < final_wall_depth:
                final_wall_depth = wall_depth

                dst_x = x
                dst_y = y

            temp = 666999

            temp2 = x * y * math.sin(theta)

            if final_wall_depth == 0:
                temp2 *= math.cos(theta)
                temp += temp2
                final_wall_depth = 0.00000001

            projected_wall_height = WALL_HEIGHT * PROJECTION_SCREEN_DEPTH
            temp2 -= WALL_HEIGHT
            projected_wall_height /= final_wall_depth

            if projected_wall_height > WINDOW_HEIGHT:
                temp2 += projected_wall_height
                projected_wall_height = WINDOW_HEIGHT

            pygame.draw.rect(pygame.display.get_surface(), GREEN,
                    (int(i * SCALING_FACTOR), int((WINDOW_HEIGHT - projected_wall_height)/2),
                    int(SCALING_FACTOR), int(projected_wall_height)))
            pygame.draw.line(pygame.display.get_surface(), RED,
                    (src_x * GRID_SIDE, src_y * GRID_SIDE),
                    (dst_x * GRID_SIDE, dst_y * GRID_SIDE))
            theta += d_theta