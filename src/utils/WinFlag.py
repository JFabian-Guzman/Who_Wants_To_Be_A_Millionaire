from config.settings import *
from os.path import join

class WinFlag(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.screen = pygame.display.get_surface()

    self.image = pygame.image.load(join("assets", "img" ,"win_flag.png")).convert_alpha()
    self.rect = self.image.get_rect(center = FLAG_POSITION)

    self.text = GIGA_TITLE.render("Congratulations!", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    
  def update(self):
    self.screen.blit(self.text, self.text_rect)

