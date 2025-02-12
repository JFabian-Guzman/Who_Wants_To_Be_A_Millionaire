from config.settings import *
from os.path import join

class Lifeline(pygame.sprite.Sprite):
  def __init__(self, position, icon):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha()
    self.rect = self.image.get_rect(center=position)
    self.icon = pygame.image.load(join("assets", "img" , icon + ".png")).convert_alpha()
    self.icon_rect = self.icon.get_rect(center=self.rect.center)

  def draw_available(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.icon, self.icon_rect)

