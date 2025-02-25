from config.settings import *
from os.path import join

ADD_POSITION = (WINDOW_WIDTH/2 + 300  ,75)

class AddQuestion(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img" ,"blue_square.png")).convert_alpha()
    self.rect = self.image.get_rect(center = ADD_POSITION)
    self.add_icon = TITLE.render("+", True, COLORS["WHITE"])
    self.add_rect = self.add_icon.get_rect(center= ADD_POSITION)
    

  def update(self):
    self.screen.blit(self.add_icon, self.add_rect)
