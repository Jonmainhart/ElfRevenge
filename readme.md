# Elf's Revenge
Santa has gone too far and the elves have had enough! Help Chad the Elf destroy all of the evil Santa clones and exploding presents before it's too late!

*Elf's Revenge* is an *Asteroids* clone written in Python. Based on [this tutorial](https://realpython.com/asteroids-game-python "Real Python - Build an Asteroids Game with Python").

# Installation
Download this repository and run from your command line with `python3 elf_revenge`. 
This game requires Python 3.9 and Pygame 2.0.

# Game Play
Shoot as many Santa Clones and Bad Gifts as possible without getting hit.

⬆️ to move forward
⬇️ to move backward
⬅️ and ➡️ to rotate
Space to shoot

Press "S" to start each new game.

## Why I Made This Project
1. Try PyGame
2. Get more comfortable with virtual environments in Python
3. Do something for the fun of it
4. Get more comfortable with project structure

## Things I Changed from the Tutorial
1. Added a score counter in the corner
2. Added a 'Reset' key to restart the game
3. Added Explosion sounds when each object is shot and when Chad is destroyed
4. Added Reverse - Chad can move backwards at a fraction of forward speed
5. Added random enemy generation - picks one of two sprites - easily expandable to more sprites
6. Added persistent high score read in from and written to a file
7. Refactored some of the methods from the tutorial to reduce complexity
8. Many different sprites are included - create your own variations
~~9. Added lots of comments to explain what is happening for future clarity~~ TODO

## Structure
ElfRevenge/
|
|__ assets/
|   |
|   |__ lib/
|   |   |__ .scores
|   |
|   |__ sounds/
|   |   |__ explosion1.mp3
|   |   |__ explosion2.mp3
|   |   |__ laser.mp3 
|   |
|   |__ sprites/
|       |__ asteroid.png
|       |__ bullet.png
|       |__ coronavirus.png
|       |__ elf.png
|       |__ gift.png
|       |__ santa1.png
|       |__ space.png
|       |__ spaceship.png
|
|__ elf_revenge/
|   |__ __main__.py
|   |__ game.py
|   |__ models.py
|   |__ utils.py
|
|__ requirements.txt
