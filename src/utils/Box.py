from config.settings import *
from os.path import join

class Box(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.image = pygame.image.load(join("assets", "img" ,"blue_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(self.width//2, self.height//2))
    self.display_contiue = True
    
  def get_rect(self):
    return self.rect
  
  def updates_position(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.rect = self.image.get_rect(center=(self.width//2, self.height//2))