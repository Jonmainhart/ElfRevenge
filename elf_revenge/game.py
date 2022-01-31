# game.py
# Does all of the game things.

import time
import pygame

from models import Enemy, Hero

from utils import get_random_position, load_sprite, print_text, print_score, score_reader, save_scores, update_scores

class ElfRevenge:
    MIN_ENEMY_DISTANCE = 250
    CONT_MESSAGE = "Press 'S' to Continue"

    # constructor
    def __init__(self):
        self._init_pygame()
        # create a display surface 
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = "Elf's Revenge"
        self.score = 0
        self.high_score = score_reader(".scores")
        
        # game objects
        self.enemies = []
        self.bullets = []
        self.hero = None

        
    def main_loop(self):
        # each frame performs the steps in the loop
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        # one-time initialization 
        pygame.init() # set-up pygame
        pygame.display.set_caption("Elf Revenge") # set the window caption

    def _handle_input(self):
        # handles user input
        self._event_listener()

        self._maneuver()

    def _process_game_logic(self):
        
        self._move_objects()
        self._detect_hero_collisions()
        self._detect_good_shot()
        self._remove_bullets()

        if not self.enemies and self.hero:
            self.message = "You Win!"
            self._end_game()

    def _draw(self):
        # displays the result of the game logic
        self.screen.blit(self.background, (0, 0)) # fill the screen
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen) # draw each object
        
        if self.message: # display messages if applicable

            if time.time() % 20 > 10:
                print_text(self.screen, self.message, self.font, y_offset=0)
                if time.time() % 1 > 0.5:
                    print_text(self.screen, self.CONT_MESSAGE, self.font, y_offset=100, color="yellow")
            elif time.time() % 20 < 10:
                msg = (f"High Score: {self.high_score}")
                print_text(self.screen, msg.strip(), self.font, color="white")
        
        print_score(self.screen, str(self.score), self.font) # always show the score

        pygame.display.flip() # update the display
        self.clock.tick(60) # set FPS to 60

    def _get_game_objects(self):
        game_objects = [*self.enemies, *self.bullets]

        if self.hero:
            game_objects.append(self.hero)
        
        return game_objects
        
    def _set_up(self):
        # creates enemy objects
        # hard coded for 6 - could set easy, medium, hard constants
        for _ in range(6):
            while True:
                position = get_random_position(self.screen) 
                if(position.distance_to(self.hero.position) > self.MIN_ENEMY_DISTANCE):
                    break
            
            self.enemies.append(Enemy(position, self.enemies.append))

    def _reset(self):
        # empties the lists of objects, resets the score, and runs set_up()
        self.enemies = []
        self.bullets = []
        self.message = ""
        self.score = 0
        self.hero = Hero((400, 300), self.bullets.append)
        self._set_up()


    def _event_listener(self):
        # listens for keyboard input
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            # SHOOT
            elif (self.hero and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.hero.shoot()
            # RESET
            elif (not self.hero and event.type == pygame.KEYDOWN and event.key == pygame.K_s) or\
                (not self.enemies and event.type == pygame.KEYDOWN and event.key == pygame.K_s):
                self._reset()

    def _maneuver(self):
        # listens for key presses to move the hero sprite
        is_key_pressed = pygame.key.get_pressed()

        if self.hero:
            if is_key_pressed[pygame.K_RIGHT]:
                self.hero.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.hero.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.hero.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.hero.decelerate()

    def _detect_hero_collisions(self):
        # plays sounds and removes the hero from play if collision detected
        if self.hero:
            for enemy in self.enemies:
                if enemy.collides_with(self.hero):
                    self.hero.explosion_sound.play()
                    self.hero = None
                    self.message = "GAME OVER"
                    self._end_game()
                    break

    def _remove_bullets(self):
        # removes bullets that go beyond the screen - prevents bullets from wrapping
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _move_objects(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

    def _detect_good_shot(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if enemy.collides_with(bullet):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    enemy.split()
                    if self.hero: # only score if the player is still alive
                        self.score += 1
                    break

    def _end_game(self):
        self.high_score = update_scores(self.high_score, self.score)
        save_scores(self.high_score, ".scores")
