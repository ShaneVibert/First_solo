import pygame, sys
import os

from pygame.examples.music_drop_fade import volume

from button import Button
from entities import Potato, Player, Weapon, Shot, Hitbox
from position import PositionGenerator
from constants import *


pygame.display.set_caption("Menu")
leveled_up = False
game_paused = False
options_paused = False
position_generator = PositionGenerator(20)
potatoes = []
screen = SCREEN
xp = 0
xp_limit = 10
xp_gain = 1
volume_level = 5
max_volume = 10
scaled_volume = volume_level / max_volume
pygame.init()
pygame.mixer.init()

def spawn_new_potato():
    new_potato = Potato(PLAYER_RADIUS, position_generator)
    potatoes.append(new_potato)

def win():
    screen.blit(WIN_SCREEN, (0, 0))
    QUIT_POS = pygame.mouse.get_pos()

    GIVING_UP_TEXT = Button(image=None, pos=(screen_width / 2, screen_height / 2.88),
                            text_input="GIVING UP :P", font=get_font(45), base_color="white", hovering_color="red")
    YES_TEXT = Button(image=None, pos=(screen_width / 2.7, screen_height / 2.1),
                      text_input="YES", font=get_font(45), base_color="white", hovering_color="green")
    NO_TEXT = Button(image=None, pos=(screen_width / 1.6, screen_height / 2.1),
                     text_input="NO", font=get_font(45), base_color="white", hovering_color="green")
    GIVING_UP_TEXT.changeColor(QUIT_POS)
    YES_TEXT.changeColor(QUIT_POS)
    NO_TEXT.changeColor(QUIT_POS)

    GIVING_UP_TEXT.update(screen)
    NO_TEXT.update(screen)
    YES_TEXT.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if NO_TEXT.checkForInput(QUIT_POS):
                main_menu()
            if YES_TEXT.checkForInput(QUIT_POS):
                pygame.quit()
                sys.exit()

    pygame.display.update()

