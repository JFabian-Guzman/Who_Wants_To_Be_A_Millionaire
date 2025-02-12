from config.settings import *

from .State import *
from utils.Box import *
from utils.Button import *

class Credits(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = Box(self.elements, event_manager)
    box_rect = self.box.get_rect()

    self.text_elements = [
      (TITLE.render("Credits", True, COLORS["AMBER"]), (box_rect.centerx, box_rect.top + 75)),
      (SUB_TITLE.render("Developer", True, COLORS["AMBER"]), (box_rect.centerx, box_rect.top + 125)),
      (SUB_TITLE.render("Contributors", True, COLORS["AMBER"]), (box_rect.centerx, box_rect.top + 225)),
      (TEXT.render(DEVELOPER, True, COLORS["WHITE"]), (box_rect.centerx, box_rect.top + 175)),
      (TEXT.render(CONTRIBUTORS, True, COLORS["WHITE"]), (box_rect.centerx, box_rect.top + 300))
    ]
    
    self.back_btn = Button((box_rect.midleft[0] + 170, box_rect.midleft[1] + 190), event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    for text_surface, position in self.text_elements:
      text_rect = text_surface.get_rect(center=position)
      self.screen.blit(text_surface, text_rect)
    self.back_btn.draw()

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()

  def check_click(self):
      if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
          self.back_btn.check_notify_state("menu")
          self.click_handled = True
      else:
          self.click_handled = False
