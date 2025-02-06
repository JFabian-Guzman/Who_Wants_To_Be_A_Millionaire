from config.settings import *

from utils.Cursor import *
from .State import *
from utils.Option import *
from utils.Questions import *
from utils.Score import *
from utils.Surrender import *
import json

class Play(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.current_level = 0
    self.current_lives = 3
    self.click_handled = False
    self.interactive_elements = []
    for position in GAME:
      self.interactive_elements.append(Option("Option", position, self.elements))
    self.question = Question(self.elements, event_manager)
    self.score = Score("1", (WINDOW_WIDTH/2,310), self.elements)
    self.surrender = Surrender((300,90), self.elements, self.event_manager)
    self.interactive_elements.append(self.surrender)

  def draw(self):
    self.elements.draw(self.screen)
    
  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.read_options()

  def read_options(self):
    if isfile(join("data", "Questions.json")):
      with open(join("data", "Questions.json"), "r") as file:
        data = json.load(file)
        option_arr = data[self.current_level]["options"]
        for i in range (4):
          self.interactive_elements[i].set_title(option_arr[i])


  def update_cursor_state(self):
    for item in self.interactive_elements:
      if item.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break
      else:
        self.event_manager.notify("change_cursor", 'default')
