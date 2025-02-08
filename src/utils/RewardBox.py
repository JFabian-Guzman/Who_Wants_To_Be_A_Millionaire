from config.settings import *
from os.path import join
from utils.BackBtn import *
from utils.Button import *

class RewardsBox(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"rewards_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    

  def get_rect(self):
    return self.rect