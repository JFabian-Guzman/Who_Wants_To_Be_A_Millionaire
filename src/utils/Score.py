from config.settings import *
from os.path import join

class Score(pygame.sprite.Sprite):
  def __init__(self, text , position, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.title = text
    self.text = self.font.render(text, True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    self.coin = pygame.image.load(join("assets", "img" ,"coin.png")).convert_alpha()
    self.coin_rect = self.coin.get_rect(midleft = (self.text_rect.centerx + 20, self.text_rect.centery - 2))

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.screen.blit(self.coin, self.coin_rect)

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title


