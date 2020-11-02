import pygame, sys
import random
import os

WIDTH = 500
HEIGHT = 600
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8

#CONSTANTS - PHYSICS
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.9
vec = pygame.math.Vector2

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (48, 227, 255)

#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#BACKGROUND
#background = pygame.image.load(os.path.join(img_folder, "space.png")).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "character_robot_idle.png")).convert()
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.pos = vec(10, GROUND - 60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def update(self):

        self.acc = vec(0, PLAYER_GRAV)
        
        #RETURNS A LIST, keystate, OF ALL PRESSED KEYS
        keystate = pygame.key.get_pressed()

        #CHECKS TO SEE WHICH KEYS WERE IN THE LIST (A.K.A PRESSED)
        if keystate[pygame.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        if keystate[pygame.K_LEFT]:
            self.acc.x += -PLAYER_ACC
        if keystate[pygame.K_UP]:
            self.rect.y += -5
        if keystate[pygame.K_DOWN]:
            self.rect.y += 5
        if self.vel.y == 0 and keystate[pygame.K_SPACE]:
            self.vel.y = -20

        #APPLY FRICTION IN THE X DIRECTION
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #EQUATIONS OF MOTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #WRAP AROUND THE SIDES OF THE SCREEN
        if self.pos.x > WIDTH - 30:
            self.pos.x = WIDTH - 30
        if self.pos.x < 0 + 30:
            self.pos.x = 0 + 30

        #SIMULATE THE GROUND
        if self.pos.y > GROUND:
            self.pos.y = GROUND + 1
            self.vel.y = 0

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos
            

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "UfoGrey.png")).convert()
        self.image = pygame.transform.scale(self.image, (150, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 500
        self.rect.y = 450

    def update(self):
        self.rect.x += -5

        if self.rect.right < 0:
            self.rect.left = WIDTH

    
#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
platform = Platform()
all_sprites.add(player, platform)

# GAME LOOP:
#   Process Events
#   Update
#   Draw
running = True
while running:

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # UPDATE
    all_sprites.update()

    # DRAW
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()


