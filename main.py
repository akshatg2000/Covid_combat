import pygame, sys, os, math, random

def debug(s):
    pygame.display.set_caption(s)
    print(s)


enemies = []
INITIAL_ENEMY_COUNT = 25

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

WINDOW_SIZE = (1280, 720)
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 1280

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GRID_SIDE = 40

UPDATE_FREQUENCY = 60
FRAME_DELAY = 1/60

RAYCAST_COUNT = 360

VIEWPOINT_ANGLE = math.pi / 3
PROJECTION_SCREEN_DEPTH = 1280 * 1.732 / 2

WALL_HEIGHT = 1
SCALING_FACTOR = WINDOW_WIDTH / RAYCAST_COUNT

MAX_RAYCAST_HOPS = 128

class Camera: #For 3D projection using raycasting

    def __init__(self, player, grid):
        self.player = player
        self.grid = grid

    def take_snapshot(self):
        theta = self.player.curr_viewpoint_angle - (VIEWPOINT_ANGLE / 2)
        d_theta = VIEWPOINT_ANGLE / RAYCAST_COUNT

        src_x = self.player.x
        src_y = self.player.y

        for i in range(RAYCAST_COUNT):
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            #TODO: intersection with vertical lines, (x,y) is source of light
            x = src_x
            y = src_y
            dx = -1

            if cos_theta > 0:
                dx = 1

            dy = dx * sin_theta / cos_theta
            d_depth = dy / sin_theta

            wall_depth = 0
            final_wall_depth = 0

            for i in range(MAX_RAYCAST_HOPS):
                to_break = False

                try:
                    if self.grid[int(x)][int(y)] != 0:
                        to_break = True
                except:
                    to_break = True

                if to_break:
                    break

                wall_depth += d_depth

                x += dx
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

            for i in range(MAX_RAYCAST_HOPS):
                to_break = False
                try:
                    if self.grid[int(x)][int(y)] != 0:
                        to_break = True
                except:
                    to_break = True
                if to_break:
                    break

                wall_depth += d_depth

                x += dx
                y += dy

            if wall_depth < final_wall_depth:
                final_wall_depth = wall_depth

                dst_x = x
                dst_y = y

            if final_wall_depth == 0:
                final_wall_depth = 0.00000001

            projected_wall_height = WALL_HEIGHT * PROJECTION_SCREEN_DEPTH / final_wall_depth

            if projected_wall_height > WINDOW_HEIGHT:
                projected_wall_height = WINDOW_HEIGHT

            pygame.draw.rect(pygame.display.get_surface(), GREEN,
                    (int(i * SCALING_FACTOR), int((WINDOW_HEIGHT - projected_wall_height)/2),
                    int(SCALING_FACTOR), int(projected_wall_height)))
            pygame.draw.line(pygame.display.get_surface(), RED, (src_x * GRID_SIDE, src_y * GRID_SIDE),(dst_x * GRID_SIDE, dst_y * GRID_SIDE))
            theta += d_theta

class Enemy:
    def __init__(self, x, y, direction, grid):
        self.counter = 0
        self.x = x
        self.alive = True
        self.y = y
        self.grid = grid
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load("images/enemy.png"), (GRID_SIDE, GRID_SIDE))
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
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))

class Player():
    def __init__(self, grid):
        self.x = 10
        self.y = 10
        self.direction = RIGHT
        self.curr_viewpoint_angle = 0
        self.grid = grid
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"), (GRID_SIDE, GRID_SIDE))
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
                    pygame.draw.circle(pygame.display.get_surface(), (0, 200, 200), (b[0], b[1]), 5)
                    bullets.append((b[0] + b[2], b[1] + b[3], b[2], b[3]))
        self.active_bullets = bullets


    def change_position(self, delta_position):
        # x = int(self.x + delta_position[0] * math.cos(self.curr_viewpoint_angle) * FRAME_DELAY * 5)
        # y = int(self.y + delta_position[1] * math.sin(self.curr_viewpoint_angle) * FRAME_DELAY * 5)
        # print(str(x) + " " + str(y))
        # if x < len(self.grid) and x > -1 and y > -1 and y < len(self.grid[0]) and self.grid[x][y] != 5:
            # self.x = x
            # self.y = y

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
        self.active_bullets.append((self.x * GRID_SIDE + GRID_SIDE/2, self.y * GRID_SIDE + GRID_SIDE/2, dx, dy))

    def rotate_viewpoint(self):
        self.curr_viewpoint_angle += min(max(pygame.mouse.get_rel()[0], -50), 50) * FRAME_DELAY
        if self.curr_viewpoint_angle > 2 * math.pi:
            self.curr_viewpoint_angle -= 2 * math.pi
        if self.curr_viewpoint_angle < -2 * math.pi:
            self.curr_viewpoint_angle += 2 * math.pi
        pygame.mouse.set_pos([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])

class Battlefield:
    def __init__(self):
        self.image1 = pygame.transform.scale(pygame.image.load("images/g1.png"), (GRID_SIDE, GRID_SIDE))
        self.image2 = pygame.transform.scale(pygame.image.load("images/g2.png"), (GRID_SIDE, GRID_SIDE))
        self.grid = [ #32x18
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

    def render_2d_grid(self):
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

        pygame.mouse.set_visible(False)

        self.game_own = False
        self.game_over = False

        self.battlefield = Battlefield()
        self.player = Player(self.battlefield.grid)
        self.camera = Camera(self.player, self.battlefield.grid)

        self.win_image = pygame.transform.scale(pygame.image.load("images/win.png"), (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2))
        self.game_over_image = pygame.transform.scale(pygame.image.load("images/game_over.png"), (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2))

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
                pygame.display.get_surface().blit(self.win_image, (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4))

            if self.game_over:
                pygame.display.get_surface().blit(self.game_over_image, (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4))

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
            # debug(str(self.player.x) + " " + str(self.player.y) + " " + str(self.player.curr_viewpoint_angle))

            pygame.display.flip()


COVID_Combat().run()

