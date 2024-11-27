import pygame
from constants import *
import os


#CONSTANTS
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

player_radius = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 350
PLAYER_COLOR = (255, 255, 255)

PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_SHOOT_SPEED = 500

SHOT_RADIUS = 5

player_image = pygame.image.load("assets/apple.png")


class Player:
    def __init__(self, x, y):
        self.position = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.PLAYER_RADIUS = player_radius
        self.rotation = 0
        self.player_image = player_image

    def draw(self, SCREEN):
        position = (self.position.x - self.PLAYER_RADIUS, self.position.y - self.PLAYER_RADIUS)
        SCREEN.blit(self.player_image, position)



    def update(self, dt, game_paused=None):
        keys = pygame.key.get_pressed()

        if not game_paused:
            if keys[pygame.K_w]:
                self.move(-dt)
            if keys[pygame.K_s]:
                self.move(dt)
            if keys[pygame.K_a]:
                self.move_left(-dt)
            if keys[pygame.K_d]:
                self.move_right(dt)


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        #not applicable to current controls

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def move_left(self, dt):
        self.position -= pygame.Vector2(-1, 0) * PLAYER_SPEED * dt

    def move_right(self, dt):
        self.position += pygame.Vector2(1, 0) * PLAYER_SPEED * dt



