from config.settings import *
from os.path import join

class Cursor:
  def __init__(self):
    super().__init__()
    self.cursor = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()
    self.screen = pygame.display.get_surface()
    self.x = 0
    self.y = 0 
    self.collision = False

  def draw(self):
      self.screen.blit(self.cursor, (self.x, self.y))

  def check_collision(self, options):
    for option in options:
      if option.rect.collidepoint(self.x, self.y):
        self.cursor = pygame.image.load(join("assets", "img", "hover_cursor.png")).convert_alpha()
        break
      else:
        self.cursor = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()


  def update(self):
    self.x, self.y = pygame.mouse.get_pos()



