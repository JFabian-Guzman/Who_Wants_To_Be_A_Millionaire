from config.settings import *
from os.path import join
from utils.Coin import *

SCORE_POSITION = (WINDOW_WIDTH/2,310)
class Score(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.elements = pygame.sprite.Group()

    self.image = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.rect = self.image.get_rect(center = SCORE_POSITION)

    self.current_level = 0

    self.update_rewards()
    COIN_POSITION = (self.text_rect.right + 20, self.text_rect.centery - 2)
    Coin(COIN_POSITION, self.elements)
    

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.elements.draw(self.screen)
    self.update_rewards()

  def update_rewards(self):
    self.text = TITLE.render(REWARDS[self.current_level], True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def next_level(self):
    self.current_level += 1

  def restart(self):
    self.current_level = 0

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title
