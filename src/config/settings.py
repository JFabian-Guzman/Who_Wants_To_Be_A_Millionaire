import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
COLORS = {
  "Blue": "#1A237E",
  "Amber": "#FFC107",
  "GREEN": "#4CAF50",
  "RED": "#F44336",
  "WHITE": "#FFFFFF",
  "BLACK": "#000000"
}

BANNER = {
  "SIZE":  (WINDOW_WIDTH, 50),
}

MENU = [
  {"TITLE": "Play", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 - 50) },
  {"TITLE": "Glossary", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 200)},
  {"TITLE": "Manage Questions", "POSITION": (WINDOW_WIDTH // 2 - 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Instructions", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 - 50)},
  {"TITLE": "Credits", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 75)},
  {"TITLE": "Exit", "POSITION": (WINDOW_WIDTH // 2 + 375, WINDOW_HEIGHT // 2 + 200)}
]

