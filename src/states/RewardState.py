from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *
from utils.RewardBox import *

class Rewards(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = RewardsBox(self.elements)

    self.font_title = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 22)
    self.text = self.font_title.render("Rewards", True, COLORS["AMBER"])
    box_rect = self.box.get_rect()
    self.text_rect = self.text.get_rect(center = (box_rect.centerx, box_rect.top + 50))

    self.continue_btn = Button(self.elements,(box_rect.midright[0] - 170, box_rect.midright[1] + 190), event_manager)
    self.back_btn = Button(self.elements,(box_rect.midleft[0] + 170, box_rect.midleft[1] + 190), event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.continue_btn)
    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    
    
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