def game_over():
    pygame.mixer.music.load("sounds/GAME OVER SONG.mp3")
    pygame.mixer.music.play(loops=-1)
    while True:
        screen.blit(GAME_OVER_SCREEN, (0, 0))
        QUIT_POS = pygame.mouse.get_pos()

        GIVING_UP_TEXT = Button(image=None , pos=(screen_width / 2,screen_height / 2.88),
                           text_input="GIVING UP :P", font=get_font(45), base_color="white", hovering_color="red")
        YES_TEXT = Button(image=None , pos=(screen_width / 2.7,screen_height / 2.1),
                          text_input="YES", font=get_font(45), base_color="white", hovering_color="green")
        NO_TEXT = Button(image=None , pos=(screen_width / 1.6,screen_height / 2.1),
                         text_input="NO", font=get_font(45), base_color="white", hovering_color="green")
        GIVING_UP_TEXT.changeColor(QUIT_POS)
        YES_TEXT.changeColor(QUIT_POS)
        NO_TEXT.changeColor(QUIT_POS)

        GIVING_UP_TEXT.update(screen)
        NO_TEXT.update(screen)
        YES_TEXT.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NO_TEXT.checkForInput(QUIT_POS):
                    pygame.mixer.music.stop()
                    main_menu()
                if YES_TEXT.checkForInput(QUIT_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def level_up():
    global xp
    global game_paused
    global leveled_up
    leveled_up = True

    for event in pygame.event.get():
        level_up_mos = pygame.mouse.get_pos()  # Fixed mouse position tracking
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()




def pause():

    global game_paused
    game_paused = not game_paused
    screen.blit(PAUSE_SCREEN, (0, 0))





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()





def play():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds/Game Music.mp3")
    pygame.mixer.music.play(loops=-1)
    clock = pygame.time.Clock()
    player = Player(screen_width, screen_height)
    potato = Potato(PLAYER_RADIUS, position_generator)
    weapon = Weapon(player)
    elapsed_seconds = 0
    spawn_time = 1
    time_since_last_spawn = 0
    spawner_counter = 0
    global game_paused, leveled_up, xp, xp_limit, xp_gain, volume_level

    running = True

    while running:
        dt = clock.tick(172) / 1000
        print(xp)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                    game_paused = True

        if not game_paused and not leveled_up:
            x, y = player.get_position()
            shot = Shot(x, y)
            screen.blit(FARMLAND, (0, 0))
            player.update(dt)
            weapon.update(dt, potatoes)

            elapsed_seconds += dt

            time_since_last_spawn += dt

            for shot in weapon.shots[:]:
                shot.update(dt)
                shot.draw(screen)

                for potato in potatoes[:]:
                    if shot.collides_with(potato):
                        potato_death.play()
                        xp += xp_gain
                        potatoes.remove(potato)
                        weapon.shots.remove(shot)
                        break
            for potato in potatoes[:]:
                if player.collides_with(potato):
                    player.take_damage()
                    potato_death.play()
                    potatoes.remove(potato)
                    print(player.health)
                    if player.health <= 0:
                        game_over()
                        xp = 0
                        weapon.shoot_modifer = 1
                        player.move_modifer = 1
                        xp_limit = 10
                        xp_gain = 1
                    else:
                        break

            if time_since_last_spawn >= spawn_time:
                spawn_new_potato()
                time_since_last_spawn = 0

            for potato in potatoes:
                potato.update(dt, x, y)
                potato.draw(screen)

            player.draw(screen)
            weapon.draw(screen, player)

            spawner_counter += dt
            if spawn_time >= 0.3:
                if spawner_counter >= 20:
                    potato.move_modifer += 0.15
                    spawn_time *= 0.8
                    spawner_counter = 0



            if xp >= xp_limit:
                leveled_up = True
                level_up()
                level_up_sound.play()



            elapsed_time = int(elapsed_seconds)
            font = pygame.font.Font(None, 72)
            text_surface = font.render(str(elapsed_time), True,(255, 255, 255))
            screen.blit(text_surface, (50, 50))

            if elapsed_time >= 600:
                win()

        if leveled_up:
            dt = 0.08
            level_up_mos = pygame.mouse.get_pos()

            screen.blit(option_A, (screen_width / -2.58, screen_height / -5))
            screen.blit(option_B, (screen_width / -14, screen_height / -5))
            screen.blit(option_C, (screen_width / 4.15, screen_height / -5))

            weapon_fire_rate_square = pygame.draw.rect(screen, (0, 0, 0),(screen_width / 24, screen_height / 1081, 453, 1084), 1)
            player_speed_square = pygame.draw.rect(screen, (0, 0, 0),(screen_width / 2.795, screen_height / 1081, 453, 1084), 1)
            xp_rate_square = pygame.draw.rect(screen, (0, 0, 0), (screen_width / 1.494, screen_height / 1081, 453, 1084),1)

            weapon_fire_rate = Button(image=None, pos=(screen_width / 6.1, screen_height / 7),
                                      text_input="Fire Rate Up", font=get_font(20), base_color="white",
                                      hovering_color="white")
            player_speed = Button(image=None, pos=(screen_width / 2.1, screen_height / 7),
                                  text_input="Player Speed Up", font=get_font(20), base_color="white",
                                  hovering_color="white")
            xp_rate = Button(image=None, pos=(screen_width / 1.28, screen_height / 7),
                             text_input="Xp Rate Up", font=get_font(20), base_color="white", hovering_color="white")

            # Detect collision and display the potato image
            if weapon_fire_rate_square.collidepoint(level_up_mos):
                # Draw the potato image at a specified position
                screen.blit(potato_image, (screen_width / 7, screen_height / 1.2))
            elif player_speed_square.collidepoint(level_up_mos):
                screen.blit(potato_image, (screen_width / 2.18, screen_height / 1.2))
            elif xp_rate_square.collidepoint(level_up_mos):
                screen.blit(potato_image, (screen_width / 1.29, screen_height / 1.2))


            weapon_fire_rate.update(screen)
            player_speed.update(screen)
            xp_rate.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if weapon_fire_rate_square.collidepoint(level_up_mos):
                        leveled_up = False
                        xp = 0
                        xp_limit += 1.1
                        weapon.shoot_modifer += 0.05
                    if player_speed_square.collidepoint(level_up_mos):
                        leveled_up = False
                        xp = 0
                        xp_limit += 10
                        player.move_modifer += 0.05
                    if xp_rate_square.collidepoint(level_up_mos):
                        leveled_up = False
                        xp = 0
                        xp_limit *= 1.1
                        xp_gain += 0.3




        if game_paused:

            dt = 0.08


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

            SURE_TEXT.update(screen)
            NO_TEXT.update(screen)
            YES_TEXT.update(screen)
            OPTIONS_TEXT.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NO_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        pause()
                        game_paused = False
                    if YES_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        pause()
                        main_menu()
                    if OPTIONS_TEXT.checkForInput(PAUSE_MOUSE_POS):
                        options_while_play()
                        pause()
        if options_paused:

            dt = 0

            screen.blit(OPTIONS_WHILE_PLAYING_SCREEN, (0, 0))

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            OPTIONS_TEXT = get_font(45).render("Make the game yours ;)", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 14.4))
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(screen_width / 2.05, screen_height / 1.1),
                                  text_input="BACK", font=get_font(45), base_color="white", hovering_color="red")
            left_volume = Button(image=None, pos=(screen_width / 3.1, screen_height / 6.55),
                                 text_input="<", font=get_font(60), base_color="white", hovering_color="red")
            right_volume = Button(image=None, pos=(screen_width / 1.545, screen_height / 6.55),
                                  text_input=">", font=get_font(60), base_color="white", hovering_color="red")
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            left_volume.changeColor(OPTIONS_MOUSE_POS)
            right_volume.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(screen)
            left_volume.update(screen)
            right_volume.update(screen)

            side = 50
            margin = 5
            start_x = screen_width / 2.93
            y_position = screen_height / 8

            for i in range(max_volume):
                x_position = start_x + i * (side + margin)
                square = pygame.Rect(x_position, y_position, side, side)

                if i < volume_level:
                    pygame.draw.rect(screen, (255, 255, 255), square)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), square, 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        options_while_play()
                        pause()
                    if left_volume.checkForInput(OPTIONS_MOUSE_POS):
                        volume_level -= 1
                        if volume_level < 0:
                            volume_level = 0
                    if right_volume.checkForInput(OPTIONS_MOUSE_POS):
                        volume_level += 1
                        if volume_level > max_volume:
                            volume_level = max_volume
                pygame.mixer.music.set_volume(volume_level * 0.01)



        pygame.display.flip()

