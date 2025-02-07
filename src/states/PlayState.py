from config.settings import *
from utils.Cursor import *
from .State import *
from utils.Option import *
from utils.Questions import *
from utils.Score import *
from utils.Surrender import *
import json
import random

class Play(State):
  def __init__(self, event_manager,file_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.current_level = 0
    self.question_index = 0
    self.current_lives = 3
    self.click_handled = False
    self.interactive_elements = []
    self.file_manager = file_manager
    for position in GAME:
      self.interactive_elements.append(Option("Option", position, self.elements))
    self.question = Question(self.elements, event_manager)
    self.score = Score("1", (WINDOW_WIDTH/2,310), self.elements)
    self.surrender = Surrender((300,90), self.elements, self.event_manager)
    self.interactive_elements.append(self.surrender)

    # Set up events
    self.question.set_up_question_events()


  def draw(self):
    self.elements.draw(self.screen)
    
  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.update_options()
    self.check_answer()

  def update_options(self):
        option_arr = self.file_manager.get_data()[self.current_level][self.question_index]["options"]
        for i in range (4):
          self.interactive_elements[i].set_title(option_arr[i])

  def generate_random_index(self, *args):
    row_size = len(self.file_manager.get_data()[self.current_level])
    self.question_index = random.randrange(row_size)

  def check_answer(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for i in range (4):
                if self.interactive_elements[i].get_rect().collidepoint(pygame.mouse.get_pos()):
                    if isfile(join("data", "Questions.json")):
                      with open(join("data", "Questions.json"), "r") as file:
                        data = json.load(file)
                        answer = data[self.current_level]["answer"]
                        if(answer.lower() == self.interactive_elements[i].get_title().lower()):
                          print("CORRECTO")
                          self.event_manager.notify("update_level")
                          self.current_level += 1
                        else:
                          print("INCORRECTO")
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

  def update_cursor_state(self):
    for item in self.interactive_elements:
      if item.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break
      else:
        self.event_manager.notify("change_cursor", 'default')

  def set_up_play_events(self):
    self.event_manager.subscribe("update_question", self.generate_random_index)