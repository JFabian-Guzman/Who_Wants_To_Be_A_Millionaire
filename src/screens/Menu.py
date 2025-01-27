from config.settings import *
from os.path import join
from utils.Cursor import *
from utils.Option import *

class Menu():
  def __init__(self, cursor):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.cursor = cursor

  def logo(self):
    logo = pygame.image.load(join("assets", "img" ,"logo.png")).convert_alpha()
    logo_rect = logo.get_rect(center=(WINDOW_WIDTH//2, 200))
    self.screen.blit(logo, logo_rect)

  def draw(self):
    self.logo()
    options = []
    for option in MENU:
        options.append(Option(option["TITLE"], option["POSITION"]))
    for option in options:
        option.draw()


