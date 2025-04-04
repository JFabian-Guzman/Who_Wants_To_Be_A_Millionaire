from config.settings import *
from os.path import join

ADD_POSITION = (WINDOW_WIDTH/2 + 300  ,75)

class AddQuestion(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.blue_square = pygame.image.load(join("assets", "img" ,"blue_square.png")).convert_alpha()
    self.blue_square_hover = pygame.image.load(join("assets", "img" ,"blue_square_hover.png")).convert_alpha()

    self.image =  self.blue_square
    self.rect = self.image.get_rect(center = ADD_POSITION)
    self.add_icon = TITLE.render("+", True, COLORS["WHITE"])
    self.add_rect = self.add_icon.get_rect(center= ADD_POSITION)
    

  def update(self):
    self.screen.blit(self.add_icon, self.add_rect)

  def on_hover(self):
    self.image = self.blue_square_hover

  def reset_hover(self):
    self.image = self.blue_square