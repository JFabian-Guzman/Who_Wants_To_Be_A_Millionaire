from config.settings import *
from os.path import join


class NumberBox(pygame.sprite.Sprite):
  def __init__(self, group, position, number: str):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img", "number_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(position))

    self.text = TITLE.render(number, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)

