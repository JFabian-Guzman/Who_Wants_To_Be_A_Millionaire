from config.settings import *
from os.path import join


class LevelBox(pygame.sprite.Sprite):
  def __init__(self, group, position, number: str):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img", "number_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(position))
    self.number = number
    self.text = TITLE.render(number, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def get_number(self):
    return self.number

  def on_hover(self):
    print("LEVEL HOVER")

  def reset_hover(self):
    pass
