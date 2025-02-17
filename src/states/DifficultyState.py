from config.settings import *
from .State import *
from utils.Box import *
from utils.Button import *
from utils.DifficultyOption import *


DIFFICULTIES = [
  ("Practice","_yellow", (WINDOW_WIDTH//2 - 225, WINDOW_HEIGHT//2 - 35)),
  ("Easy","_green",(WINDOW_WIDTH//2 - 225, WINDOW_HEIGHT//2 + 65)),
  ("Normal","_light_blue",(WINDOW_WIDTH//2 + 225, WINDOW_HEIGHT//2 - 35)),
  ("Hard","_red",(WINDOW_WIDTH//2 + 225, WINDOW_HEIGHT//2 + 65))
]

class Difficulty(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.box = Box(self.elements)
    box_rect = self.box.get_rect()
    self.active_difficulty = None
    self.display_warning_message = False

    TITLE_POSTION = (box_rect.centerx, box_rect.top + 50)
    WARNING_POSTION = (box_rect.centerx, box_rect.top + 100)

    self.text_elements = [
      (TITLE.render("Select Difficulty", True, COLORS["AMBER"]), TITLE_POSTION),
    ]
    self.warning_message = TEXT.render("Please select a difficulty", True, COLORS["RED"])
    self.waning_rect = self.warning_message.get_rect(center=WARNING_POSTION)

    self.difficulties = []
    for difficulty, color, position in DIFFICULTIES:
      option = DifficultyOption(difficulty, position, self.elements, color)
      self.difficulties.append(option)
      self.interactive_elements.append(option)

    self.continue_btn = Button(self.elements,RIGHT_BTN_POSITION, event_manager, text="Start")
    self.back_btn = Button(self.elements,LEFT_BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.continue_btn)
    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    for text_surface, position in self.text_elements:
      text_rect = text_surface.get_rect(center=position)
      self.screen.blit(text_surface, text_rect)
    for difficulty in self.difficulties:
      if not difficulty.get_active():
        difficulty.draw_overlay()
    if self.display_warning_message:
      self.screen.blit(self.warning_message, self.waning_rect)
    

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()

  def is_difficulty_selected(self):
    is_selected = False
    if self.active_difficulty == None:
      self.display_warning_message = True
    else:
      is_selected = True
    return is_selected

  def check_click(self):
    if not pygame.mouse.get_pressed()[0]:
        self.click_handled = False
        return

    if self.click_handled:
        return

    if self.check_difficulty_click():
        self.click_handled = True
        return

    if self.check_continue_click():
        self.click_handled = True
        return

    if self.check_back_click():
        self.click_handled = True

  def check_difficulty_click(self):
    for difficulty in self.difficulties:
        if difficulty.get_rect().collidepoint(pygame.mouse.get_pos()):
            if self.active_difficulty:
                self.active_difficulty.set_active(False)
            difficulty.set_active(True)
            self.active_difficulty = difficulty
            return True
    return False

  def check_continue_click(self):
    if self.continue_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
        if self.is_difficulty_selected():
            self.event_manager.notify("set_difficulty", self.active_difficulty.get_title())
            self.continue_btn.check_notify_state("game")
            self.active_difficulty.set_active(False)
            self.display_warning_message = False
            self.active_difficulty = None
        else:
            self.display_warning_message = True
        return True
    return False
  
  def check_back_click(self):
    if self.back_btn.check_notify_state("rewards"):
        if self.active_difficulty:
            self.active_difficulty.set_active(False)
            self.display_warning_message = False
            self.active_difficulty = None
        return True
    return False
