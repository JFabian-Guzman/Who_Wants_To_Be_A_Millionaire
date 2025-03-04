from config.settings import *
from os.path import join

class Check(pygame.sprite.Sprite):
  def __init__(self , position, groups):
    super().__init__(groups)

    self.screen = pygame.display.get_surface()

    self.image = pygame.image.load(join("assets", "img" ,"check_disable.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.is_answer = False

  def change_state(self, state):
    self.is_answer = state
    if self.is_answer:
      self.image = pygame.image.load(join("assets", "img" ,"check.png")).convert_alpha()
    else:
      self.image = pygame.image.load(join("assets", "img" ,"check_disable.png")).convert_alpha()
  

  def get_state(self):
    return self.is_answer

  def on_hover(self):
    print("CHECK HOVER")

  def reset_hover(self):
    pass