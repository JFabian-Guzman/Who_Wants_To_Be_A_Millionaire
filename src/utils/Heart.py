from config.settings import *
from os.path import join

class Heart(pygame.sprite.Sprite):
  def __init__(self, position , group):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img" ,"heart.png")).convert_alpha()
    self.rect = self.image.get_rect(center=position)

  def draw(self):
    self.screen.blit(self.image, self.rect)

  def disable(self):
    self.image = pygame.image.load(join("assets", "img" ,"disable_heart.png")).convert_alpha()