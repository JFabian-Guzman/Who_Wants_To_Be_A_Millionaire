from config.settings import *
from os.path import join
from utils.Button import *

class PodiumBox(pygame.sprite.Sprite):
  def __init__(self, groups, position):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"leaderboard_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=position)
    

  def draw(self):
    self.screen.blit(self.image, self.rect)