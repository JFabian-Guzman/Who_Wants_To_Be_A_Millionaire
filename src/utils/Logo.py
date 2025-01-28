from config.settings import *
from os.path import join

class Logo(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"logo.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, 200))





