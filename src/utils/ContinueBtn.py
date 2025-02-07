from config.settings import *
from os.path import join

class ContinueBtn(pygame.sprite.Sprite):
  def __init__(self, position, event_manager):
    super().__init__()
    self.image = pygame.image.load(join("assets", "img" ,"btn.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.text = self.font.render("Continue", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    self.event_manager = event_manager
    self.click_handled = False

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.text, self.text_rect)


  def update(self):
    self.check_click()

  def get_rect(self):
    return self.rect

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
          if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.event_manager.notify("set_state", "game")
          self.click_handled = True
          return
    else:
        self.click_handled = False
