import pygame, sys, os, math, random

WINDOW_SIZE = (1280, 720)
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 1280
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRID_SIDE = 40
UPDATE_FREQUENCY = 60
RAYCAST_COUNT = 10
TOTAL_VIEWPOINT_ANGLE = math.pi / 3
PROJECTION_SCREEN_DEPTH = 1280 * 1.732 / 2
WALL_HEIGHT = 1
SCALING_FACTOR = WINDOW_WIDTH / RAYCAST_COUNT
MAX_RAYCAST_HOPS = 128

class Camera:
    def __init__(self, player, grid):
        self.player = player
        self.grid = grid

    def take_snapshot(self):
        theta = self.player.curr_viewpoint_angle - (TOTAL_VIEWPOINT_ANGLE / 2)
        d_theta = (TOTAL_VIEWPOINT_ANGLE / (RAYCAST_COUNT * 2))
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

            projected_wall_height = WALL_HEIGHT * PROJECTION_SCREEN_DEPTH / final_wall_depth
            pygame.draw.rect(pygame.display.get_surface(), GREEN,
                    (int(i * SCALING_FACTOR), int(WINDOW_HEIGHT/2 - projected_wall_height/2),
                    int(SCALING_FACTOR), int(projected_wall_height)))
            pygame.draw.line(pygame.display.get_surface(), RED, (src_x * GRID_SIDE, src_y * GRID_SIDE),(dst_x * GRID_SIDE, dst_y * GRID_SIDE))
            theta += d_theta

class Player():
    def __init__(self, grid, clock_tick):
        self.points = 0
        self.x = 10
        self.y = 10
        self.curr_viewpoint_angle = 0
        self.grid = grid
        self.image = pygame.transform.scale(pygame.image.load("images/player.png"), (GRID_SIDE, GRID_SIDE))
        self.gun_shot = pygame.mixer.Sound('sounds/gun_shot.wav')
        self.clock_tick = clock_tick

    def update(self):
        pygame.display.get_surface().blit(self.image, (GRID_SIDE * self.x, GRID_SIDE * self.y))

    def change_position(self, delta_position):
        if self.grid[self.x + delta_position[0]][self.y + delta_position[1]] == 0:
            self.x += delta_position[0]
            self.y += delta_position[1]

    def shoot(self):
        self.gun_shot.play()

    def rotate_viewpoint(self):
        edge_distance = 80
        if pygame.mouse.get_pos()[0] + edge_distance > WINDOW_WIDTH:
            pygame.mouse.set_pos([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])
        if pygame.mouse.get_pos()[0] < edge_distance:
            pygame.mouse.set_pos([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])
        self.curr_viewpoint_angle += min(max(pygame.mouse.get_rel()[0], -50), 50) * self.clock_tick * 0.0005

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

    def render(self):
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
        self.clock_tick = pygame.time.Clock().tick(UPDATE_FREQUENCY)

        self.battlefield = Battlefield()
        self.player = Player(self.battlefield.grid, self.clock_tick)
        self.camera = Camera(self.player, self.battlefield.grid)

    def run(self):
        while True:
            self.clock_tick = pygame.time.Clock().tick(UPDATE_FREQUENCY)
            pygame.display.get_surface().fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RIGHT:
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
                    self.player.rotate_viewpoint()
            self.battlefield.render()
            self.camera.take_snapshot()
            self.player.update()
            pygame.display.flip()

COVID_Combat().run()