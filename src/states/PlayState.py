from config.settings import *
from utils.Cursor import *
from .State import *
from utils.Option import *
from utils.Questions import *
from utils.Score import *
from utils.Surrender import *
from utils.ConfirmModal import *
from utils.SurrederModal import *
from utils.LifeLine import *
from utils.Heart import *
import random

LIFELINE_1_POSITION = (WINDOW_WIDTH/2 , WINDOW_HEIGHT/2 - 275)
LIFELINE_2_POSITION = (WINDOW_WIDTH/2 + 75, WINDOW_HEIGHT/2 - 275)
LIFELINE_3_POSITION = (WINDOW_WIDTH/2 - 75, WINDOW_HEIGHT/2 - 275)

class Play(State):
  def __init__(self, event_manager,file_manager):
    super().__init__(event_manager)

    self.save_level = 0
    self.current_level = 0
    self.question_index = 0
    self.total_lives = 0
    self.lives = 0
    self.number_questions = 0
    self.correct_answers = 0
    self.wrong_answer = 0
    self.click_handled = False
    self.display_modal = False
    self.display_surrender_modal = False
    self.active_shield = False
    self.practice_mode = False
    self.answer = ""
    self.difficulty = ""
    self.question = ""
    self.options = []
    self.lifelines = []
    self.file_manager = file_manager  

    for position in OPTION_POSITIONS:
      self.interactive_elements.append(Option("", position, self.elements))
    self.question = Question(self.elements, event_manager)
    self.score = Score(self.elements)
    self.surrender = Surrender(self.elements, self.event_manager)
    self.modal = ConfirmModal(self.event_manager)
    self.surrender_modal = SurrenderModal(self.event_manager)
    self.shield_lifeline = Lifeline(LIFELINE_1_POSITION, "shield_lifeline")
    self.fifty_fifty_lifeline = Lifeline(LIFELINE_2_POSITION, "fifty_fifty_lifeline")
    self.switch_lifeline = Lifeline(LIFELINE_3_POSITION, "switch_lifeline")
    self.hearts = []
    for i in range(5):
        heart_position = (WINDOW_WIDTH/2 + 425 - (50 * i), WINDOW_HEIGHT/2 - 275)
        self.hearts.append(Heart(heart_position))

    self.interactive_elements.append(self.surrender)
    self.interactive_elements.append(self.shield_lifeline)
    self.interactive_elements.append(self.fifty_fifty_lifeline)
    self.interactive_elements.append(self.switch_lifeline)


    # Set up events
    self.question.set_up_question_events()


  def draw(self):
    self.elements.draw(self.screen)
    self.shield_lifeline.draw()
    self.fifty_fifty_lifeline.draw()
    self.switch_lifeline.draw()
    for i in range(self.total_lives):
      self.hearts[i].draw()


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
      self.click_option()
      self.click_lifeline()

  def display_options(self):
    for i in range (4):
      self.interactive_elements[i].set_title(self.options[i])

  def generate_random_index(self, *args):
    self.number_questions = len(self.file_manager.get_data()[self.current_level])
    self.question_index = random.randrange(self.number_questions)
    if self.number_questions > 1:
      # Avoid generating the same question
      while self.question == self.file_manager.get_data()[self.current_level][self.question_index]["question"]:
        self.question_index= random.randrange(self.number_questions)

  def update_display_data(self, *args):
    self.options = self.file_manager.get_data()[self.current_level][self.question_index]["options"]
    self.answer = self.file_manager.get_data()[self.current_level][self.question_index]["answer"]
    self.question = self.file_manager.get_data()[self.current_level][self.question_index]["question"]
    self.event_manager.notify("change_question", self.question)

  def shuffle_options(self, *args):
    random.shuffle(self.options)

  def click_option(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for i in range (4):
                if self.interactive_elements[i].get_rect().collidepoint(pygame.mouse.get_pos()) and self.interactive_elements[i].get_title() != '':
                    self.modal.set_option(i)
                    self.switch_modal()
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

  def click_lifeline(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for lifeline in self.lifelines:
                if lifeline.get_rect().collidepoint(pygame.mouse.get_pos()):
                    if lifeline.get_type() == "fifty_fifty_lifeline":
                      self.set_options(lifeline.fifty_fifty_lifeline(self.options, self.answer))
                    elif lifeline.get_type() == "switch_lifeline":
                      prev_index = self.question_index
                      self.generate_random_index()
                      if prev_index != self.question_index:
                        self.update_display_data()
                        self.shuffle_options()
                    elif lifeline.get_type() == "shield_lifeline":
                      self.active_shield = True
                    self.lifelines.remove(lifeline)
                    lifeline.disable()
                    self.click_handled = True
                    return
    else:
        self.click_handled = False

  def start_game(self, *args):
    self.save_level = 0
    self.current_level = 0
    self.practice_mode = False
    self.score.set_practice_mode(False)

    self.load_difficulty()

    self.score.restart()

    self.lifelines.clear()
    self.lifelines.append(self.switch_lifeline)
    self.lifelines.append(self.fifty_fifty_lifeline)
    self.lifelines.append(self.shield_lifeline)

    self.fifty_fifty_lifeline.enable()
    self.switch_lifeline.enable()
    self.shield_lifeline.enable()
    

  def load_difficulty(self):
    print(self.difficulty)
    if self.difficulty == 'Practice':
      self.lives = 0
      self.correct_answers = 0
      self.wrong_answer = 0
      self.score.set_practice_mode(True)
      self.practice_mode = True
    elif self.difficulty == 'Easy':
      self.lives = 5
    elif self.difficulty == 'Normal':
      self.lives = 3
    elif self.difficulty == 'Hard':
      self.lives = 1

    for i in range (self.lives):
      self.hearts[i].enable()
    self.total_lives= self.lives
    

  def switch_modal(self, *args):
    self.display_modal = not self.display_modal
    self.surrender.set_disable(self.display_modal)

  # args[0] = index of the option
  def validate_answer(self, *args):
    option_position = args[0]
    # Check the answer with the selected option
    if(self.answer.lower() == self.interactive_elements[option_position].get_title().lower()):
      self.current_level += 1
      self.active_shield = False
      self.surrender.set_level(self.current_level)
      # Check if it is a save level (5, 10, 15)
      if self.current_level % 5 == 0:
        self.save_level = self.current_level
      if self.practice_mode:
        self.correct_answers += 1

      if self.current_level == LAST_LEVEL:
        self.event_manager.notify("set_state", "win")
        self.event_manager.notify("final_reward", self.current_level - 1)
      else:
        self.generate_random_index()
        self.update_display_data()
        self.shuffle_options()
        self.score.next_level()
    else:
      if self.active_shield:
        self.active_shield = False
        self.options[option_position] = ''
        return
      self.hearts[self.total_lives - self.lives].disable()
      self.lives -= 1
      if self.lives == 0 and not self.practice_mode:
        self.event_manager.notify("game_over_message", (self.answer, self.save_level))
        self.event_manager.notify("set_state", "game over")
      if self.practice_mode:
        self.current_level += 1
        self.generate_random_index()
        self.update_display_data()
        self.shuffle_options()
        self.wrong_answer += 1
  
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

  def set_difficulty(self, *args):
    self.difficulty = args[0]

  def set_up_play_events(self):
    self.event_manager.subscribe("display_question", self.update_display_data)
    self.event_manager.subscribe("choose_random_question", self.generate_random_index)
    self.event_manager.subscribe("shuffle_options", self.shuffle_options)
    self.event_manager.subscribe("start_game", self.start_game)
    self.event_manager.subscribe("switch_modal", self.switch_modal)
    self.event_manager.subscribe("validate_answer", self.validate_answer)
    self.event_manager.subscribe("display_surrender_modal", self.switch_surrender_modal)
    self.event_manager.subscribe("display_win_screen", self.display_win_screen)
    self.event_manager.subscribe("set_difficulty", self.set_difficulty)

  def set_options(self, options):
    self.options = options

