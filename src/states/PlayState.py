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
    self.file_manager = file_manager
    for position in GAME:
      self.interactive_elements.append(Option("Option", position, self.elements))
    self.question = Question(self.elements, event_manager)
    self.score = Score( (WINDOW_WIDTH/2,310), self.elements)
    self.surrender = Surrender((300,90), self.elements, self.event_manager)
    self.interactive_elements.append(self.surrender)
    self.options = []

    # Set up events
    self.question.set_up_question_events()

  def draw(self):
    self.elements.draw(self.screen)

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.display_options()
    self.check_answer()

  def display_options(self):
    for i in range (4):
      self.interactive_elements[i].set_title(self.options[i])

  def generate_random_index(self):
    row_size = len(self.file_manager.get_data()[self.current_level])
    self.question_index = random.randrange(row_size)

  def update_display_data(self, *args):
    self.generate_random_index()
    self.options = self.file_manager.get_data()[self.current_level][self.question_index]["options"]
    question = self.file_manager.get_data()[self.current_level][self.question_index]["question"]
    self.event_manager.notify("change_question", question)

  def check_answer(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for i in range (4):
                if self.interactive_elements[i].get_rect().collidepoint(pygame.mouse.get_pos()):
                    answer = self.file_manager.get_data()[self.current_level][self.question_index]["answer"]
                    if(answer.lower() == self.interactive_elements[i].get_title().lower()):
                      print("CORRECTO")
                      self.current_level += 1
                      self.update_display_data()
                      self.score.next_level()
                    else:
                      print("INCORRECTO")
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

  def reset_game(self, *args):
    self.current_level = 0

  def set_up_play_events(self):
    self.event_manager.subscribe("generate_question", self.update_display_data)
    self.event_manager.subscribe("reset_game", self.reset_game)