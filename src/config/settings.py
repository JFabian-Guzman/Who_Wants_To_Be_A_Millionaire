import pygame
from os.path import join

# SIZE
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
BANNER = {
  "SIZE":  (WINDOW_WIDTH, 65),
}

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

# POSTIONS
LEFT_BTN_POSITION = (WINDOW_WIDTH // 2 - 275, WINDOW_HEIGHT // 2 + 185)
RIGHT_BTN_POSITION = (WINDOW_WIDTH // 2 + 275, WINDOW_HEIGHT // 2 + 185)
FLAG_POSITION = (WINDOW_WIDTH/2, 150)
MODAL_POSITION = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
MODAL_BTN_LEFT_POSITION = (WINDOW_WIDTH // 2 - 275, WINDOW_HEIGHT // 2 + 65)
MODAL_BTN_RIGHT_POSITION = (WINDOW_WIDTH // 2 + 275, WINDOW_HEIGHT // 2 + 65)
OPTION_POSITIONS = [
  (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 100),
  (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200),
  (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 100),
  (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)
]

# TEXT LENGTH
MAX_LENGTH_OPTIONS = 48
MAX_LENGTH_QUESTION = 128
MAX_NAME_LENGTH = 20


# FONT
PRESS_START_2P = join("assets", "fonts", "PressStart2P-Regular.ttf")
pygame.font.init()  
GIGA_TITLE = pygame.font.Font(PRESS_START_2P, 48)
TITLE = pygame.font.Font(PRESS_START_2P, 20)
SUB_TITLE = pygame.font.Font(PRESS_START_2P, 16)
TEXT = pygame.font.Font(PRESS_START_2P, 13)

# MENU OPTIONS
MENU = [
  {"TITLE": "Play", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 - 50) },
  {"TITLE": "Leaderboard", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200)},
  {"TITLE": "Manage Questions", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Instructions", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 - 50)},
  {"TITLE": "Credits", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Exit", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)}
]

# GAME DATA

REWARDS = ["0","01", "02" , "03" , "04", "05", "07", "10", "15", "20", "25", "30", "40", "50", "75", "100"]

OPTIONS = ["A","B","C","D"]

LAST_LEVEL = 5


# TEXTS

OPTION_MAX_LENGTH_WARNING = "You've reached the maximum option length of 24 characters"
QUESTION_MAX_LENGTH_WARNING = "You've reached the maximum option length of 128 characters"

INSTRUCTIONS = """
Students should read the questions and choose 

one of the options displayed on the screen.



If the answer is correct, they remain in the game 

and earn more points. The next question is displayed.



If the answer is incorrect, a "Game Over" message 

will appear, and the user will lose their points.



The winner of the game will be the individual 

who answers all 15 questions correctly."""

DEVELOPER = "José Fabián Guzmán González"

CONTRIBUTORS = """
Universidad De Costa Rica


Escuela de Lenguas Modernas


TCU 658 UCR
"""