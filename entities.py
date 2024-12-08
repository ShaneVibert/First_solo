
import pygame
import random


from constants import *


player_image = pygame.image.load("assets/apple.png")
weapon_image = pygame.image.load("assets/weapon.png")
fully_heart = pygame.image.load("assets/hearty.png")
full_heart = pygame.transform.scale(fully_heart, (100, 100))
halfy_heart = pygame.image.load("assets/healfheart.png")
half_heart = pygame.transform.scale(halfy_heart, (100, 100))



PLAYER_SPEED = 300
PLAYER_RADIUS = 40
player_radius = PLAYER_RADIUS

screen = SCREEN



class Hitbox:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0,0)
        self.radius = radius

    def collides_with(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius

    def move(self, dt):
        self.position += self.velocity * dt

    def resize(self, new_radius):
        self.radius = new_radius

class Player(Hitbox):
    def __init__(self, x, y):
        super().__init__(x, y, radius=30)
        self.position = pygame.Vector2(screen_width / 2, screen_height / 2)
        self.PLAYER_RADIUS = player_radius
        self.rotation = 0
        self.player_image = player_image
        self.health = 6
        self.invincibility_time = 0
        self.invincibility_duration = 2.0
        self.is_invincible = False
        self.max_health = 6
        self.regen_timer = 0
        self.regen_delay = 10
        self.move_modifer = 1

    def take_damage(self):
        if not self.is_invincible:
            self.health -= 1
            self.is_invincible = True
            self.invincibility_time = 0
            self.regen_timer = 0
        return self.health

    def draw_hearts(self, screen):
        heart_x = 10
        heart_y = 800
        for i in range(0, 6, 2):
            if self.health >= i + 2:
                screen.blit(full_heart, (heart_x, heart_y))
            elif self.health == i + 1:
                screen.blit(half_heart, (heart_x, heart_y))
            heart_x += 100

    def draw(self, screen):
        if self.is_invincible:
            if int(pygame.time.get_ticks() / 100) % 2 == 0:  # Blink every 100ms
                position = (self.position.x - self.PLAYER_RADIUS, self.position.y - self.PLAYER_RADIUS)
                screen.blit(self.player_image, position)
        else:
            position = (self.position.x - self.PLAYER_RADIUS, self.position.y - self.PLAYER_RADIUS)
            screen.blit(self.player_image, position)
        self.draw_hearts(screen)

    def update(self, dt, game_paused=None):
        if self.is_invincible:
            self.invincibility_time += dt
            if self.invincibility_time >= self.invincibility_duration:
                self.is_invincible = False
                self.invincibility_time = 0
        keys = pygame.key.get_pressed()

        if not game_paused:
            initial_pos = self.position.copy()
            if keys[pygame.K_w]:
                self.move(-dt * self.move_modifer)
            if keys[pygame.K_s]:
                self.move(dt * self.move_modifer)
            if keys[pygame.K_a]:
                self.move_left(-dt * self.move_modifer)
            if keys[pygame.K_d]:
                self.move_right(dt * self.move_modifer)

        self.regen_timer += dt
        if self.regen_timer >= self.regen_delay:
            self.regen_timer = 0
            if self.health < self.max_health:
                self.health += 1



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

    def get_position(self):
        x = self.position.x + self.PLAYER_RADIUS
        y = self.position.y + self.PLAYER_RADIUS
        return x, y

player = Player(screen_width, screen_height)
x5, y5= player.get_position()


class Potato(Hitbox):
    def __init__(self, radius, position_generator):
        self.position_generator = position_generator
        x, y = self.position_generator.generate_valid_position()
        super().__init__(x, y, radius)
        self.image = potato_image
        self.is_alive = True
        self.move_modifer = 1

    def draw(self, screen):
        screen.blit(self.image, (self.position.x - self.image.get_width() // 2,
                                self.position.y - self.image.get_height() // 2))

    def update(self, dt, target_x, target_y, game_paused = None):
        if not game_paused:
            direction_x = target_x - self.position.x
            direction_y = target_y - self.position.y

            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            self.position.x += direction_x * ((PLAYER_SPEED / 2) * self.move_modifer) * dt
            self.position.y += direction_y * ((PLAYER_SPEED / 2) * self.move_modifer) * dt

    def spawn(self):
        new_x, new_y = self.position_generator.generate_valid_position(x5, y5)
        self.position.x = new_x
        self.position.y = new_y

    def kill(self):
        self.is_alive = False
        return 1

    def get_position(self):
        return self.position.x, self.position.y


class Weapon:
    def __init__(self, player):
        self.shots = []
        self.weapon_image = weapon_image
        self.position = player.position
        self.rotation = 0
        self.shoot_timer = 0
        self.flipped = False
        self.shoot_modifer = 1

    def draw(self, SCREEN, player):
        self.position = player.position
        weapon_image = pygame.transform.flip(self.weapon_image, self.flipped, False)
        rotated_weapon = pygame.transform.rotate(weapon_image, self.rotation)
        weapon_rect = rotated_weapon.get_rect(center=player.position)
        SCREEN.blit(rotated_weapon, weapon_rect)

    def find_closest_potato(self, potatoes):
        closest_potato = None
        min_distance = float('inf')  # Start with a very large number

        for potato in potatoes:
            distance = pygame.Vector2(potato.position - self.position).length()
            if distance < min_distance:
                min_distance = distance
                closest_potato = potato

        return closest_potato

    def shoot_at_target(self, target):
        direction = pygame.Vector2(target.position.x - self.position.x,
                                   target.position.y - self.position.y)

        if direction.length() != 0:
            direction = direction.normalize()

        velocity = direction * PLAYER_SHOOT_SPEED

        shot = Shot(self.position.x, self.position.y)
        shot.velocity = velocity
        self.shots.append(shot)

    def update(self, dt, potatoes):
        keys = pygame.key.get_pressed()

        closest_potato = self.find_closest_potato(potatoes)

        if closest_potato:
            direction = pygame.Vector2(closest_potato.position - self.position)
            angle = direction.angle_to(pygame.Vector2(1, 0))

            if -90 <= angle <= 90:
                self.rotation = angle
                self.flipped = False
            else:
                self.rotation = angle - 180
                self.flipped = True

            if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
                gunshot_sound.play()
                self.shoot_at_target(closest_potato)
                self.shoot_timer = 0.5

        self.shoot_timer = max(0, self.shoot_timer - (dt * self.shoot_modifer))

        for shot in self.shots:
            shot.update(dt)
        self.shots = [shot for shot in self.shots if not shot.is_offscreen()]

    def move(self):
        pass

    def handle_collision(self):
        pass

    def get_position(self):
        x = self.position.x
        y = self.position.y
        return x, y


class Shot(Hitbox):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = PLAYER_SHOOT_SPEED
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def is_offscreen(self):
        return (self.position.x < 0 or self.position.x > screen_width or
                self.position.y < 0 or self.position.y > screen_height)

