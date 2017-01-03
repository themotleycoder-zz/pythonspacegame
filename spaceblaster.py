from pygame.locals import *
import pygame
import sys
import time
import random
import math
from os import path

size = width, height = 1024, 768
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0, 255,0)
clock = pygame.time.Clock

img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'sounds')

screen = pygame.display.set_mode(size)
FPS = 60
maxMissiles = 10
numberOfMeteors = 10
maxVal = 10
score = 0
pygame.font.init()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(path.join(img_dir, "spaceShips_009.png")).convert_alpha()
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * 0.8), int(h * 0.8)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = height-(h+25)
        self.rect.x = (width/2)-(w/2)
        self.speed = 0

    def update(self):
        self.speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.speed = 10
        elif keys[pygame.K_LEFT]:
            self.speed = -10

        self.rect.x += self.speed

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def getRect(self):
        return self.rect

    def shoot(self):
        if (len(missiles) < maxMissiles):
            rect = player.getRect()
            missile = Missile([self.rect.center[0], rect.y+20])
            shoot_sound.play()
            all_sprites.add(missile)
            missiles.add(missile)


class Missile(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(path.join(img_dir, "spaceMissiles_007.png")).convert_alpha()
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w * 0.5), int(h * 0.5)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]-  (w/2)
        self.rect.y = position[1]-h
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):

    speed = [0.5, 1]

    def __init__(self, speed, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "spaceMeteors_002.png")).convert_alpha()
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * scale), int(h * scale)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.height / 2
        if self.rect.width>self.rect.height:
            self.radius = self.rect.width / 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self. rect.x = random.randrange(width - self.rect.width)
        self.rect.y = 0
        self.speed = speed
        self.mass = (math.pi * (self.radius*self.radius))/2

    def update(self):

        self.test_collide()

        if self.rect.right > width or self.rect.x < 0:
            self.speed[0] = -self.speed[0]

        if self.rect.bottom > height or self.rect.y < 0:
            self.speed[1] = -self.speed[1]

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def test_collide(self):
        for meteor in meteors:
            if meteor is not self:
                diffx = self.rect.center[0] - meteor.rect.center[0]
                diffy = self.rect.center[1] - meteor.rect.center[1]
                # distance between ball centers
                distance = math.sqrt((diffx * diffx) + (diffy * diffy))

                if distance <= (self.radius + meteor.radius):
                    self.bounce_balls(self, meteor)

    def bounce_balls(self, firstBall, secondBall):
        newVelX1 = (firstBall.speed[0] * (firstBall.mass - secondBall.mass) + (
        2 * secondBall.mass * secondBall.speed[0])) / (firstBall.mass + secondBall.mass);
        newVelY1 = (firstBall.speed[1] * (firstBall.mass - secondBall.mass) + (
        2 * secondBall.mass * secondBall.speed[1])) / (firstBall.mass + secondBall.mass);
        newVelX2 = (secondBall.speed[0] * (secondBall.mass - firstBall.mass) + (
        2 * firstBall.mass * firstBall.speed[0])) / (firstBall.mass + secondBall.mass);
        newVelY2 = (secondBall.speed[1] * (secondBall.mass - firstBall.mass) + (
        2 * firstBall.mass * firstBall.speed[1])) / (firstBall.mass + secondBall.mass);
        firstBall.speed = [newVelX1, newVelY1]
        secondBall.speed = [newVelX2, newVelY2]

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',48)
    label = largeText.render(text, 1, (255,255,255))
    screen.blit(label, (100,100))
    # pygame.display.flip()

pygame.init()
pygame.mixer.init()

#load all sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "explosion.wav"))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, "8bit_bomb_explosion.wav"))

meteors = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for _ in range(numberOfMeteors):
    meteor = Meteor([random.randrange(1, maxVal, 1), random.randrange(1, maxVal, 1)], scale = random.uniform(0.1, 0.5))
    meteors.add(meteor)
    all_sprites.add(meteor)

player = Player()
all_sprites.add(player)

running = True;
while running:

    # ticks = pygame.time.get_ticks()
    clock().tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                meteor = Meteor([random.randrange(random.randrange(-1, 1, 1), maxVal, 1), random.randrange(1, maxVal, 1)], scale=random.uniform(0.1, 0.5))
                meteors.add(meteor)
                all_sprites.add(meteor)
            elif event.key == pygame.K_SPACE:
                player.shoot()
            # else:
            #     print("Unrecognized key")

    hits = pygame.sprite.groupcollide(meteors , missiles, True, True)
    for hit in hits:
        explosion_sound . play()
        score+=100
        meteor = Meteor([random.randrange(random.randrange(-1, 1, 1), maxVal, 1), random.randrange(1, maxVal, 1)], scale=random.uniform(0.1, 0.5))
        meteors.add(meteor)
        all_sprites.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    #Update sprites
    all_sprites.update()

    #Render screen
    screen.fill(BLACK)
    message_display("Score:" + str(score))
    all_sprites.draw(screen)
    #Now flip the display
    pygame.display.flip()


pygame.quit()