def options_while_play():
    pass
    global options_paused
    options_paused = not options_paused

    screen.blit(OPTIONS_WHILE_PLAYING_SCREEN, (0, 0))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()







def options():
    global volume_level
    while True:
        screen.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()


        OPTIONS_TEXT = get_font(45).render("Make the game yours ;)", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 14.4))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(screen_width / 2.05, screen_height / 1.1),
                              text_input="BACK", font=get_font(45), base_color="white", hovering_color="red")
        left_volume = Button(image=None, pos=(screen_width / 3.1, screen_height / 6.55),
                              text_input="<", font=get_font(60), base_color="white", hovering_color="red")
        right_volume = Button(image=None, pos=(screen_width / 1.545, screen_height / 6.55),
                              text_input=">", font=get_font(60), base_color="white", hovering_color="red")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        left_volume.changeColor(OPTIONS_MOUSE_POS)
        right_volume.changeColor(OPTIONS_MOUSE_POS)


        OPTIONS_BACK.update(screen)
        left_volume.update(screen)
        right_volume.update(screen)

        side = 50
        margin = 5
        start_x = screen_width / 2.93
        y_position = screen_height / 8

        for i in range(max_volume):
            x_position = start_x + i * (side + margin)
            square = pygame.Rect(x_position, y_position, side, side)

            if i < volume_level:
                pygame.draw.rect(screen, (255, 255, 255), square)
            else:
                pygame.draw.rect(screen, (255, 255, 255), square, 2)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if left_volume.checkForInput(OPTIONS_MOUSE_POS):
                    volume_level -= 1
                    if volume_level < 0:
                        volume_level = 0
                if right_volume.checkForInput(OPTIONS_MOUSE_POS):
                    volume_level += 1
                    if volume_level > max_volume:
                        volume_level = max_volume
            pygame.mixer.music.set_volume(volume_level * 0.01)

        pygame.display.update()

def quit():
    while True:
        QUIT_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        GIVING_UP_TEXT = Button(image=None , pos=(screen_width / 2,screen_height / 2.88),
                           text_input="GIVING UP :P", font=get_font(45), base_color="white", hovering_color="red")
        YES_TEXT = Button(image=None , pos=(screen_width / 2.7,screen_height / 2.1),
                          text_input="YES", font=get_font(45), base_color="white", hovering_color="green")
        NO_TEXT = Button(image=None , pos=(screen_width / 1.6,screen_height / 2.1),
                         text_input="NO", font=get_font(45), base_color="white", hovering_color="green")
        GIVING_UP_TEXT.changeColor(QUIT_POS)
        YES_TEXT.changeColor(QUIT_POS)
        NO_TEXT.changeColor(QUIT_POS)

        GIVING_UP_TEXT.update(screen)
        NO_TEXT.update(screen)
        YES_TEXT.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NO_TEXT.checkForInput(QUIT_POS):
                    main_menu()
                if YES_TEXT.checkForInput(QUIT_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    pygame.mixer.music.load("sounds/MAIN_MENU.mp3")
    pygame.mixer.music.play(loops=-1)
    while True:
        screen.blit(BG, (0, 0))

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

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        OPTIONS_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)

        PLAY_BUTTON.update(screen)
        OPTIONS_BUTTON.update(screen)
        QUIT_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    play()
                    pygame.quit()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit()

        pygame.display.update()


main_menu()