from pygame.locals import *
import pygame
import sys
import time
import random
import math

size = width, height = 1024, 768
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
clock = pygame.time.Clock

screen = pygame.display.set_mode(size)
FPS = 60

numberOfBalls = 3
maxVal = 10
balls = []

pygame.font.init()

class Ball(pygame.sprite.Sprite):

    speed = [0.5, 1]

    def __init__(self, speed, scale):
        pygame.sprite.Sprite.__init__(self)
        w, h = [200,200]
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.radius = 100
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.rect.x = random.randrange(width - self.rect.width)
        self.speed = speed
        self.mass = (math.pi * (self.radius*self.radius))/2

    def update(self):

        self.test_collide()

        if self.rect.right > width or self.rect.left < 0:
            self.speed[0] = -self.speed[0]

        if self.rect.bottom > height or self.rect.top < 0:
            self.speed[1] = -self.speed[1]

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def test_collide(self):
        for ball in balls:
            if ball is not self:
                diffx = self.rect.center[0] - ball.rect.center[0]
                diffy = self.rect.center[1] - ball.rect.center[1]
                # distance between ball centers
                distance = math.sqrt((diffx * diffx) + (diffy * diffy))

                if distance <= (self.radius + ball.radius):
                    self.bounce_balls(self, ball)


    def bounce_balls(self, firstBall, secondBall):
        newVelX1 = (firstBall.speed[0] * (firstBall.mass - secondBall.mass) + (2 * secondBall.mass * secondBall.speed[0])) / (firstBall.mass + secondBall.mass);
        newVelY1 = (firstBall.speed[1] * (firstBall.mass - secondBall.mass) + (2 * secondBall.mass * secondBall.speed[1])) / (firstBall.mass + secondBall.mass);
        newVelX2 = (secondBall.speed[0] * (secondBall.mass - firstBall.mass) + (2 * firstBall.mass * firstBall.speed[0])) / (firstBall.mass + secondBall.mass);
        newVelY2 = (secondBall.speed[1] * (secondBall.mass - firstBall.mass) + (2 * firstBall.mass * firstBall.speed[1])) / (firstBall.mass + secondBall.mass);
        firstBall.speed = [newVelX1, newVelY1]
        secondBall.speed = [newVelX2, newVelY2]

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',48)
    label = largeText.render(text, 1, (255,255,255))
    screen.blit(label, (100,100))
    # pygame.display.flip()

pygame.init()

balls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for _ in range(numberOfBalls):
    ball = Ball([random.randrange(1, maxVal, 1), random.randrange(1, maxVal, 1)], scale = random.uniform(0.5, 1.0))
    balls.add(ball)
    all_sprites.add(ball)

while True:

    clock().tick(FPS)

    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                balls.add(Ball([random.randrange(random.randrange(-1, 1, 1), maxVal, 1), random.randrange(1, maxVal, 1)],scale=random.uniform(0.1, 1.0)))
            # if event.key == pygame.K_DOWN:
            #     balls.pop(balls.__len__() - 1)

    # for ball in balls:
    #     for ball2 in balls:
    #         ball.collide(ball2)
    #     ball.move()

    # for meteorhit in balls:
    #     hits = pygame.sprite.spritecollide(meteorhit, balls, False, pygame.sprite.collide_circle)
    #     for hit in hits:
    #         meteorhit.collide(hit)

    # balls.draw(screen)

    # Update sprites
    all_sprites.update()

    # Render screen
    screen.fill(BLACK)
    message_display("Balls:" + str(balls.__len__()))
    all_sprites.draw(screen)
    # Now flip the display
    pygame.display.flip()

    # screen.blit(background, (0, 0))


