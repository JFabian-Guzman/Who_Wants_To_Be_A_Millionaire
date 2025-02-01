from config.settings import *
from os.path import join
from .State import *

class Glossary(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.current_level = 1
    self.current_lives = 3
    self.click_handled = False
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 30)
    self.text = self.font.render("Glossary Screen", True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH/2  ,WINDOW_HEIGHT/2))

  def draw(self):
    self.screen.blit(self.text, self.text_rect)
    
  def update(self):
    pass


