from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.ContinueBtn import *

class Rewards(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = Box(self.elements, event_manager)
    self.font_title = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.text = self.font_title.render("Rewards", True, COLORS["AMBER"])
    box_rect = self.box.get_rect()
    self.text_rect = self.text.get_rect(center = (box_rect.centerx, box_rect.top + 75))
    self.continue_btn = ContinueBtn((box_rect.midright[0] - 170, box_rect.midright[1] + 190), event_manager)
    self.back_btn = ContinueBtn((box_rect.midleft[0] + 170, box_rect.midleft[1] + 190), event_manager, 'negative_btn', 'Go Back', 'WHITE')

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    self.continue_btn.draw()
    self.back_btn.draw()
    
    
  def update(self):
    self.elements.update()
    self.check_click()


  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.continue_btn.check_notify_state("game")
        self.back_btn.check_notify_state("play")
    else:
        self.click_handled = False
