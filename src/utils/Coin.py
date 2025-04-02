from config.settings import *
from os.path import join


class Coin(pygame.sprite.Sprite):
  def __init__(self, position, group):
    super().__init__(group)
    self.image = pygame.image.load(join("assets", "img", "coin.png")).convert_alpha()
    self.rect = self.image.get_rect(midleft = position)

  def draw(self):
    self.screen.blit(self.coin, self.coin_rect)

  def update_position(self, position):
    self.rect = self.image.get_rect(midleft = position)
