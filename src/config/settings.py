import pygame
from pygame.locals import *
from os.path import join
from utils.PathHandler import *

# SIZE
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


# COLORS
COLORS = {
  "BLUE": "#1A237E",
  "AMBER": "#FFC107",
  "GREEN": "#4CAF50",
  "RED": "#F44336",
  "WHITE": "#FFFFFF",
  "BLACK": "#000000",
  "GRAY": (115, 115, 115)
}

# TEXT LENGTH
MAX_LENGTH_OPTIONS = 58
MAX_LENGTH_QUESTION = 128
MAX_NAME_LENGTH = 20

# LIMITS
MAX_CATEGORIES = 10
MAX_CATEGORIES_WARNING = f"You've reached the maximum number of categories ({MAX_CATEGORIES})."


# FONT
PRESS_START_2P = resource_path(join("assets", "fonts", "PressStart2P-Regular.ttf"));
pygame.font.init()  
GIGA_TITLE = pygame.font.Font(PRESS_START_2P, 48)
TITLE = pygame.font.Font(PRESS_START_2P, 20)
SUB_TITLE = pygame.font.Font(PRESS_START_2P, 16)
TEXT = pygame.font.Font(PRESS_START_2P, 12)
SMALL_TEXT = pygame.font.Font(PRESS_START_2P, 9)
TINY_TEXT = pygame.font.Font(PRESS_START_2P, 8)

# MENU OPTIONS
MENU = [
  {"TITLE": "Play", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 - 50) },
  {"TITLE": "Instructions", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 - 50)},
  {"TITLE": "Manage Questions", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Credits", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Leaderboard", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200)},
  {"TITLE": "Exit", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)}
]

# GAME DATA
OPTIONS = ["A","B","C","D"]



# TEXTS

OPTION_MAX_LENGTH_WARNING = f"You've reached the maximum option length of {MAX_LENGTH_OPTIONS} characters"
QUESTION_MAX_LENGTH_WARNING = "You've reached the maximum option length of 128 characters"

INSTRUCTIONS = """
      Read the questions about cultural aspects and 
      choose one of the options displayed on the screen.


      If you answer correctly, you remain in the game and 
      earn points. The number of points awarded depends on 
      the question's difficulty and your response time.


      If you answer incorrectly, you lose a life. If you 
      lose your last life, the game will end 
      and a “Game Over” screen will be displayed.

      
      The goal is to answer 15 questions correctly
      to win the game. You can click on 'Surrender' at 
      any time to claim your points."""

GAMEMODES_INSTRUCTIONS = {
  "PRACTICE" : "No points. Designed to help \n\nyou learn.",
  "EASY": "5 lives/hearts. No score multiplier.",
  "NORMAL":  "3 lives/ hearts. Score multiplied \n\nby 1.5x.",
  "HARD": "1 life/ heart. Score multiplied \n\nby 2x."
}

LIFELINE_INSTRUCTIONS = {
  "SHIELD" : "Incorrect answers won't cost you a life.",
  "50/50": "Removes two incorrect answers.",
  "CHANGE_QUESTION":  "Swap this question for a new one.",
}


DEVELOPER = "José Fabián Guzmán González"

CONTRIBUTORS = """
Universidad De Costa Rica\n\n\nEscuela de Lenguas Modernas


TCU 658 UCR
"""