import pygame, sys
import os
from button import Button
from constants import *
from player import Player
from weapon import Weapon

pygame.display.set_caption("Menu")
game_paused = False
options_paused = False



def pause():

    global game_paused
    game_paused = not game_paused
    screen = SCREEN
    screen.blit(PAUSE_SCREEN, (0, 0))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()





def play():
    pygame.init()
    screen = SCREEN
    clock = pygame.time.Clock()
    player = Player(screen_width / 2, screen_height / 2)
    weapon = Weapon(player)
    dt = 0
    elapsed_seconds = 0

    running = True

    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                
        if not game_paused and not options_paused:
            dt = clock.tick(60) / 1000
            player.update(dt)
            elapsed_seconds += dt

            SCREEN.blit(FARMLAND, (0, 0))
            player.draw(screen)
            weapon.draw(screen, player)

            elapsed_time = int(elapsed_seconds)
            font = pygame.font.Font(None, 72)
            text_surface = font.render(str(elapsed_time), True,(255, 255, 255))
            screen.blit(text_surface, (50, 50))



        if game_paused:

            dt = 0

            PAUSE_MOUSE_POS = pygame.mouse.get_pos()

            SURE_TEXT = Button(image=None, pos=(screen_width / 2, screen_height / 7),
                               text_input="PAUSED", font=get_font(145), base_color="white", hovering_color="white")

            YES_TEXT = Button(image=None, pos=(screen_width / 7, screen_height / 1.4),
                              text_input="QUIT", font=get_font(45), base_color="white", hovering_color="green")

            OPTIONS_TEXT = Button(image=None, pos=(screen_width / 7, screen_height / 1.75),
                             text_input="OPTIONS", font=get_font(45), base_color="white", hovering_color="green")

            NO_TEXT = Button(image=None, pos=(screen_width / 7, screen_height / 2.4),
                             text_input="RESUME", font=get_font(45), base_color="white", hovering_color="green")

            SURE_TEXT.changeColor(PAUSE_MOUSE_POS)
            YES_TEXT.changeColor(PAUSE_MOUSE_POS)
            NO_TEXT.changeColor(PAUSE_MOUSE_POS)
            OPTIONS_TEXT.changeColor(PAUSE_MOUSE_POS)

            SURE_TEXT.update(SCREEN)
            NO_TEXT.update(SCREEN)
            YES_TEXT.update(SCREEN)
            OPTIONS_TEXT.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NO_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        pause()
                    if YES_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        pause()
                        main_menu()
                    if OPTIONS_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        options_while_play()
                        pause()
        if options_paused:

            player.update(0)

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            OPTIONS_TEXT = get_font(45).render("Make the game yours ;)", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 14.4))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(screen_width / 2, screen_height / 1.1),
                                  text_input="BACK", font=get_font(45), base_color="white", hovering_color="red")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        options_while_play()
                        pause()



        pygame.display.flip()

def options_while_play():
    pass
    global options_paused
    options_paused = not options_paused

    screen = SCREEN
    SCREEN.blit(OPTIONS_WHILE_PLAYING_SCREEN, (0, 0))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()







def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(45).render("Make the game yours ;)", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 14.4))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(screen_width / 2, screen_height / 1.1),
                              text_input="BACK", font=get_font(45), base_color="white", hovering_color="red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def sure():
    while True:
        SURE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        SURE_TEXT = Button(image=None , pos=(screen_width / 2,screen_height / 2.88),
                           text_input="GIVING UP :P", font=get_font(45), base_color="white", hovering_color="red")
        YES_TEXT = Button(image=None , pos=(screen_width / 2.7,screen_height / 2.1),
                          text_input="YES", font=get_font(45), base_color="white", hovering_color="green")
        NO_TEXT = Button(image=None , pos=(screen_width / 1.6,screen_height / 2.1),
                         text_input="NO", font=get_font(45), base_color="white", hovering_color="green")
        SURE_TEXT.changeColor(SURE_MOUSE_POS)
        YES_TEXT.changeColor(SURE_MOUSE_POS)
        NO_TEXT.changeColor(SURE_MOUSE_POS)

        SURE_TEXT.update(SCREEN)
        NO_TEXT.update(SCREEN)
        YES_TEXT.update(SCREEN)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NO_TEXT.checkForInput(SURE_MOUSE_POS):
                    main_menu()
                if YES_TEXT.checkForInput(SURE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Devoring", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, screen_height / 7.2))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(screen_width / 2, screen_height / 2.88),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(screen_width / 2, screen_height / 1.8),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(screen_width / 2, screen_height / 1.31),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    pygame.quit()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sure()

        pygame.display.update()


main_menu()