# Bullet range is 10 * length_of_grid_size
# You can shoot a Coronavirus and gain 10 points
# You can shoot trees without any effect
# You can shoot infected human beings and lose 100 points
# You can shoot healthy human beings and game is over
# You can quickly wear a mask to save yourself by spending 100 points for 10 seconds
# You can get infected(i.e. a Coronavirus touches you)
# Infected human beings recover after 14 seconds if no further coronavirus touches him
# If 3 coronaviruses are alive within you simultaneously, You die and game is over
# Same rules of death is applicable for all human beings
# Infected human beings spread coronavirus at a certain rate(say 3 viruses per second)
# Viruses spread away from the source
# If points drop below 0, game over

# TODO: Create graphics for CoronaVirus, Tree, Infected Human Beings, Healthy Human Beings, Bullet
# TODO: Create sounds for firing, infecting, dying, recovering

import pygame, sys, os, math, random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_SIDE = 40
UPDATE_FREQUENCY = 30

class Tree:
    def __init__(self):
        pass

class CoronaVirus:
    def __init__(self):
        pass

class Human:
    def __init__(self):
        self.infected = False

class Player(Human):
    def __init__(self):
        self.points = 0
        self.x = 1
        self.y = 1
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"), (GRID_SIDE, GRID_SIDE))

    def update(self):
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))

    def change_position(self, delta_position):
        self.x += delta_position[0]
        self.y += delta_position[1]

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
        self.grid = [
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
        self.battlefield = Battlefield()
        self.player = Player()

    def run(self):
        pygame.time.Clock().tick(UPDATE_FREQUENCY)
        while True:
            pygame.display.get_surface().fill((0, 0, 0))
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.change_position((1, 0))
                    elif event.key == pygame.K_LEFT:
                        self.player.change_position((-1, 0))
                    elif event.key == pygame.K_UP:
                        self.player.change_position((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.player.change_position((0, 1))
            self.battlefield.update()
            self.player.update()
            pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("COVID Combat")
    COVID_Combat().run()

main()