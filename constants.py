import os
import pygame


ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 40
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_COLOR = (255, 255, 255)


PLAYER_SHOOT_COOLDOWN = 0.5
PLAYER_SHOOT_SPEED = 500

SHOT_RADIUS = 5

pause = False

os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_AUDIODRIVER'] = 'pulse'

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((screen_width - 10, screen_height - 50), pygame.RESIZABLE)

MARGIN = 25

surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


FARM = pygame.image.load("assets/farm.png")
FARMLAND = pygame.transform.scale(FARM, (screen_width, screen_height))

APPLE = pygame.image.load("assets/CANNABLIST_APPLE.png")
OPTIONS_WHILE_PLAYING_SCREEN = pygame.transform.scale(APPLE, (screen_width, screen_height))

POTATO = pygame.image.load("assets/POTATO.png")
PAUSE_SCREEN = pygame.transform.scale(POTATO, (screen_width, screen_height))

OVER = pygame.image.load("assets/GAME_OVER.png")
GAME_OVER_SCREEN = pygame.transform.scale(OVER, (screen_width, screen_height))

WIN = pygame.image.load("assets/WINNER.png")
WIN_SCREEN = pygame.transform.scale(WIN, (screen_width, screen_height))

Cover = pygame.image.load("assets/COVER.png")
BG = pygame.transform.scale(Cover, (screen_width, screen_height))

option_A = pygame.image.load("assets/card_one.png")
option_B = pygame.image.load("assets/card_two.png")
option_C = pygame.image.load("assets/card_three.png")

potato_image = pygame.image.load("assets/Penemy.png")

gunshot_sound = pygame.mixer.Sound("sounds/PEW.mp3")
gunshot_sound.set_volume(.05)
level_up_sound = pygame.mixer.Sound("sounds/LEVEL.mp3")
level_up_sound.set_volume(0.3)
potato_death = pygame.mixer.Sound("sounds/dead pototoes.mp3")
potato_death.set_volume(0.1)






def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)





