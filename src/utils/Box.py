from config.settings import *
from os.path import join

class Box(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"blue_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.display_contiue = True
    
  def get_rect(self):
    return self.rect