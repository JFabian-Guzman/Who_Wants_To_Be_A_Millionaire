from config.settings import *
from os.path import join

class Option(pygame.sprite.Sprite):
  def __init__(self, text , position, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.title = text
    self.text = self.font.render(text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)


  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title


