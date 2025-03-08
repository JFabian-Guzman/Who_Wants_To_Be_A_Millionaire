from abc import ABC, abstractmethod
from utils.EventManager import *
from config.settings import *
from utils.TextInput import *

class State(ABC):
  def __init__(self, event_manager: EventManager):
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.event_manager = event_manager
    self.click_handle = False
    self.interactive_elements = []

  @abstractmethod
  def draw(self):
    pass

  @abstractmethod
  def update(self):
    pass

  def listen(self, state):
    self.current_state = state

  def on(self):
    self.draw()
    self.update()

  def set_click_handle(self, isHandle):
    self.click_handled = isHandle

  def update_cursor_state(self):
    hover_detected = False
    for element in self.interactive_elements:
        if element.rect.collidepoint(pygame.mouse.get_pos()):
            if isinstance(element, TextInput):
                element.on_hover()
                self.event_manager.notify("change_cursor", 'text')
                hover_detected = True
            elif not hover_detected:
                element.on_hover()
                self.event_manager.notify("change_cursor", 'hover')
                hover_detected = True
        else:
            element.reset_hover()

    if not hover_detected:
        self.event_manager.notify("change_cursor", 'default')
