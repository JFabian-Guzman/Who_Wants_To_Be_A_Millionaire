from config.settings import *
from os.path import join
from .State import *
from utils.Box import *

class Instructions(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = Box(self.elements, event_manager)
    self.font_title = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.text = self.font_title.render("Instructions", True, COLORS["AMBER"])
    box_rect = self.box.get_rect()
    self.text_rect = self.text.get_rect(center = (box_rect.centerx, box_rect.top + 75))
    self.instructions = self.font.render(INSTRUCTIONS, True, COLORS["WHITE"] )
    self.instructions_rect = self.instructions.get_rect(center = box_rect.center)

    self.box.set_up_box_event()


  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    self.screen.blit(self.instructions, self.instructions_rect)

  def update(self):
    self.elements.update()