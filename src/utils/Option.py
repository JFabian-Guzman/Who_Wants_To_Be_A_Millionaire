from config.settings import *
from os.path import join

class Option(pygame.sprite.Sprite):
  def __init__(self, text , position, groups):
    super().__init__(groups)

    self.screen = pygame.display.get_surface()

    self.image = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)

    self.display_text = self.wrap_text(text)
    
    self.text = TEXT.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def wrap_text(self, text):
        wrap_text = text
        if len(text) > 24:
            mid = len(text) // 2
            if ord(text[mid]) >= 65 and ord(text[mid]) <= 90 or ord(text[mid]) >= 97 and ord(text[mid]) <= 122:
              wrap_text =  text[:mid] + "-\n" + text[mid:]
            else:
              wrap_text = text[:mid] + "\n" + text[mid:]
        return wrap_text

  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.display_text

  def set_title(self,text):
    self.title = text
    self.display_text = self.wrap_text(text)
    self.text = TEXT.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)



