from config.settings import *
from os.path import join

class GameOverFlag(pygame.sprite.Sprite):
  def __init__(self, position, groups):
    super().__init__(groups)
    
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()

    self.image = pygame.image.load(join("assets", "img" ,"game_over_flag.png")).convert_alpha()
    self.rect = self.image.get_rect(center = (self.width//2, 150))

    self.text = GIGA_TITLE.render("Game Over", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def update_position(self, position):
    self.rect = self.image.get_rect(center = position)
    self.text_rect = self.text.get_rect(center = self.rect.center)