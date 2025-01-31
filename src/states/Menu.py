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

  def draw(self):
    self.elements.draw(self.screen)
    self.elements.update()

  def update(self):
    self.cursor.check_collision(self.options)
    
  def test(self, *data):
    print("HOLA, SOY MENU Y MI DATA ES: " , data)

  def set_up_menu_events(self):
    self.event_manager.subscribe('test', self.test)

