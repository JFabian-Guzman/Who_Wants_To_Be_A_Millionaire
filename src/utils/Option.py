from config.settings import *
from os.path import join

class Option(pygame.sprite.Sprite):
  def __init__(self, text , position, groups):
    super().__init__(groups)
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.title = text
    self.display_text = self.wrap_text(text)
    self.text = self.font.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def wrap_text(self, text):
        if len(text) > 24:
            mid = len(text) // 2
            if ord(text[mid]) >= 65 and ord(text[mid]) <= 90 or ord(text[mid]) >= 97 and ord(text[mid]) <= 122:
              return text[:mid] + "-\n" + text[mid:]
            else:
              return text[:mid] + "\n" + text[mid:]
        return text

  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title

  def set_title(self,text):
    self.title = text
    self.display_text = self.wrap_text(text)
    self.text = self.font.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)



