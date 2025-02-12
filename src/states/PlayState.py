from config.settings import *
from utils.Cursor import *
from .State import *
from utils.Option import *
from utils.Questions import *
from utils.Score import *
from utils.Surrender import *
from utils.ConfirmModal import *
from utils.SurrederModal import *
import random

class Play(State):
  def __init__(self, event_manager,file_manager):
    super().__init__(event_manager)

    self.save_level = 0
    self.current_level = 0
    self.question_index = 0
    self.current_lives = 1
    self.click_handled = False
    self.display_modal = False
    self.display_surrender_modal = False
    self.options = []
    self.file_manager = file_manager   

    for position in GAME:
      self.interactive_elements.append(Option("Option", position, self.elements))
    self.question = Question(self.elements, event_manager)
    self.score = Score(  self.elements)
    self.surrender = Surrender(self.elements, self.event_manager)
    self.modal = ConfirmModal(self.event_manager)
    self.surrender_modal = SurrenderModal(self.event_manager)

    self.interactive_elements.append(self.surrender)

    # Set up events
    self.question.set_up_question_events()

  def draw(self):
    self.elements.draw(self.screen)

  def update(self):
    self.elements.update()
    if self.display_modal:
      self.modal.draw()
      self.modal.update()
    elif self.display_surrender_modal:
      self.surrender_modal.draw()
      self.surrender_modal.update()
    else:
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
                    self.modal.set_option(i)
                    self.switch_modal()
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

  def reset_game(self, *args):
    self.current_level = 0
    self.score.restart()
    self.current_lives = 1

  def switch_modal(self, *args):
    self.display_modal = not self.display_modal
    self.surrender.set_disable(self.display_modal)

  def validate_answer(self, *args):
    answer = self.file_manager.get_data()[self.current_level][self.question_index]["answer"]
    if(answer.lower() == self.interactive_elements[args[0]].get_title().lower()):
      self.current_level += 1
      self.surrender.set_level(self.current_level)
      if self.current_level % 5 == 0:
        self.save_level = self.current_level

      if self.current_level == LAST_LEVEL:
        self.event_manager.notify("set_state", "win")
        self.event_manager.notify("final_reward", self.current_level - 1)
      else:
        self.update_display_data()
        self.score.next_level()
    else:
      self.current_lives -= 1
      if self.current_lives == 0:
        answer = self.file_manager.get_data()[self.current_level][self.question_index]["answer"]
        self.event_manager.notify("game_over_message", (answer, self.save_level))
        self.event_manager.notify("set_state", "game over")
  
  def switch_surrender_modal(self, *args):
    self.click_handled = True
    self.display_surrender_modal = not self.display_surrender_modal
    self.surrender.switch_modal_display()

  def display_win_screen(self, *args):
    if self.current_level == 0:
      self.event_manager.notify("set_state", "menu")
    else:
      self.event_manager.notify("set_state", "win")
      self.event_manager.notify("final_reward", self.current_level)


  def set_up_play_events(self):
    self.event_manager.subscribe("generate_question", self.update_display_data)
    self.event_manager.subscribe("reset_game", self.reset_game)
    self.event_manager.subscribe("switch_modal", self.switch_modal)
    self.event_manager.subscribe("validate_answer", self.validate_answer)
    self.event_manager.subscribe("display_surrender_modal", self.switch_surrender_modal)
    self.event_manager.subscribe("display_win_screen", self.display_win_screen)