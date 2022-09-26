import pygame, sys, os, math, random

COLOR_RED = (255, 0, 0)

# TODO: Create graphics for CoronaVirus, Tree, Infected Human Beings, Healthy Human Beings, Bullet
# TODO: Create sounds for firing, infecting, dying, recovering

class Tree:
    def __init__(self):
        ## Load image
        pass

class CoronaVirus:
    def __init__(self):
        pass

class HumanBeing:
    def __init__(self):
        self.is_infected = False

class You(HumanBeing):
    def __init__(self):
        self.points = 0

class Bullet:
    ## Bullets will follow projectile motion
    def __init__(self):
        self.xSpeed = 10
        self.ySpeed = 10
        self.zSpeed = 0
        self.x = 10
        self.y = 10
        self.z = 10

    def update(self):
        self.zSpeed += 0.2 # We take g=2, will adjust later
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.z += self.zSpeed
        if self.z > 0:
            pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (self.x, self.z, 3, 3))
        # Check collision

class COVID_Combat:
    ## Rules:
    ## Bullet range is 10 * length_of_grid_size
    ## You can shoot a Coronavirus and gain 10 points
    ## You can shoot trees without any effect
    ## You can shoot infected human beings and lose 100 points
    ## You can shoot healthy human beings and game is over
    ## You can quickly wear a mask to save yourself by spending 100 points for 10 seconds
    ## You can get infected(i.e. a Coronavirus touches you)
    ## Infected human beings recover after 14 seconds if no further coronavirus touches him
    ## If 3 coronaviruses are alive within you simultaneously, You die and game is over
    ## Same rules of death is applicable for all human beings
    ## Infected human beings spread coronavirus at a certain rate(say 3 viruses per second)
    ## Viruses spread away from the source
    ## If points drop below 0, game over
    def __init__(self):
        self.battle_field = [
            ## 0 empty space, 1 tree, 2 infected human, 3 healthy human, 4 coronavirus
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        ]

    def run(self):
        pygame.time.Clock().tick(60)
        running = True
        display_update_count = 0
        bullet = Bullet()
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    print("Other key pressed")
            for i, row in enumerate(self.battle_field):
                for j, color in enumerate(row):
                    if (color != 0):
                        pygame.draw.rect(pygame.display.get_surface(), COLOR_RED, ((i * 10, j * 10, 10, 10)))
            bullet.update()
            ## TODO: Currently display is getting updated very rapidly, explore pygame to reduce frequency
            ## This will cause flikering later
            display_update_count += 1
            print("Display updating " + str(display_update_count))
            pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("COVID Combat")
    COVID_Combat().run()

main()