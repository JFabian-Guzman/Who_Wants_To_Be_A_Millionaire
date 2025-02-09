import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
COLORS = {
  "BLUE": "#1A237E",
  "AMBER": "#FFC107",
  "GREEN": "#4CAF50",
  "RED": "#F44336",
  "WHITE": "#FFFFFF",
  "BLACK": "#000000"
}

BANNER = {
  "SIZE":  (WINDOW_WIDTH, 65),
}

MENU = [
  {"TITLE": "Play", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 - 50) },
  {"TITLE": "Glossary", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200)},
  {"TITLE": "Manage Questions", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Instructions", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 - 50)},
  {"TITLE": "Credits", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Exit", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)}
]

GAME = [
  (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 100),
  (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200),
  (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 100),
  (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)
]

REWARDS = ["01", "02" , "03" , "04", "05", "07", "10", "15", "20", "25", "30", "40", "50", "75", "100"]

LAST_LEVEL = 5

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