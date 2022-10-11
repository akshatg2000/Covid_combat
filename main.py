import pygame, sys, os, math, random

WINDOW_SIZE = (1280, 720)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_SIDE = 40
UPDATE_FREQUENCY = 60
RAYCAST_COUNT = 600
TOTAL_VIEWPOINT_ANGLE = math.pi / 3

class RaycastEngine:
    def __init__(self):
        pass

    # Cast Rays and find the list of objects that needs to be rendered
    # Sort them based on decreasing depth
    # Draw them using blit()
    def cast_rays(self):
        angle_of_ray = player.curr_viewpoint_angle - (TOTAL_VIEWPOINT_ANGLE / 2) + 0.000000001
        for i in range(RAYCAST_COUNT):
            angle_of_ray += (TOTAL_VIEWPOINT_ANGLE / (RAYCAST_COUNT * 2))

        # pygame.display.get_surface().blit(obj_image, (obj_x, obj_y))

class Tree:
    def __init__(self):
        pass

class CoronaVirus:
    def __init__(self, grid, player):
        self.x = 1
        self.y = 1
        self.grid = grid
        self.player = player
        self.image = pygame.transform.scale(pygame.image.load("images/coronavirus.png"), (GRID_SIDE, GRID_SIDE))

    def update(self):
        dx = random.choice([1, 1])
        dy = random.choice([1, 1])
        if self.grid[self.x + dx][self.y + dy] == 0:
            self.x += dx
            self.y += dy
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))


class Human:
    def __init__(self):
        self.infected = False

class Player(Human):
    def __init__(self, grid):
        self.points = 0
        self.x = 1
        self.y = 1
        self.curr_viewpoint_angle = 0
        self.grid = grid
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"), (GRID_SIDE, GRID_SIDE))
        self.gun_shot = pygame.mixer.Sound('sounds/gun_shot.wav')

    def update(self):
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))

    def change_position(self, delta_position):
        if self.grid[self.x + delta_position[0]][self.y + delta_position[1]] == 0:
            self.x += delta_position[0]
            self.y += delta_position[1]

    def shoot(self):
        self.gun_shot.play()

    def rotate_viewpoint(self, pos_change):
        dx, dy = pos_change
        # update self.curr_viewpoint_angle
        pass

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_velocity = 2
        self.y_velocity = 2

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

class Battlefield:
    def __init__(self):
        self.image1 = pygame.transform.scale(pygame.image.load("images/g1.png"), (GRID_SIDE, GRID_SIDE))
        self.image2 = pygame.transform.scale(pygame.image.load("images/g2.png"), (GRID_SIDE, GRID_SIDE))
        self.grid = [ #33x18
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def update(self):
        for i, row in enumerate(self.grid):
            for j, color in enumerate(row):
                image = self.image1
                if (i + j) % 2:
                    image = self.image2
                if (color != 0):
                    pygame.display.get_surface().blit(image, (GRID_SIDE * i, GRID_SIDE * j))

class COVID_Combat:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/background.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("COVID Combat")

        self.battlefield = Battlefield()
        self.player = Player(self.battlefield.grid)
        self.coronaviruses = []
        self.coronaviruses.append(CoronaVirus(self.battlefield.grid, self.player))
        self.coronaviruses.append(CoronaVirus(self.battlefield.grid, self.player))
        self.coronaviruses.append(CoronaVirus(self.battlefield.grid, self.player))
        self.coronaviruses.append(CoronaVirus(self.battlefield.grid, self.player))
        self.coronaviruses.append(CoronaVirus(self.battlefield.grid, self.player))

    def run(self):
        while True:
            pygame.time.Clock().tick(UPDATE_FREQUENCY)
            pygame.display.get_surface().fill((0, 0, 0))
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player.change_position((1, 0))
                    elif event.key == pygame.K_LEFT:
                        self.player.change_position((-1, 0))
                    elif event.key == pygame.K_UP:
                        self.player.change_position((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.player.change_position((0, 1))
                    elif event.key == pygame.K_SPACE:
                        self.player.shoot()
                elif event.type == pygame.MOUSEMOTION:
                    self.player.rotate_viewpoint(event.rel)
            self.battlefield.update()
            self.player.update()
            for coronavirus in self.coronaviruses:
                coronavirus.update()
            pygame.display.flip()

COVID_Combat().run()