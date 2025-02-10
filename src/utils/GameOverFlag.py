from config.settings import *
from os.path import join

class GameOverFlag(pygame.sprite.Sprite):
  def __init__(self, position, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img" ,"game_over_flag.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 48)
    self.text = self.font.render("Game Over", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)

