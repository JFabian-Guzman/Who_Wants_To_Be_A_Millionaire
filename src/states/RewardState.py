from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *
from utils.RewardBox import *

class Rewards(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)

    self.box = RewardsBox(self.elements)
    box_rect = self.box.get_rect()

    self.title = TITLE.render("Rewards", True, COLORS["AMBER"])
    self.title_rect = self.title.get_rect(center = (box_rect.centerx, box_rect.top + 50))

    self.continue_btn = Button(self.elements,RIGHT_BTN_POSITION, event_manager)
    self.back_btn = Button(self.elements,LEFT_BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.continue_btn)
    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title, self.title_rect)
    
  def update(self):
    self.elements.update()
    self.check_click()
    self.update_cursor_state()


  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.continue_btn.check_notify_state("game")
        self.back_btn.check_notify_state("play")
    else:
        self.click_handled = False
