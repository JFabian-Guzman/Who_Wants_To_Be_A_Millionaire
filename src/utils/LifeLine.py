from config.settings import *
from os.path import join
import random

class Lifeline(pygame.sprite.Sprite):
  def __init__(self, position, icon):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha()
    self.rect = self.image.get_rect(center=position)
    self.icon = pygame.image.load(join("assets", "img" , icon + ".png")).convert_alpha()
    self.icon_rect = self.icon.get_rect(center=self.rect.center)
    self.type = icon
    self.available = True

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.icon, self.icon_rect)

  def disable(self):
    self.image = pygame.image.load(join("assets", "img" ,"lifeline_disable.png")).convert_alpha()
    self.available = False

  def enable(self):
    self.image = pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha()
    self.available = True

  def fifty_fifty_lifeline(self, options, answer):
    if not self.available:
      return
    result = []
    random_option = random.choice(options)
    while random_option == answer or random_option == '':
      random_option = random.choice(options)
    # This keeps the original order of the options
    for option in options:
      if option == answer or option == random_option:
        result.append(option)
      else:
        result.append('')
    return result



  def get_rect(self):
    return self.rect

  def get_type(self):
    return self.type