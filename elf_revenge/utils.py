# game utilities
import random

from pygame import Color

from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

def load_sprite(name, with_alpha=True):
    """
    Loads sprite with the name provided. Default behavior is
    with alpha masking. 
    :param name: string
    :param with_alpha: boolean
    """
    # create path to sprite image
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_position(position, surface):
    """
    Provides a position to move the sprite to the opposite side of the screen
    when it moves beyond the border of the screen.
    :param position: Vector2
    :param surface: Vector2
    :return: Vector2
    """
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    """
    Utility to generate a random position within the surface.
    :param surface:
    :return: Vector2
    """
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )

def get_random_velocity(min_speed, max_speed):
    """
    Utility to generate a random velocity and angle.
    :param min_speed: Int
    :param max_speed: Int
    :return: Vector2
    """
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def load_sound(name):
    """
    Utility to load sound files.
    :param name: string
    """
    path = f"assets/sounds/{name}.mp3"
    return Sound(path)

def print_text(surface, text, font, y_offset=0, color=Color("tomato")):
    """
    Displays text in the center of the screen.
    
    :param surface:
    :param text: string
    :param font: Font
    :param y_offset: Int
    :param color: Color
    """
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = (Vector2(surface.get_size()) / 2) + (0, y_offset)

    surface.blit(text_surface, rect)


def print_score(surface, text, font, color=Color("white")):
    """
    Displays the current score on the screen,
    :param surface: 
    :param text: String
    :param font: Font
    :param color: Color
    """
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.topleft = (700, 50)

    surface.blit(text_surface, rect.topleft)

def score_reader(filename):
    """
    Reads the high score from the scores file.
    :param filename: string
    :return: int
    """
    path = f"assets/lib/{filename}"
    high_score = 0

    try:
        with open(path, mode="r", newline="") as scores:
            for s in scores:
                high_score = s
    
    except FileNotFoundError as fnf:
        print(fnf)
    
    except PermissionError as perm:
        print(perm)

    return high_score

def update_scores(high_score, game_score):
    """
    Updates the high score if the game score is higher
    than the existing high score.
    :return: int
    """
    high = int(high_score)
    game = int(game_score)

    if game > high:
        high = game
    
    return high

def save_scores(high_score, filename):
    """
    Overwrites the high score in the filename provided
    with the score provided.
    :param high_score: int
    :param filename: string
    """
    # get the path
    path = f"assets/lib/{filename}"
    # write to the file
    try:
        with open(path, mode="w", newline="") as scores:
            scores.write(str(high_score))
    # close the file
    except FileNotFoundError as fnf:
        print(fnf)

    except PermissionError as perm:
        print(perm)
