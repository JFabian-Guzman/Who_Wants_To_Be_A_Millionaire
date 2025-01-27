from config.settings import *
from os.path import join

class Cursor:
  def __init__(self):
    super().__init__()
    self.default = pygame.image.load(join("assets", "img", "default_cursor.png")).convert_alpha()
    self.select = pygame.image.load(join("assets", "img", "select_cursor.png")).convert_alpha()
    self.screen = pygame.display.get_surface()
    self.x = 0
    self.y = 0 
    self.collision = False

  def draw(self):
      self.screen.blit(self.default, (self.x, self.y))

  def check_collision(self, obj_rect):
    if obj_rect.collidepoint((self.x, self.y)):
      self.collision = True
      # self.screen.blit(self.select, (self.x, self.y))
    else:
      self.collision = False


  def update(self):
    print(self.collision)
    self.x, self.y = pygame.mouse.get_pos()



