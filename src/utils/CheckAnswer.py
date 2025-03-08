from config.settings import *
from os.path import join

class Check(pygame.sprite.Sprite):
  def __init__(self , position, groups):
    super().__init__(groups)

    self.screen = pygame.display.get_surface()
    self.active_check = pygame.image.load(join("assets", "img" ,"check.png")).convert_alpha()
    self.disable_check = pygame.image.load(join("assets", "img" ,"check_disable.png")).convert_alpha()


    self.image = self.disable_check
    self.rect = self.image.get_rect(center = position)
    self.is_answer = False

  def change_state(self, state):
    self.is_answer = state
    if self.is_answer:
      self.image = self.active_check
    else:
      self.image = self.disable_check
  

  def get_state(self):
    return self.is_answer

  def on_hover(self):
    self.image = self.active_check

  def reset_hover(self):
    if not self.is_answer:
      self.image = self.disable_check