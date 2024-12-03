import os
import pygame


ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_COLOR = (255, 255, 255)

PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_SHOOT_SPEED = 500

SHOT_RADIUS = 5

pause = False

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((screen_width - 10, screen_height - 50), pygame.RESIZABLE)

surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

BC = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BC, (screen_width, screen_height))

FARM = pygame.image.load("assets/farm.png")
FARMLAND = pygame.transform.scale(FARM, (screen_width, screen_height))

APPLE = pygame.image.load("assets/CANNABLIST_APPLE.png")
OPTIONS_WHILE_PLAYING_SCREEN = pygame.transform.scale(APPLE, (screen_width, screen_height))

POTATO = pygame.image.load("assets/POTATO.png")
PAUSE_SCREEN = pygame.transform.scale(POTATO, (screen_width, screen_height))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)



