from config.settings import *
from os.path import join
from utils.Option import *
from utils.Logo import *
from .State import *

class Menu(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.options = []
    for option in MENU:
      option = Option(option["TITLE"], option["POSITION"], self.elements)
      self.options.append(option)
      self.interactive_elements.append(option)
    self.logo = Logo(self.elements)
    self.click_handled = False

  def draw(self):
    self.elements.draw(self.screen)

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.update_user_click()

  def update_user_click(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for option in self.options:
                if option.get_rect().collidepoint(pygame.mouse.get_pos()):
                    if(option.get_title().lower() != 'exit'):
                      self.event_manager.notify("set_state", option.get_title().lower())
                    else:
                      self.event_manager.notify("stop_game")
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

