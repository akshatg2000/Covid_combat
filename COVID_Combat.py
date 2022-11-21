import pygame, sys, os, math, random
from globals import *
from Battlefield import *
from Player import *
from Enemy import *
from Camera import *

class COVID_Combat:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('sounds/background.mp3')
        pygame.mixer.music.play(-1)

        pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("COVID Combat")

        pygame.mouse.set_visible(False)

        self.game_own = False
        self.game_over = False

        self.battlefield = Battlefield()
        self.player = Player(self.battlefield.grid)
        self.camera = Camera(self.player, self.battlefield.grid)

        self.win_image = pygame.transform.scale(pygame.image.load("images/win.png"),
                    (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2))
        self.game_over_image = pygame.transform.scale(pygame.image.load("images/game_over.png"),
                    (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2))

    def run(self):
        global enemies
        while len(enemies) != INITIAL_ENEMY_COUNT:
            x = random.randint(0, len(self.battlefield.grid) - 1)
            y = random.randint(0, len(self.battlefield.grid[0]) - 1)
            direction = random.randint(0, 3)

            if self.battlefield.grid[x][y] == 0:
                enemies.append(Enemy(x, y, direction, self.battlefield.grid))

        while True:
            pygame.time.Clock().tick(UPDATE_FREQUENCY)

            pygame.display.get_surface().fill((0, 0, 0))

            if len(enemies) == 0:
                self.game_own = True

            if self.game_own:
                pygame.display.get_surface().blit(self.win_image,
                        (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4))

            if self.game_over:
                pygame.display.get_surface().blit(self.game_over_image,
                        (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_RIGHT:
                        self.player.change_position((1, 0, RIGHT))

                    if event.key == pygame.K_LEFT:
                        self.player.change_position((-1, 0, LEFT))

                    if event.key == pygame.K_UP:
                        self.player.change_position((0, -1, UP))

                    if event.key == pygame.K_DOWN:
                        self.player.change_position((0, 1, DOWN))

                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

                if event.type == pygame.MOUSEMOTION:
                    self.player.rotate_viewpoint()

            if self.game_over or self.game_own:
                pygame.display.flip()
                continue

            self.player.update()
            self.battlefield.render_2d_grid()
            #self.camera.take_snapshot()

            alive_enemies = []
            for enemy in enemies:
                if enemy.alive:
                    enemy.update()
                    alive_enemies.append(enemy)

                    if self.player.x == enemy.x and self.player.y == enemy.y:
                        self.game_over = True

            enemies = alive_enemies
            # debug(str(self.player.x) + " " + str(self.player.y) +
            #    " " + str(self.player.curr_viewpoint_angle))

            pygame.display.flip()