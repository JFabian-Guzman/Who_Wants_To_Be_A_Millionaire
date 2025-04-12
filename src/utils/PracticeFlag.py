from config.settings import *
from os.path import join

class PracticeFlag(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.screen = pygame.display.get_surface()

    self.image = pygame.image.load(join("assets", "img" ,"practice_flag.png")).convert_alpha()
    self.rect = self.image.get_rect(center = FLAG_POSITION)

    self.text = GIGA_TITLE.render("Practice Complete!", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    
  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def update_position(self, position):
    self.rect = self.image.get_rect(center = position)
    self.text_rect = self.text.get_rect(center = self.rect.center)

