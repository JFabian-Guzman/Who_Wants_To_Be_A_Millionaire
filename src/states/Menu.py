from config.settings import *
from os.path import join
from utils.Cursor import *
from utils.Option import *
from utils.Logo import *
from .State import *

class Menu(State):
  def __init__(self, event_manager, cursor):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.cursor = cursor
    self.options = []
    for option in MENU:
      self.options.append(Option(option["TITLE"], option["POSITION"], self.elements))
    self.logo = Logo(self.elements)
    self.click_handled = False

  def draw(self):
    self.elements.draw(self.screen)
    self.elements.update()

  def update(self):
    self.cursor.check_collision(self.options)
    self.verify_click()

  def verify_click(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for option in self.options:
                if option.get_rect().collidepoint(pygame.mouse.get_pos()):
                    print(f"OPTION CLICKED: {option.get_title()}")
                    self.click_handled = True
                    return
    else:
        self.click_handled = False


  def set_up_menu_events(self):
    self.event_manager.subscribe('click', self.verify_click)

