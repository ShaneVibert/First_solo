import pygame
import random
from constants import *
from entities import Player, screen

player = Player(screen_width, screen_height)
playerx, playery = player.get_position()
player1 = int(playerx)
player2 = int(playery)

class PositionGenerator:
    def __init__(self, margin, min_distance=300):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin
        self.min_distance = min_distance
        self.player_x = player2
        self.player_y = player2

    def get_random_position(self):
        x = random.randint(self.margin, self.screen_width - self.margin)
        y = random.randint(self.margin, self.screen_height - self.margin)
        return x, y

    def is_position_valid(self, x, y,):
        return ((x - self.player_x)**2 + (y - self.player_y)**2)**0.5 >= self.min_distance

    def generate_valid_position(self):
        x, y = self.get_random_position()
        while not self.is_position_valid(x, y):
            x, y = self.get_random_position()
        return x, y
