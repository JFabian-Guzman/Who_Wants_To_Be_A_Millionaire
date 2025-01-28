from config.settings import *
from os.path import join

class Cursor(pygame.sprite.Sprite):
  def __init__(self,groups):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()
    self.rect = self.image.get_rect()
    self.screen = pygame.display.get_surface()
    self.collision = False

  def check_collision(self, options):
    for option in options:
      if option.rect.collidepoint(pygame.mouse.get_pos()):
        self.image = pygame.image.load(join("assets", "img", "hover_cursor.png")).convert_alpha()
        break
      else:
        self.image = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()


  def update(self):
    self.rect.topleft = pygame.mouse.get_pos()



