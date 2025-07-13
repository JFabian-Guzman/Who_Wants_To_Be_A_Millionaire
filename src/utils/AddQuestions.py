from config.settings import *
from os.path import join
from utils.PathHandler import *

class AddQuestion(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.blue_square = pygame.image.load(resource_path(join("assets", "img" ,"blue_square.png"))).convert_alpha()
    self.blue_square_hover = pygame.image.load(resource_path(join("assets", "img" ,"blue_square_hover.png"))).convert_alpha()

    self.image =  self.blue_square
    self.rect = self.image.get_rect(center = (self.width//2 + 300, 75))
    self.add_icon = TITLE.render("+", True, COLORS["WHITE"])
    self.add_rect = self.add_icon.get_rect(center= self.rect.center)
    

  def update(self):
    self.screen.blit(self.add_icon, self.add_rect)

  def on_hover(self):
    self.image = self.blue_square_hover

  def reset_hover(self):
    self.image = self.blue_square

  def update_position(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.rect = self.image.get_rect(center = (self.width//2 + 300, 75))
    self.add_rect = self.add_icon.get_rect(center= self.rect.center)