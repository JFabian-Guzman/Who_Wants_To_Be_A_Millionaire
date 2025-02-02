from config.settings import *
from os.path import join
from utils.Cursor import *
from .State import *
from utils.Option import *

class Play(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.current_level = 1
    self.current_lives = 3
    self.click_handled = False
    self.options = []
    for position in GAME:
      self.options.append(Option("game", position, self.elements))

  def draw(self):
    self.elements.draw(self.screen)
    
  def update(self):
    self.elements.update()


