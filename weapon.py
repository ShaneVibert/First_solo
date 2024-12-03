import pygame
from player import Player

weapon_image = pygame.image.load("assets/weapon.png")

class Weapon:
    def __init__(self, player):
        self.weapon_image = weapon_image
        self.position = player.position
        self.rotation = 0

    def draw(self, SCREEN, player):
        rotated_weapon = pygame.transform.rotate(self.weapon_image, self.rotation)
        weapon_rect = rotated_weapon.get_rect(center=player.position)
        SCREEN.blit(rotated_weapon, weapon_rect)


    def move(self):
        pass

    def handle_collision(self):
        pass
