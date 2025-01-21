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

MENU = [
  {"TITLE": "Play", "POSITION": (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)},
  {"TITLE": "Glossary", "POSITION": (WINDOW_HEIGHT // 2 + 50, 100)},
  {"TITLE": "Manage Questions", "POSITION": (WINDOW_HEIGHT // 2 + 100, 100)},
  {"TITLE": "Exit", "POSITION": (WINDOW_HEIGHT // 2 + 150, 100)}
]

