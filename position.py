import pygame
from constants import *

def get_random_position():
    x = random.randit(MARGIN, screen_width - MARGIN)
    y = random.randit(MARGIN, screen_height - MARGIN)
    return x,y