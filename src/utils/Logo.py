from config.settings import *
from os.path import join

LOGO_HEIGHT = 200
class Logo(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.draw_logo()
    

  def draw_logo(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.image = pygame.image.load(join("assets", "img" ,"logo.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(self.width//2, LOGO_HEIGHT))





