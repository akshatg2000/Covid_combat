import pygame, sys, os, math, random
pygame.mixer.init()
bang=pygame.mixer.Sound('bang.wav')
music=pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_SIDE = 40
UPDATE_FREQUENCY = 60

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
        self.grid = grid
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"), (GRID_SIDE, GRID_SIDE))

    def update(self):
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))

    def change_position(self, delta_position):
        if self.grid[self.x + delta_position[0]][self.y + delta_position[1]] == 0:
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
            # if pygame.key.get_pressed()[pygame.K_RIGHT]:
                # self.player.change_position((1, 0))
            # elif pygame.key.get_pressed()[pygame.K_LEFT]:
                # self.player.change_position((-1, 0))
            # elif pygame.key.get_pressed()[pygame.K_UP]:
                # self.player.change_position((0, -1))
            # elif pygame.key.get_pressed()[pygame.K_DOWN]:
                # self.player.change_position((0, 1))
            self.battlefield.update()
            self.player.update()
            for coronavirus in self.coronaviruses:
                print("calling update on coronas")
                coronavirus.update()
            pygame.display.flip()

def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("COVID Combat")
    COVID_Combat().run()

main()
