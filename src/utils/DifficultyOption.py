from config.settings import *
from os.path import join

class DifficultyOption(pygame.sprite.Sprite):
  def __init__(self, text , position, groups, color=''):
    super().__init__(groups)

    self.screen = pygame.display.get_surface()

    self.image = pygame.image.load(join("assets", "img" ,"option" + color +".png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)

    self.overlay = pygame.Surface(self.image.get_size())
    self.overlay.fill((0, 0, 0))
    self.overlay.set_alpha(128)

    self.display_text = self.wrap_text(text)
    self.is_active = False

    self.text = TEXT.render(self.display_text, True, COLORS["BLACK"])
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

  def draw_overlay(self):
    self.screen.blit(self.overlay, self.rect)

  def update(self):
    self.screen.blit(self.text, self.text_rect)

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.display_text
  
  def get_active(self):
    return self.is_active
  
  def set_active(self, state):
    self.is_active = state

  def on_hover(self):
    print("DIFFICULTY OPTION HOVER")

  def reset_hover(self):
    pass

  def set_title(self,text):
    self.title = text
    self.display_text = self.wrap_text(text)
    self.text = TEXT.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)



