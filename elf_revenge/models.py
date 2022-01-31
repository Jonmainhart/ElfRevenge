# object models
import random
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)

class GameObject:
    # base class for all game objects
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position) # center of object - will always be vector
        self.sprite = sprite # the image used to draw object
        self.radius = sprite.get_width() / 2 # calculate the radius as half the width of the sprite
        self.velocity = Vector2(velocity) # updates the position of the object each frame - will always be vector

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius) # offsets the image by the radius for collisions
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
    
    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Hero(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.15
    BULLET_SPEED = 3

    def __init__ (self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.explosion_sound = load_sound("explosion1")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("elf"), Vector2(0))
    
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
    
    def decelerate(self):
        self.velocity -= self.direction * (0.35 * self.ACCELERATION) # rear thrusters are not as strong

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

class Enemy(GameObject):
    
    enemy = {
        1: "gift",
        2: "santa1"
    }

    def __init__(self, position, create_asteroid_callback, size=3):
        kind = random.randint(1, 2)
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25
        }

        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite(self.enemy[kind]), 0 , scale)
        self.explode_sound = load_sound("explosion2")

        super().__init__(position, sprite, get_random_velocity(1, 3))
    
    def split(self):
        self.explode_sound.play()
        if self.size > 1:
            for _ in range(2):
                asteroid = Enemy(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity

