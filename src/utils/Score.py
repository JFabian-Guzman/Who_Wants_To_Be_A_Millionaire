from config.settings import *
from os.path import join

class Score(pygame.sprite.Sprite):
  def __init__(self, position, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.current_level = 0
    self.update_rewards()
    self.coin = pygame.image.load(join("assets", "img" ,"coin.png")).convert_alpha()
    self.coin_rect = self.coin.get_rect(midleft = (self.text_rect.right + 20, self.text_rect.centery - 2))
    

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.screen.blit(self.coin, self.coin_rect)
    self.update_rewards()

  def update_rewards(self):
    self.text = self.font.render(REWARDS[self.current_level], True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def next_level(self):
    self.current_level += 1

  def restart(self):
    self.current_level = 0

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title
